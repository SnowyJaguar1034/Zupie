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

from discord import (CategoryChannel, Interaction, Object, Role, StageChannel,
                     TextChannel, VoiceChannel, app_commands)
from discord.ext import commands
from discord.ext.commands import GroupCog
from dotenv import load_dotenv
from utils.helper_roles import info_func, members_func, permissions_func
from utils.helpers import parent

# from main import bot

load_dotenv()

from logging import getLogger

log = getLogger(__name__)

default_guild = int(environ.get("DEFAULT_GUILD"))


class Role_Cog(
    GroupCog,
    name="role",
    description="Shows all role related commands, legacy and slash",
):
    def __init__(self, bot):
        # super().__init__(bot)
        self.bot = bot

    edit_role = app_commands.Group(
        name="edit", description="edit Role stuff.", guild_ids=[default_guild]
    )
    info_description = "Show some information about a role"
    members_description = "Show the members who have this role."
    permissions_description = "Show a role's permission, Defualts to current channel."
    role_param = "Defaults to your highest role"

    @commands.group(
        name="role",
        invoke_without_command=True,
        case_insensitive=True,
        aliases=["rank"],
    )
    async def role_group(self, ctx):
        await parent(ctx)

    @role_group.command(
        name="info",
        description=info_description,
        usage="<role>",
        aliases=["whatis", "ri"],
    )
    async def info_legacy(self, ctx, role: Role = None):
        await info_func(ctx, role)

    @app_commands.command(name="info", description=info_description)
    @app_commands.describe(role=role_param)
    async def info_slash(
        self,
        interaction: Interaction,
        role: Role = None,
        channel: Union[TextChannel, VoiceChannel, StageChannel, CategoryChannel] = None,
    ):
        await info_func(interaction, role, channel)

    @role_group.command(
        name="members",
        description=members_description,
        usage="[role]",
    )
    async def members_legacy(self, ctx, role: Role = None):
        await members_func(ctx, role)

    @app_commands.command(name="members", description=members_description)
    @app_commands.describe(role=role_param)
    async def members_slash(
        self,
        interaction: Interaction,
        role: Role = None,
        channel: Union[TextChannel, VoiceChannel, StageChannel, CategoryChannel] = None,
    ):
        await members_func(interaction, role, channel)

    @role_group.command(
        name="permissions",
        description=permissions_description,
        usage="[role]",
        aliases=["perms"],
    )
    async def permissions_legacy(self, ctx, role: Role = None):
        await permissions_func(ctx, role)

    @app_commands.command(name="permissions", description=permissions_description)
    @app_commands.describe(role=role_param)
    @app_commands.describe(channel="The channel to get permissions for.")
    async def permissions_slash(
        self,
        interaction: Interaction,
        role: Role = None,
        channel: Union[TextChannel, VoiceChannel, StageChannel, CategoryChannel] = None,
    ):
        await permissions_func(interaction, role, channel)

    @role_group.group(name="edit", description=permissions_description)
    async def edit_legacy(self, ctx, role: Role = None):
        await parent(ctx)

    @edit_legacy.command(name="name")
    async def edit_name_legacy(
        self, interaction: Interaction, role: Role = None, *, name=str
    ):
        print("'edit_name_legacy' print out")

    @edit_role.command(name="name")
    @app_commands.describe(role=role_param)
    @app_commands.describe(name="The name you want the role to have")
    async def edit_name_slash(
        self, interaction: Interaction, role: Role = None, *, name: str
    ):
        print("edit_name_slash print out")


async def setup(bot):
    await bot.add_cog(Role_Cog(bot), guild=Object(id=default_guild))
