from discord import Embed

from main import bot as bot_var
from utils.helpers import interaction_or_context, perm_format

# from typing import Union, Sequence
# from datetime import datetime

# from traceback import format_exc


# from discord.ext.commands import Context


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
