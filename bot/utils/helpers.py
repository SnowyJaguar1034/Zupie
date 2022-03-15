import discord
from main import bot as bot_var
from typing import Union
from discord import Member, User, Interaction, Embed, app_commands, Role, TextChannel, VoiceChannel, StageChannel, CategoryChannel
from discord.ext.commands import Context

def perm_format(perm):
    return perm.replace("_", " ").replace("guild", "server").title()

def shorten_message(message):
    if len(message) > 2048:
        return message[:2045] + "..."
    else:
        return message

def user_tag_format(message, member):
    tags = {
        "{user_name}": member.name,
        "{user_tag}": member.discriminator,
        "{user_id}": str(member.id),
        "{user_mention}": member.mention,
    }
    for tag, val in tags.items():
        message = message.replace(tag, val)
    return shorten_message(message)

def channel_tag_format(message, channel):
    tags = {
        "{channel_name}": channel.name,
        "{channel_id}": str(channel.id),
        "{channel_mention}": channel.mention,
    }
    for tag, val in tags.items():
        message = message.replace(tag, val)
    return shorten_message(message)

def guild_tag_format(message, guild):
    tags = {
        "{guild_name}": guild.name,
        "{guild_id}": str(guild.id),
    }
    for tag, val in tags.items():
        message = message.replace(tag, val)
    return shorten_message(message)

async def interaction_or_context(transaction, object_arg):
    if isinstance(object_arg, (Member, User)): # == "MEMBER"
        if isinstance(transaction, Interaction):
            member = transaction.user if object_arg is None else object_arg
        elif isinstance(transaction, Context):
            member = transaction.author if object_arg is None else object_arg
        else:
            print("Something went wrong in 'member interaction_or_context'")
        return member
    elif isinstance(object_arg, Role): # == "ROLE"
        if isinstance(transaction, Interaction):
            role = object_arg or transaction.user.top_role
            #role = transaction.user.top_role if object_arg is None else object_arg
        elif isinstance(transaction, Context):
            role = object_arg or transaction.user.top_role
            #role = transaction.author.top_role if object_arg is None else object_arg
        else:
            print("Something went wrong in 'member interaction_or_context'")
        return role
    elif isinstance(object_arg, Embed): # == "SEND"
        if isinstance(transaction, Interaction):
            await transaction.response.send(embed=object_arg)
        elif isinstance(transaction, Context):
            await transaction.reply(embed=object_arg)
        else:
            print("Something went wrong in 'user_roles_func'")
    elif isinstance(object_arg, (TextChannel, VoiceChannel, StageChannel, CategoryChannel)): # == "channel"
        channel = transaction.channel if object_arg is None else object_arg
        return channel
    else:
        print("The provided arg time is not recognize")

class Users():
    def __init__(self, bot):
        #pass
        self.bot = bot

    async def timestamps_func(self, member, embed, avatar):
        embed.add_field(name = "Joined Server:", value = f"<t:{int(member.joined_at.timestamp())}:R>", inline = True)
        if avatar == True:
            embed.add_field(name = "Avatar", value = f"[PNG]({member.avatar.with_static_format('png')})", inline = True)
        embed.add_field(name = "Joined Discord:", value = f"<t:{int(member.created_at.timestamp())}:R>", inline = True)

    async def info_func(self, transaction, member_arg):
        member = await interaction_or_context(transaction, member_arg)
        member_status = "No status" if member.activity is None else member.activity.name

        embed = Embed(title = f"{member}", description = f"Status: **{member.status}**\n*{member_status}*", colour = member.colour)
        embed.set_author(name = f"{member.id}", icon_url = member.avatar.url)
        embed.set_thumbnail(url = member.avatar.url)
        await self.timestamps_func(member, embed, True)
        roles = [f"{role.mention}" for role in member.roles]
        if len(roles) == 0: roles.append("No roles")
        has_key = [perm for perm in bot_var.config.key_perms if getattr(member.guild_permissions, perm)]
        if len(has_key) == 0: has_key.append('No permissions')
        embed.add_field(name = f"Roles: {len(roles)}",value = f"{len(roles)} roles" if len(" ".join(roles)) > 1000 else " ".join(roles), inline = False)
        embed.add_field(name =f'Key permissions', value = ", ".join(has_key).replace("_"," ").title(), inline = False)
        await interaction_or_context(transaction, embed)

    async def joined_func(self, transaction, member_arg):
        member = await interaction_or_context(transaction, member_arg)    
        embed = Embed(title = f"{member}", colour = member.colour)
        embed.set_author(name = f"{member.id}", icon_url = member.avatar.url)
        embed.set_thumbnail(url = member.avatar.url)
        await self.timestamps_func(member, embed, False)
        await interaction_or_context(transaction, embed)

    async def avatar_func(self, transaction, member_arg):
        member = await interaction_or_context(transaction, member_arg)
        embed = Embed(title = f"{member}'s Avatar", colour = member.colour)
        embed.add_field(name = "PNG", value = f"[Link]({member.avatar.with_static_format('png')})", inline = True)
        embed.add_field(name = "JPG", value = f"[Link]({member.avatar.with_static_format('jpg')})", inline = True)
        embed.add_field(name = "WebP", value = f"[Link]({member.avatar.with_static_format('webp')})", inline = True)
        embed.set_image(url = member.avatar.url)
        await interaction_or_context(transaction, embed)

    async def roles_func(self, transaction, member_arg):
        member = await interaction_or_context(transaction, member_arg)
        roles = [f"<@&{role.id}>" for role in member.roles]
        if len(roles) == 0:
            roles.append("No roles")
        embed = Embed(title = f"Roles for {member.name}#{member.discriminator}: {len(roles)}", description = "Too many roles to list" if len(" ".join(roles)) > 1000 else " ".join(roles))
        await interaction_or_context(transaction, embed)
        
    async def status_func(self, transaction, member_arg):
        member = await interaction_or_context(transaction, member_arg)
        member_status = "No status" if member.activity is None else member.activity.name
        embed = Embed(title = f"{member}", description = f"Status: **{member.status}**\n*{member_status}*", colour = member.colour)
        embed.set_author(name = f"{member.id}", icon_url = member.avatar.url)
        embed.set_thumbnail(url = member.avatar.url)
        await interaction_or_context(transaction, embed) 
            
    async def permissions_func(self, transaction, member_arg, channel_arg):
        member = await interaction_or_context(transaction, member_arg)
        channel = await interaction_or_context(transaction, channel_arg)
        permissions = channel.permissions_for(member)
        embed = discord.Embed(title=f"Permission Information for {member}", colour = member.colour)
        embed.set_author(name = f"{member} | {member.id}", icon_url = member.avatar.url)
        embed.set_footer(text=f"{channel.name} | {channel.id}")
        embed.add_field(name = "Allowed", value = ", ".join([perm_format(name) for name, value in permissions if value]), inline = False)
        embed.add_field(name = "Denied", value=", ".join([perm_format(name) for name, value in permissions if not value]), inline = False)
        await interaction_or_context(transaction, embed)

class Roles():
    def __init__(self, bot):
        #pass
        self.bot = bot

    async def info_func(self, transaction, role_arg):
        role = await interaction_or_context(transaction, role_arg)
        has_perm = [perm for perm in bot_var.config.guild_perms if getattr(role.permissions, perm)]

        embed = Embed(title = f"{role.name}", description = f"{role.mention} was created <t:{int(role.created_at.timestamp())}:R>", color = role.colour)
        embed.set_author(name = f"ID: {role.id}")
        embed.add_field(name = "Members in role:", value = len(role.members), inline = True)
        embed.add_field(name = "Position", value = role.position, inline = True)
        embed.add_field(name = "Colour:", value = role.colour, inline = True)
        embed.add_field(name = "Hoisted:", value = role.hoist, inline = True)
        embed.add_field(name = "Mentionable:", value = role.mentionable, inline = True)
        embed.add_field(name = "Intergration:", value = role.managed, inline = True)   
        embed.add_field(name = f'Permissions', value = ", ".join([perm_format(name) for name, value in has_perm if not value]), inline = False)
        await interaction_or_context(transaction, embed)

    async def members_func(self, transaction, role_arg):
        role = await interaction_or_context(transaction, role_arg)
        members = [f"{member.mention}, " for member in role.members]
        if len(members) == 0: members.append("No members")
        embed=Embed(title = f"{len(role.members)} Members in `{role}`", description = f" ".join(members))
        await interaction_or_context(transaction, embed)

    async def permissions_func(self, transaction, role_arg):
        role = await interaction_or_context(transaction, role_arg)
        has_perm = [perm[0] for perm in role.permissions if perm[1]]
        if len(has_perm) == 0:
            has_perm.append('No permissions')
        embed=Embed(title = f"Permissions for `{role}`", description = f", ".join(has_perm).replace("_"," ").title())
        await interaction_or_context(transaction, embed)

class Guilds():
    def __init__(self, bot):
        self.bot = bot

class Emojis():
    def __init__(self, bot):
        self.bot = bot

class Messages():
    def __init__(self, bot):
        self.bot = bot

def _emoji_counter_(guild):
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