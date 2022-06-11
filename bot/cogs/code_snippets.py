"""
BSD 3-Clause License (BSD-3)

Copyright (c) 2022, SnowyJaguar1034(Teagan Collyer)
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this
   list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice,
   this list of conditions and the following disclaimer in the documentation
   and/or other materials provided with the distribution.

3. Neither the name of the copyright holder nor the names of its
   contributors may be used to endorse or promote products derived from
   this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY COPYRIGHT HOLDER "AS IS" AND ANY EXPRESS OR
IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF
MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO
EVENT SHALL COPYRIGHT HOLDER BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS;
OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR
OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF
ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""

import os
import re
from asyncio import TimeoutError as AsyncTimeoutError
from functools import partial
from textwrap import dedent
from traceback import format_exc
from typing import Any, Sequence
from urllib.parse import quote_plus

from aiohttp import ClientResponseError
from discord import Interaction, Message, NotFound, Object, Reaction, app_commands
from discord.abc import User
from discord.ext.commands import Cog, Context, GroupCog
from dotenv import load_dotenv

load_dotenv()

default_guild = int(os.environ.get("DEFAULT_GUILD"))

from logging import getLogger

log = getLogger(__name__)

GITHUB_RE = re.compile(
    r"https://github\.com/(?P<repo>[a-zA-Z0-9-]+/[\w.-]+)/blob/"
    r"(?P<path>[^#>]+)(\?[^#>]+)?(#L(?P<start_line>\d+)(([-~:]|(\.\.))L(?P<end_line>\d+))?)"
)

GITHUB_GIST_RE = re.compile(
    r"https://gist\.github\.com/([a-zA-Z0-9-]+)/(?P<gist_id>[a-zA-Z0-9]+)/*"
    r"(?P<revision>[a-zA-Z0-9]*)/*#file-(?P<file_path>[^#>]+?)(\?[^#>]+)?"
    r"(-L(?P<start_line>\d+)([-~:]L(?P<end_line>\d+))?)"
)

GITHUB_HEADERS = {"Accept": "application/vnd.github.v3.raw"}

GITLAB_RE = re.compile(
    r"https://gitlab\.com/(?P<repo>[\w.-]+/[\w.-]+)/\-/blob/(?P<path>[^#>]+)"
    r"(\?[^#>]+)?(#L(?P<start_line>\d+)(-(?P<end_line>\d+))?)"
)

BITBUCKET_RE = re.compile(
    r"https://bitbucket\.org/(?P<repo>[a-zA-Z0-9-]+/[\w.-]+)/src/(?P<ref>[0-9a-zA-Z]+)"
    r"/(?P<file_path>[^#>]+)(\?[^#>]+)?(#lines-(?P<start_line>\d+)(:(?P<end_line>\d+))?)"
)


class CodeSnippets(
    GroupCog,
    name="snippets",
    description="Cog that parses and sends code snippets to Discord.",
):
    def __init__(self, bot):
        # super().__init__(bot)
        self.bot = bot

        self.pattern_handlers = [
            (GITHUB_RE, self._fetch_github_snippet),
            (GITHUB_GIST_RE, self._fetch_github_gist_snippet),
            (GITLAB_RE, self._fetch_gitlab_snippet),
            (BITBUCKET_RE, self._fetch_bitbucket_snippet),
        ]

    def reaction_check(
        self,
        reaction: Reaction,
        user: User,
        *,
        message_id: int,
        allowed_emoji: Sequence[str],
        # allowed_users: Sequence[int],
    ) -> bool:
        """
        Check if a reaction's emoji and author are allowed and the message is `message_id`.
        If the user is not allowed, remove the reaction. Ignore reactions made by the bot.
        If `allow_mods` is True, allow users with moderator roles even if they're not in `allowed_users`.
        """
        right_reaction = (
            user != self.bot.user
            and reaction.message.id == message_id
            and str(reaction.emoji) in allowed_emoji
        )
        if not right_reaction:
            return False

        """ 
        if user.id in allowed_users:
            # log.trace(f"Allowed reaction {reaction} by {user} on {reaction.message.id}.")
            return True
        else:
            # log.trace(f"Removing reaction {reaction} by {user} on {reaction.message.id}: disallowed user.")
            return False 
        """

    async def wait_for_deletion(
        self,
        message: Message,
        user_ids: Sequence[int],
        deletion_emoji: Sequence[str] = "🗑️",
        timeout: float = 60 * 5,
        attach_emojis: bool = True,
        allow_mods: bool = True,
    ) -> None:
        """
        Wait for any of `user_ids` to react with one of the `deletion_emoji` within `timeout` seconds to delete `message`.
        If `timeout` expires then reactions are cleared to indicate the option to delete has expired.
        An `attach_emojis` bool may be specified to determine whether to attach the given
        `deletion_emoji` to the message in the given `context`.
        An `allow_mods` bool may also be specified to allow anyone with a role in `MODERATION_ROLES` to delete
        the message.
        """

        if attach_emojis:
            try:
                await message.add_reaction(deletion_emoji)
            except NotFound:
                string = f"Aborting wait_for_deletion: message {message.id} deleted prematurely.\{format_exc()}"
                # log.trace(string)
                print(string)
                return

        check = partial(
            self.reaction_check,
            message_id=message.id,
            allowed_emoji=deletion_emoji,
            # allowed_users=user_ids,
            # allow_mods=allow_mods,
        )

        try:
            try:
                await self.bot.wait_for(
                    "reaction_add",
                    check=check,
                    timeout=timeout,
                )
            except AsyncTimeoutError:
                await message.clear_reactions()
            else:
                await message.delete()

        except NotFound:
            string = f"wait_for_deletion: message {message.id} deleted prematurely."
            # log.trace(string)
            print(string)

    async def _fetch_response(self, url: str, response_format: str, **kwargs) -> Any:
        """Makes http requests using aiohttp."""
        async with self.bot.session.get(
            url, raise_for_status=True, **kwargs
        ) as response:
            if response_format == "text":
                return await response.text()
            elif response_format == "json":
                return await response.json()

    def _find_ref(self, path: str, refs: tuple) -> tuple:
        """Loops through all branches and tags to find the required ref."""
        # Base case: there is no slash in the branch name
        ref, file_path = path.split("/", 1)
        # In case there are slashes in the branch name, we loop through all branches and tags
        for possible_ref in refs:
            if path.startswith(possible_ref["name"] + "/"):
                ref = possible_ref["name"]
                file_path = path[len(ref) + 1 :]
                break
        return ref, file_path

    async def _fetch_github_snippet(
        self, repo: str, path: str, start_line: str, end_line: str
    ) -> str:
        """Fetches a snippet from a GitHub repo."""
        # Search the GitHub API for the specified branch
        branches = await self._fetch_response(
            f"https://api.github.com/repos/{repo}/branches",
            "json",
            headers=GITHUB_HEADERS,
        )
        tags = await self._fetch_response(
            f"https://api.github.com/repos/{repo}/tags", "json", headers=GITHUB_HEADERS
        )
        refs = branches + tags
        ref, file_path = self._find_ref(path, refs)

        file_contents = await self._fetch_response(
            f"https://api.github.com/repos/{repo}/contents/{file_path}?ref={ref}",
            "text",
            headers=GITHUB_HEADERS,
        )
        return self._snippet_to_codeblock(
            file_contents, file_path, start_line, end_line
        )

    async def _fetch_github_gist_snippet(
        self,
        gist_id: str,
        revision: str,
        file_path: str,
        start_line: str,
        end_line: str,
    ) -> str:
        """Fetches a snippet from a GitHub gist."""
        gist_json = await self._fetch_response(
            f'https://api.github.com/gists/{gist_id}{f"/{revision}" if len(revision) > 0 else ""}',
            "json",
            headers=GITHUB_HEADERS,
        )

        # Check each file in the gist for the specified file
        for gist_file in gist_json["files"]:
            if file_path == gist_file.lower().replace(".", "-"):
                file_contents = await self._fetch_response(
                    gist_json["files"][gist_file]["raw_url"],
                    "text",
                )
                return self._snippet_to_codeblock(
                    file_contents, gist_file, start_line, end_line
                )
        return ""

    async def _fetch_gitlab_snippet(
        self, repo: str, path: str, start_line: str, end_line: str
    ) -> str:
        """Fetches a snippet from a GitLab repo."""
        enc_repo = quote_plus(repo)

        # Searches the GitLab API for the specified branch
        branches = await self._fetch_response(
            f"https://gitlab.com/api/v4/projects/{enc_repo}/repository/branches", "json"
        )
        tags = await self._fetch_response(
            f"https://gitlab.com/api/v4/projects/{enc_repo}/repository/tags", "json"
        )
        refs = branches + tags
        ref, file_path = self._find_ref(path, refs)
        enc_ref = quote_plus(ref)
        enc_file_path = quote_plus(file_path)

        file_contents = await self._fetch_response(
            f"https://gitlab.com/api/v4/projects/{enc_repo}/repository/files/{enc_file_path}/raw?ref={enc_ref}",
            "text",
        )
        return self._snippet_to_codeblock(
            file_contents, file_path, start_line, end_line
        )

    async def _fetch_bitbucket_snippet(
        self, repo: str, ref: str, file_path: str, start_line: str, end_line: str
    ) -> str:
        """Fetches a snippet from a BitBucket repo."""
        file_contents = await self._fetch_response(
            f"https://bitbucket.org/{quote_plus(repo)}/raw/{quote_plus(ref)}/{quote_plus(file_path)}",
            "text",
        )
        return self._snippet_to_codeblock(
            file_contents, file_path, start_line, end_line
        )

    def _snippet_to_codeblock(
        self, file_contents: str, file_path: str, start_line: str, end_line: str
    ) -> str:
        """
        Given the entire file contents and target lines, creates a code block.

        First, we split the file contents into a list of lines and then keep and join only the required
        ones together.

        We then dedent the lines to look nice, and replace all ` characters with `\u200b to prevent
        markdown injection.

        Finally, we surround the code with ``` characters.
        """
        # Parse start_line and end_line into integers
        if end_line is None:
            start_line = end_line = int(start_line)
        else:
            start_line = int(start_line)
            end_line = int(end_line)

        split_file_contents = file_contents.splitlines()

        # Make sure that the specified lines are in range
        if start_line > end_line:
            start_line, end_line = end_line, start_line
        if start_line > len(split_file_contents) or end_line < 1:
            return ""
        start_line = max(1, start_line)
        end_line = min(len(split_file_contents), end_line)

        # Gets the code lines, dedents them, and inserts zero-width spaces to prevent Markdown injection
        required = "\n".join(split_file_contents[start_line - 1 : end_line])
        required = dedent(required).rstrip().replace("`", "`\u200b")

        # Extracts the code language and checks whether it's a "valid" language
        language = file_path.split("/")[-1].split(".")[-1]
        trimmed_language = language.replace("-", "").replace("+", "").replace("_", "")
        is_valid_language = trimmed_language.isalnum()
        if not is_valid_language:
            language = ""

        # Adds a label showing the file path to the snippet
        if start_line == end_line:
            ret = f"`{file_path}` line {start_line}\n"
        else:
            ret = f"`{file_path}` lines {start_line} to {end_line}\n"

        if len(required) != 0:
            return f"{ret}```{language}\n{required}```"
        # Returns an empty codeblock if the snippet is empty
        return f"{ret}``` ```"

    async def _parse_snippets(self, content: str) -> str:
        """Parse message content and return a string with a code block for each URL found."""
        all_snippets = []

        for pattern, handler in self.pattern_handlers:
            for match in pattern.finditer(content):
                try:
                    snippet = await handler(**match.groupdict())
                    all_snippets.append((match.start(), snippet))
                except ClientResponseError as error:
                    error_message = error.message  # noqa: B306
                    print(
                        f"Failed to fetch code snippet from {match[0]!r}: {error.status} ",
                        f"{error_message} for GET {error.request_info.real_url.human_repr()}",
                        sep="\n",
                    )
                    """
                    log.log(
                        logging.DEBUG if error.status == 404 else logging.ERROR,
                        f'Failed to fetch code snippet from {match[0]!r}: {error.status} '
                        f'{error_message} for GET {error.request_info.real_url.human_repr()}'
                    )
                    """
        # Sorts the list of snippets by their match index and joins them into a single message
        return "\n".join(map(lambda x: x[1], sorted(all_snippets)))

    async def send_snippet(self, message, url: str = None):
        """
        Checks if the message has a snippet link, removes the embed, then sends the snippet contents.
        """
        if isinstance(message, Interaction):
            if message.user.bot:
                return
        elif isinstance(message, Context):
            if message.author.bot:
                return
        elif isinstance(message, Message):
            if message.author.bot:
                return

        if message.guild is None:
            return

        if url is None:
            url = message.content
        message_to_send = await self._parse_snippets(url)
        destination = message.channel

        if 0 < len(message_to_send) <= 2000 and message_to_send.count("\n") <= 15:
            """
            try:
                await message.edit(suppress=True)
            except NotFound:
                # Don't send snippets if the original message was deleted.
                return
            """

            if isinstance(message, Message):
                await self.wait_for_deletion(
                    await destination.send(message_to_send), (message.author.id,)
                )
            elif isinstance(message, Interaction):
                await self.wait_for_deletion(
                    await destination.send(message_to_send), (message.user.id,)
                )

    @Cog.listener()
    async def on_message(self, message):
        await self.send_snippet(message)

    @app_commands.command(
        name="snippet", description="Sends a snippet of the provided URL."
    )
    @app_commands.describe(url="The url to snip.")
    @app_commands.guilds(Object(id=default_guild))
    async def snippet(self, interaction: Interaction, url: str):
        await interaction.response.send_message("Responded with snippet.")
        await self.send_snippet(interaction, url)


async def setup(bot):
    """Load the CodeSnippets cog."""
    await bot.add_cog(CodeSnippets(bot), guild=Object(id=default_guild))
