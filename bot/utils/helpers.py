from main import bot as bot_var

from typing import Union
from datetime import datetime
from traceback import format_exc

from discord import Member, User, Interaction, Embed, app_commands, Role, TextChannel, VoiceChannel, StageChannel, CategoryChannel, Role, Colour, Object
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

async def parent(ctx):
    group_commands = []
    for subcommand in ctx.command.commands:
        command_string = f"{ctx.prefix + subcommand.qualified_name}"
        group_commands.append(command_string)
    response = await ctx.reply(embed=Embed(title = f"Commands in `{ctx.command.name}`", description = ", ".join(group_commands)), delete_after=30)
    invocation = response.reference.resolved
    await invocation.delete(delay=30)

async def interaction_or_context(arg_type, transaction, object_arg, ephemeral):
    if arg_type == "MEMBER":
        if isinstance(transaction, Interaction):
            member = transaction.user if object_arg is None else object_arg
        elif isinstance(transaction, Context):
            member = transaction.author if object_arg is None else object_arg
        else:
            print("ERROR: interaction_or_context : Hit ele statemnt in 'MEMBER' check")
        return member
    elif arg_type == "ROLE":
        if isinstance(transaction, Interaction):
            #role = object_arg or transaction.user.top_role
            role = transaction.user.top_role if object_arg is None else object_arg
        elif isinstance(transaction, Context):
            #role = object_arg or transaction.user.top_role
            role = transaction.author.top_role if object_arg is None else object_arg
        else:
            print("ERROR: interaction_or_context : Hit ele statemnt in 'ROLE' check")
        return role
    elif arg_type == "SEND":
        if isinstance(object_arg, Embed):
            if isinstance(transaction, Interaction):
                await transaction.response.send_message(embed=object_arg, ephemeral=ephemeral)
            elif isinstance(transaction, Context):
                await transaction.reply(embed=object_arg)
            else:
                print("ERROR: interaction_or_context : Hit ele statemnt in 'SEND.EMBED' check'")
        else:
            if isinstance(transaction, Interaction):
                await transaction.response.send(content=object_arg, ephemeral=ephemeral)
            elif isinstance(transaction, Context):
                await transaction.reply(content=object_arg)
            else:
                print("ERROR: interaction_or_context : Hit ele statemnt in 'SEND.CONTENT' check")
    elif arg_type == "CHANNEL":
        return transaction.channel if object_arg is None else object_arg
    else:
        print("ERROR: interaction_or_context : Hit final eele statemnt")

class Users():
    def __init__(self, bot):
        self.bot = bot

    async def timestamps_func(self, member, embed, avatar):
        embed.add_field(name = "Joined Server:", value = f"<t:{int(member.joined_at.timestamp())}:R>", inline = True)
        if avatar == True:
            embed.add_field(name = "Avatar", value = f"[PNG]({member.avatar.with_static_format('png')})", inline = True)
        embed.add_field(name = "Joined Discord:", value = f"<t:{int(member.created_at.timestamp())}:R>", inline = True)

    async def info_func(self, transaction, member_arg):
        member = await interaction_or_context("MEMBER", transaction, member_arg)
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
        await interaction_or_context("SEND", transaction, embed)

    async def joined_func(self, transaction, member_arg):
        member = await interaction_or_context("MEMBER", transaction, member_arg)    
        embed = Embed(title = f"{member}", colour = member.colour)
        embed.set_author(name = f"{member.id}", icon_url = member.avatar.url)
        embed.set_thumbnail(url = member.avatar.url)
        await self.timestamps_func(member, embed, False)
        await interaction_or_context("SEND", transaction, embed)

    async def avatar_func(self, transaction, member_arg):
        member = await interaction_or_context("MEMBER", transaction, member_arg)
        embed = Embed(title = f"{member}'s Avatar", colour = member.colour)
        embed.add_field(name = "PNG", value = f"[Link]({member.avatar.with_static_format('png')})", inline = True)
        embed.add_field(name = "JPG", value = f"[Link]({member.avatar.with_static_format('jpg')})", inline = True)
        embed.add_field(name = "WebP", value = f"[Link]({member.avatar.with_static_format('webp')})", inline = True)
        embed.set_image(url = member.avatar.url)
        await interaction_or_context("SEND", transaction, embed, True)

    async def roles_func(self, transaction, member_arg):
        member = await interaction_or_context("MEMBER", transaction, member_arg)
        roles = [f"<@&{role.id}>" for role in member.roles]
        if len(roles) == 0:
            roles.append("No roles")
        embed = Embed(title = f"Roles for {member.name}#{member.discriminator}: {len(roles)}", description = "Too many roles to list" if len(" ".join(roles)) > 1000 else " ".join(roles))
        await interaction_or_context("SEND", transaction, embed)
        
    async def status_func(self, transaction, member_arg):
        member = await interaction_or_context("MEMBER", transaction, member_arg)
        member_status = "No status" if member.activity is None else member.activity.name
        embed = Embed(title = f"{member}", description = f"Status: **{member.status}**\n*{member_status}*", colour = member.colour)
        embed.set_author(name = f"{member.id}", icon_url = member.avatar.url)
        embed.set_thumbnail(url = member.avatar.url)
        await interaction_or_context("SEND", transaction, embed) 
            
    async def permissions_func(self, transaction, member_arg, channel_arg):
        member = await interaction_or_context("MEMBER", transaction, member_arg)
        channel = await interaction_or_context("CHANNEL", transaction, channel_arg)
        permissions = channel.permissions_for(member)
        embed = Embed(title=f"Permission Information for {member}", colour = member.colour)
        embed.set_author(name = f"{member} | {member.id}", icon_url = member.avatar.url)
        embed.set_footer(text=f"{channel.name} | {channel.id}")
        embed.add_field(name = "Allowed", value = ", ".join([perm_format(name) for name, value in permissions if value]), inline = False)
        embed.add_field(name = "Denied", value=", ".join([perm_format(name) for name, value in permissions if not value]), inline = False)
        await interaction_or_context("SEND", transaction, embed)

class Roles():
    def __init__(self, bot):
        self.bot = bot

    async def info_func(self, transaction, role_arg):
        role = await interaction_or_context("ROLE", transaction, role_arg)
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
        await interaction_or_context("SEND", transaction, embed)

    async def members_func(self, transaction, role_arg):
        role = await interaction_or_context("ROLE", transaction, role_arg)
        members = [f"{member.mention}, " for member in role.members]
        if len(members) == 0: members.append("No members")
        embed=Embed(title = f"{len(role.members)} Members in `{role}`", description = f" ".join(members))
        await interaction_or_context("SEND", transaction, embed)

    async def permissions_func(self, transaction, role_arg):
        role = await interaction_or_context("ROLE", transaction, role_arg)
        has_perm = [perm[0] for perm in role.permissions if perm[1]]
        if len(has_perm) == 0:
            has_perm.append('No permissions')
        embed=Embed(title = f"Permissions for `{role}`", description = f", ".join(has_perm).replace("_"," ").title())
        await interaction_or_context("SEND", transaction, embed)

class Guilds():
    def __init__(self, bot):
        self.bot = bot

class Emojis():
    def __init__(self, bot):
        self.bot = bot

class Messages():
    def __init__(self, bot):
        self.bot = bot

class Owners():
    def __init__(self, bot):
        self.bot = bot

    async def cog(self, task, transaction, cog):
        embed = Embed(timestamp=datetime.now())
        ephemeral = None
        try:
            if task == "LOAD":
                await bot_var.load_extension(cog)
                embed.color=(Colour.green())
            elif task == "UNLOAD":
                await bot_var.unload_extension(cog)
                embed.color=(Colour.orange())
            elif task == "RELOAD":
                await bot_var.reload_extension(cog)
                embed.color=(Colour.gold())
            embed.title=(f"__Cog {task.title()}ed__")
            embed.description=(f"{cog.split('.')[1].title()} has been {task.lower()}ed.")
            ephemeral = False
        except Exception as e:
            embed.title=(f"__{task.title()} Error__")
            embed.description=(f"There was an error trying to {task.lower()} `{cog.split('.')[1].title()}`")
            embed.color=(Colour.red())
            embed.add_field(name="Traceback", value=f"```py\n{format_exc()}```")
            ephemeral=True
        embed.set_footer(text=f"{transaction.user}", icon_url=transaction.user.display_avatar.url)
        await interaction_or_context("SEND", transaction, embed, ephemeral)

    async def cog_error(self, transaction, cog, task):
        embed = Embed(timestamp=datetime.now())
        embed.title=(f"__{task.title()} Error__")
        embed.description=(f"There was an error trying to {task.lower()} `{cog.split('.')[1].title()}`")
        embed.color=(Colour.red())
        embed.add_field(name="Traceback", value=f"```py\n{format_exc()}```")
        ephemeral=True
        embed.set_footer(text=f"{transaction.user}", icon_url=transaction.user.display_avatar.url)
        await interaction_or_context("SEND", transaction, embed, ephemeral)

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