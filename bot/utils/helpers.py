import discord
from main import bot
from typing import Union
from discord import Member, User, Interaction, Embed, app_commands
from discord.ext.commands import Context

def perm_format(perm):
    return perm.replace("_", " ").replace("guild", "server").title()

def shorten_message(message):
    if len(message) > 2048:
        return message[:2045] + "..."
    else:
        return message


def tag_format(message, member):
    tags = {
        "{username}": member.name,
        "{usertag}": member.discriminator,
        "{userid}": str(member.id),
        "{usermention}": member.mention,
    }
    for tag, val in tags.items():
        message = message.replace(tag, val)
    return shorten_message(message)

def interaction_or_context(arg_type, transaction, object_arg):
    if arg_type == "member":
        if isinstance(transaction, Interaction):
            member = transaction.user if object_arg is None else object_arg
        elif isinstance(transaction, Context):
            member = transaction.author if object_arg is None else object_arg
        else:
            print("Something went wrong in 'member interaction_or_context'")
        return member
    elif arg_type == "channel":
        channel = transaction.channel if object_arg is None else object_arg
        return channel
    else:
        print("The provided arg time is not recognize")

async def timestamps_func(member, embed, avatar):
    embed.add_field(name = "Joined Server:", value = f"<t:{int(member.joined_at.timestamp())}:R>", inline = True)
    if avatar == True:
        embed.add_field(name = "Avatar", value = f"[PNG]({member.avatar.with_static_format('png')})", inline = True)
    embed.add_field(name = "Joined Discord:", value = f"<t:{int(member.created_at.timestamp())}:R>", inline = True)

async def user_info_func(transaction, member_arg):
    member = interaction_or_context("member", transaction, member_arg)
    member_status = "No status" if member.activity is None else member.activity.name

    embed = Embed(title = f"{member}", description = f"Status: **{member.status}**\n*{member_status}*", colour = member.colour)
    embed.set_author(name = f"{member.id}", icon_url = member.avatar.url)
    embed.set_thumbnail(url = member.avatar.url)
    await timestamps_func(member, embed, True)
    roles = [f"{role.mention}" for role in member.roles]
    if len(roles) == 0: roles.append("No roles")
    has_key = [perm for perm in bot.config.key_perms if getattr(member.guild_permissions, perm)]
    if len(has_key) == 0: has_key.append('No permissions')
    embed.add_field(name = f"Roles: {len(roles)}",value = f"{len(roles)} roles" if len(" ".join(roles)) > 1000 else " ".join(roles), inline = False)
    embed.add_field(name =f'Key permissions', value = ", ".join(has_key).replace("_"," ").title(), inline = False)
    if isinstance(transaction, Interaction):
        await transaction.response.send_message(embed=embed)
    elif isinstance(transaction, Context):
        await transaction.reply(embed=embed)
    else:
        print("Something went wrong in 'user_info_func'")

async def user_joined_func(transaction, member_arg):
    member = interaction_or_context("member", transaction, member_arg)    
    embed = Embed(title = f"{member}", colour = member.colour)
    embed.set_author(name = f"{member.id}", icon_url = member.avatar.url)
    embed.set_thumbnail(url = member.avatar.url)
    await timestamps_func(member, embed, False)
    if isinstance(transaction, Interaction):
        await interaction.response.send_message(embed=embed)
    elif isinstance(transaction, Context):
        await interaction.reply(embed=embed)
    else:
        print("Something went wrong in 'user_joined_func'")

async def user_avatar_func(transaction, member_arg):
    member = interaction_or_context("member", transaction, member_arg)
    embed = Embed(title = f"{member}'s Avatar", colour = member.colour)
    embed.add_field(name = "PNG", value = f"[Link]({member.avatar.with_static_format('png')})", inline = True)
    embed.add_field(name = "JPG", value = f"[Link]({member.avatar.with_static_format('jpg')})", inline = True)
    embed.add_field(name = "WebP", value = f"[Link]({member.avatar.with_static_format('webp')})", inline = True)
    embed.set_image(url = member.avatar.url)
    if isinstance(transaction, Interaction):
        await interaction.response.send_message(embed=embed)
    elif isinstance(transaction, Context):
        await interaction.reply(embed=embed)
    else:
        print("Something went wrong in 'user_avatar_func'")

async def user_roles_func(transaction, member_arg):
    member = interaction_or_context("member", transaction, member_arg)
    roles = [f"<@&{role.id}>" for role in member.roles]
    if len(roles) == 0:
        roles.append("No roles")
    embed = Embed(title = f"Roles for {member}: {len(roles)}" if len(" ".join(roles)) > 1000 else " ".join(roles), description = f" ".join(roles))
    if isinstance(transaction, Interaction):
        await interaction.response.send_message(embed=embed)
    elif isinstance(transaction, Context):
        await interaction.reply(embed=embed)
    else:
        print("Something went wrong in 'user_roles_func'")
    
async def user_status_func(transaction, member_arg):
    member = interaction_or_context("member", transaction, member_arg)
    member_status = "No status" if member.activity is None else member.activity.name
    embed = Embed(title = f"{member}", description = f"Status: **{member.status}**\n*{member_status}*", colour = member.colour)
    embed.set_author(name = f"{member.id}", icon_url = member.avatar_url)
    embed.set_thumbnail(url = member.avatar_url)
    if isinstance(transaction, Interaction):
        await interaction.response.send_message(embed=embed)
    elif isinstance(transaction, Context):
        await interaction.reply(embed=embed)
    else:
        print("Something went wrong in 'user_status_func'")    
        
async def user_permissions_func(transaction, member_arg, channel_arg):
    member = interaction_or_context("member", transaction, member_arg)
    channel = transaction.channel if channel_arg is not None else channel_arg
    permissions = channel.permissions_for(member)
    embed = discord.Embed(title="Permission Information", colour = member.colour, description = f"{member} | {member.id}")
    #embed.add_field(name="User", value=str(member), inline=False)
    embed.add_field(name = "Allowed", value = ", ".join([perm_format(name) for name, value in permissions if value]), inline = False)
    embed.add_field(name = "Denied", value=", ".join([perm_format(name) for name, value in permissions if not value]), inline = False)
    if isinstance(transaction, Interaction):
        await interaction.response.send_message(embed=embed)
    elif isinstance(transaction, Context):
        await interaction.reply(embed=embed)
    else:
        print("Something went wrong in 'user_permissions_func'")

def _emoji_counter_(self, guild):
    emoji_stats = Counter()
    for emoji in guild.emojis:
        if emoji.animated:
            emoji_stats['animated'] += 1
            emoji_stats['animated_disabled'] += not emoji.available
        else:
            emoji_stats['regular'] += 1
            emoji_stats['disabled'] += not emoji.available

        fmt = f'Regular: {emoji_stats["regular"]}/{guild.emoji_limit} |     Animated: {emoji_stats["animated"]}/{guild.emoji_limit}'\

        if emoji_stats['disabled'] or emoji_stats['animated_disabled']:
            fmt = f'{fmt} Disabled: {emoji_stats["disabled"]} regular, {emoji_stats["animated_disabled"]} animated\n'

        fmt = f'{fmt} | Total Emojis: {len(guild.emojis)}/{guild.emoji_limit*2}'

    return fmt