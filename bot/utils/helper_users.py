from main import bot as bot_var
from utils.helpers import interaction_or_context

from typing import Union, Sequence
from datetime import datetime
from traceback import format_exc

from discord import Member, User, Interaction, Embed, app_commands, Role, TextChannel, VoiceChannel, StageChannel, CategoryChannel, Colour, Object, Message, NotFound
from discord.ext.commands import Context

async def timestamps_func(member, embed, avatar):
        embed.add_field(name = "Joined Server:", value = f"<t:{int(member.joined_at.timestamp())}:R>", inline = True)
        if avatar == True:
            embed.add_field(name = "Avatar", value = f"[PNG]({member.avatar.with_static_format('png')})", inline = True)
        embed.add_field(name = "Joined Discord:", value = f"<t:{int(member.created_at.timestamp())}:R>", inline = True)

async def info_func(transaction, member_arg):
    member = await interaction_or_context("MEMBER", transaction, member_arg)
    member_status = "No status" if member.activity is None else member.activity.name
    embed = Embed(title = f"{member}", description = f"Status: **{member.status}**\n*{member_status}*", colour = member.colour)
    embed.set_author(name = f"{member.id}", icon_url = member.avatar.url)
    embed.set_thumbnail(url = member.avatar.url)
    await timestamps_func(member, embed, True)
    roles = [f"{role.mention}" for role in member.roles]
    if len(roles) == 0: roles.append("No roles")
    has_key = [perm for perm in bot_var.config.key_perms if getattr(member.guild_permissions, perm)]
    if len(has_key) == 0: has_key.append('No permissions')
    embed.add_field(name = f"Roles: {len(roles)}",value = f"{len(roles)} roles" if len(" ".join(roles)) > 1000 else " ".join(roles), inline = False)
    embed.add_field(name =f'Key permissions', value = ", ".join(has_key).replace("_"," ").title(), inline = False)
    await interaction_or_context("SEND", transaction, embed)

async def joined_func(transaction, member_arg):
    member = await interaction_or_context("MEMBER", transaction, member_arg)
    embed = Embed(title = f"{member}", colour = member.colour)
    embed.set_author(name = f"{member.id}", icon_url = member.avatar.url)
    embed.set_thumbnail(url = member.avatar.url)
    await timestamps_func(member, embed, False)
    await interaction_or_context("SEND", transaction, embed, False)

async def avatar_func(transaction, member_arg):
    member = await interaction_or_context("MEMBER", transaction, member_arg)
    embed = Embed(title = f"{member}'s Avatar", colour = member.colour)
    embed.add_field(name = "PNG", value = f"[Link]({member.avatar.with_static_format('png')})", inline = True)
    embed.add_field(name = "JPG", value = f"[Link]({member.avatar.with_static_format('jpg')})", inline = True)
    embed.add_field(name = "WebP", value = f"[Link]({member.avatar.with_static_format('webp')})", inline = True)
    embed.set_image(url = member.avatar.url)
    await interaction_or_context("SEND", transaction, embed, True)

async def roles_func(transaction, member_arg):
    member = await interaction_or_context("MEMBER", transaction, member_arg)
    roles = [f"<@&{role.id}>" for role in member.roles]
    if len(roles) == 0:
        roles.append("No roles")
    embed = Embed(title = f"Roles for {member.name}#{member.discriminator}: {len(roles)}", description = "Too many roles to list" if len(" ".join(roles)) > 1000 else " ".join(roles))
    await interaction_or_context("SEND", transaction, embed)
    
async def status_func(transaction, member_arg):
    member = await interaction_or_context("MEMBER", transaction, member_arg)
    member_status = "No status" if member.activity is None else member.activity.name
    embed = Embed(title = f"{member}", description = f"Status: **{member.status}**\n*{member_status}*", colour = member.colour)
    embed.set_author(name = f"{member.id}", icon_url = member.avatar.url)
    embed.set_thumbnail(url = member.avatar.url)
    await interaction_or_context("SEND", transaction, embed) 
        
async def permissions_func(transaction, member_arg, channel_arg):
    member = await interaction_or_context("MEMBER", transaction, member_arg)
    channel = await interaction_or_context("CHANNEL", transaction, channel_arg)
    permissions = channel.permissions_for(member)
    embed = Embed(title=f"Permission Information for {member}", colour = member.colour)
    embed.set_author(name = f"{member} | {member.id}", icon_url = member.avatar.url)
    embed.set_footer(text=f"{channel.name} | {channel.id}")
    embed.add_field(name = "Allowed", value = ", ".join([perm_format(name) for name, value in permissions if value]), inline = False)
    embed.add_field(name = "Denied", value=", ".join([perm_format(name) for name, value in permissions if not value]), inline = False)
    await interaction_or_context("SEND", transaction, embed)
