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

from logging import getLogger

from discord import Embed
from main import bot as bot_var
from utils.helpers import interaction_or_context, perm_format

# from typing import Union, Sequence
# from datetime import datetime

# from traceback import format_exc


# from discord.ext.commands import Context


log = getLogger(__name__)


async def info_func(transaction, role_arg):
    role = await interaction_or_context("ROLE", transaction, role_arg)
    has_perm = [
        perm
        for perm in bot_var.configuration.guild_perms
        if getattr(role.permissions, perm)
    ]
    embed = Embed(
        title=f"{role.name}",
        description=f"{role.mention} was created <t:{int(role.created_at.timestamp())}:R>",
        color=role.colour,
    )
    embed.set_author(name=f"ID: {role.id}")
    embed.add_field(name="Members in role:", value=len(role.members), inline=True)
    embed.add_field(name="Position", value=role.position, inline=True)
    embed.add_field(name="Colour:", value=role.colour, inline=True)
    embed.add_field(name="Hoisted:", value=role.hoist, inline=True)
    embed.add_field(name="Mentionable:", value=role.mentionable, inline=True)
    embed.add_field(name="Intergration:", value=role.managed, inline=True)
    embed.add_field(
        name=f"Permissions",
        value=", ".join([perm_format(name) for name, value in has_perm if not value]),
        inline=False,
    )
    await interaction_or_context("SEND", transaction, embed)


async def members_func(transaction, role_arg):
    role = await interaction_or_context("ROLE", transaction, role_arg)
    members = [f"{member.mention}, " for member in role.members]
    if len(members) == 0:
        members.append("No members")
    embed = Embed(
        title=f"{len(role.members)} Members in `{role}`", description=f" ".join(members)
    )
    await interaction_or_context("SEND", transaction, embed)


async def permissions_func(transaction, role_arg):
    role = await interaction_or_context("ROLE", transaction, role_arg)
    has_perm = [perm[0] for perm in role.permissions if perm[1]]
    if len(has_perm) == 0:
        has_perm.append("No permissions")
    embed = Embed(
        title=f"Permissions for `{role}`",
        description=f", ".join(has_perm).replace("_", " ").title(),
    )
    await interaction_or_context("SEND", transaction, embed)
