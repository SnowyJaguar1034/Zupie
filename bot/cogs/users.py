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

from os import environ
from typing import Union

from discord import (
    CategoryChannel,
    Interaction,
    Member,
    Object,
    StageChannel,
    TextChannel,
    User,
    VoiceChannel,
    app_commands,
)
from discord.ext import commands
from discord.ext.commands import GroupCog
from dotenv import load_dotenv
from utils.helper_users import (
    avatar_func,
    info_func,
    joined_func,
    permissions_func,
    roles_func,
    status_func,
)
from utils.helpers import parent

# from main import bot

load_dotenv()

default_guild = int(environ.get("DEFAULT_GUILD"))


class User_Cog(
    GroupCog,
    name="user",
    description="Shows all user related commands, legacy and slash",
):
    def __init__(self, bot):
        # super().__init__(bot)
        self.bot = bot

    # slash_user_group = app_commands.Group(name="users", description="Check User stuff.", guild_ids=[default_guild])
    info_description = "Show some information about yourself or the member specified."
    joined_description = (
        "Show when yourself or the member specified joined this server and Discord."
    )
    avatar_description = "Show a users avatar."
    roles_description = "Show a users roles."
    status_description = "Show a users status."
    permissions_description = "Show a member's permission, Defualts to current channel."

    @commands.group(
        name="user",
        aliases=["member"],
        invoke_without_command=True,
        case_insensitive=True,
    )
    async def legacy_user_group(self, ctx):
        await parent(ctx)

    @legacy_user_group.command(
        name="info",
        description=info_description,
        usage="[member]",
        aliases=["whois", "ui"],
    )
    async def info_legacy(
        self, ctx: commands.Context, member: Union[Member, User] = None
    ):
        await info_func(ctx, member)

    @app_commands.command(name="info", description=info_description)
    @app_commands.describe(member="The discord member to get information for.")
    async def info_slash(
        self, interaction: Interaction, member: Union[Member, User] = None
    ):
        await info_func(interaction, member)

    @legacy_user_group.command(
        name="joined",
        description=joined_description,
        usage="[member]",
        aliases=["dates", "created", "j"],
    )
    async def joined_legacy(self, ctx, member: Member = None):
        await joined_func(ctx, member)

    @app_commands.command(name="joined", description=joined_description)
    @app_commands.describe(member="The discord member to get information for.")
    async def joined_slash(self, interaction: Interaction, member: Member = None):
        await joined_func(interaction, member)

    @legacy_user_group.command(
        name="avatar", description=avatar_description, usage="[member]", aliases=["av"]
    )
    async def avatar_legacy(self, ctx, member: Union[Member, User] = None):
        await avatar_func(ctx, member)

    @app_commands.command(name="avatar", description=avatar_description)
    @app_commands.describe(member="The discord member to get information for.")
    async def avatar_slash(
        self, interaction: Interaction, member: Union[Member, User] = None
    ):
        await avatar_func(interaction, member)

    @legacy_user_group.command(
        name="roles", description=roles_description, usage="[member]"
    )
    async def roles_legacy(self, ctx, member: Member = None):
        await roles_func(ctx, member)

    @app_commands.command(name="roles", description=roles_description)
    @app_commands.describe(member="The discord member to get information for.")
    async def roles_slash(self, interaction: Interaction, member: Member = None):
        await roles_func(interaction, member)

    @legacy_user_group.command(
        name="status", description=status_description, usage="[member]"
    )
    async def status_legacy(self, ctx, member: Union[Member, User] = None):
        await status_func(ctx, member)

    @app_commands.command(name="status", description=status_description)
    @app_commands.describe(member="The discord member to get information for.")
    async def status_slash(
        self, interaction: Interaction, member: Union[Member, User] = None
    ):
        await status_func(interaction, member)

    @legacy_user_group.command(
        name="permissions",
        description=permissions_description,
        usage="[member] [channel]",
        aliases=["perms"],
    )
    async def permissions_legacy(
        self,
        ctx,
        member: Member = None,
        channel: Union[TextChannel, VoiceChannel, StageChannel, CategoryChannel] = None,
    ):
        await permissions_func(ctx, member, channel)

    @app_commands.command(name="permissions", description=permissions_description)
    @app_commands.describe(member="The discord member to get information for.")
    @app_commands.describe(channel="The channel to get permissions for.")
    async def permissions_slash(
        self,
        interaction: Interaction,
        member: Member = None,
        channel: Union[TextChannel, VoiceChannel, StageChannel, CategoryChannel] = None,
    ):
        await permissions_func(interaction, member, channel)


@app_commands.context_menu(name="User Info")
async def info_menu(interaction: Interaction, member: Union[Member, User]):
    await info_func(interaction, member)


@app_commands.context_menu(name="User Joined\Created")
async def joined_menu(interaction: Interaction, member: Union[Member, User]):
    await joined_func(interaction, member)


@app_commands.context_menu(name="User Avatar")
async def avatar_menu(interaction: Interaction, member: Union[Member, User]):
    await avatar_func(interaction, member)


@app_commands.context_menu(name="User Roles")
async def roles_menu(interaction: Interaction, member: Union[Member, User]):
    await roles_func(interaction, member)


@app_commands.context_menu(name="User Status")
async def status_menu(interaction: Interaction, member: Union[Member, User]):
    await status_func(interaction, member)


@app_commands.context_menu(name="User Permissions")
async def permissions_menu(interaction: Interaction, member: Union[Member, User]):
    await permissions_func(interaction, member, interaction.channel)


async def setup(bot):
    await bot.add_cog(User_Cog(bot), guild=Object(id=default_guild))
    menus = [info_menu, joined_menu, avatar_menu, roles_menu, status_menu]
    for menu in menus:
        bot.tree.add_command(menu, guild=Object(id=default_guild))
    bot.tree.add_command(permissions_menu)
