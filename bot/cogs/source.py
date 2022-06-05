import inspect
from pathlib import Path
from typing import Optional, Tuple, Union

from discord import Embed
from discord.ext import commands
from discord.ext.commands import (BadArgument, Bot, Cog, Command, Context,
                                  Converter, ExtensionNotLoaded, HelpCommand)
from discord.utils import escape_markdown

SourceType = Union[
    HelpCommand,
    Command,
    Cog,
    ExtensionNotLoaded,
]

GITHUB_REPO = "https://github.com/SnowyJaguar1034/Zupie"
GITHUB_AVATAR = "https://avatars1.githubusercontent.com/u/9919"


class SourceConverter(Converter):
    """Convert an argument into a help command, tag, command, or cog."""

    @staticmethod
    async def convert(ctx: Context, argument: str) -> SourceType:
        """Convert argument into source object."""
        if argument.lower() == "help":
            return ctx.bot.help_command

        cog = ctx.bot.get_cog(argument)
        if cog:
            return cog

        cmd = ctx.bot.get_command(argument)
        if cmd:
            return cmd

        escaped_arg = escape_markdown(argument)

        raise BadArgument(f"Unable to convert '{escaped_arg}' to valid command or Cog.")


class BotSource(Cog):
    """Displays information about the bot's source code."""

    def __init__(self, bot: Bot):
        self.bot = bot

    @commands.command(name="source", aliases=("src",))
    async def source_command(
        self, ctx: commands.Context, *, source_item: SourceConverter = None
    ):
        """Display information and a GitHub link to the source code of a command, tag, or cog."""
        if not source_item:
            embed = Embed(
                title=f"{self.bot.user.name}'s GitHub Repository",
                description=f"This repository includes all of {self.bot.user.name}'s source code so that you can see we're not doing anything dodgy with your data.",
            )
            embed.add_field(name="Repository", value=f"[Go to GitHub]({GITHUB_REPO})")
            embed.set_thumbnail(url=GITHUB_AVATAR)
            await ctx.send(embed=embed)
            return

        embed = await self.build_embed(source_item)
        await ctx.send(embed=embed)

    def get_source_link(
        self, source_item: SourceType
    ) -> Tuple[str, str, Optional[int]]:

        """
        Build GitHub link of source item, return this link, file location and first line number.

        Raise BadArgument if `source_item` is a dynamically-created object (e.g. via internal eval).
        """

        if isinstance(source_item, commands.Command):
            source_item = inspect.unwrap(source_item.callback)
            src = source_item.__code__
            filename = src.co_filename
        else:
            src = type(source_item)
            try:
                filename = inspect.getsourcefile(src)
            except TypeError:
                raise commands.BadArgument(
                    "Cannot get source for a dynamically-created object."
                )

        try:
            lines, first_line_no = inspect.getsourcelines(src)
        except OSError:
            raise commands.BadArgument(
                "Cannot get source for a dynamically-created object."
            )

        lines_extension = f"#L{first_line_no}-L{first_line_no+len(lines)-1}"

        # Handle tag file location differently than others to avoid errors in some cases
        if not first_line_no:
            file_location = Path(filename).relative_to("bot/")
        else:
            file_location = Path(filename).relative_to(Path.cwd()).as_posix()

        url = f"{GITHUB_REPO}/blob/main/{file_location}{lines_extension}"

        return url, file_location, first_line_no or None

    async def build_embed(self, source_object: SourceType) -> Optional[Embed]:
        """Build embed based on source object."""
        url, location, first_line = self.get_source_link(source_object)

        if isinstance(source_object, commands.HelpCommand):
            title = "Help Command"
            description = source_object.__doc__.splitlines()[1]
        elif isinstance(source_object, commands.Command):
            description = source_object.short_doc
            title = f"Command: {source_object.qualified_name}"
        else:
            title = f"Cog: {source_object.qualified_name}"
            description = source_object.description.splitlines()[0]

        embed = Embed(title=title, description=description)
        embed.set_thumbnail(url=GITHUB_AVATAR)
        embed.add_field(name="Source Code", value=f"[Go to GitHub]({url})")
        embed.add_field(name="File Location", value=f"`{location}`")
        line_text = f"{first_line}" if first_line else ""
        embed.set_footer(text=f"First line: {line_text}")
        # embed.set_footer(text=f"{location}{line_text}")

        return embed


async def setup(bot):
    """Load the BotSource cog."""
    await bot.add_cog(BotSource(bot))
