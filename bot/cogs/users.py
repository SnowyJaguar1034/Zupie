import discord, os
from utils.helpers import interaction_or_context,user_info_func, user_joined_func, user_avatar_func, user_roles_func, user_status_func, user_permissions_func
from typing import Union
from discord import Member, User, Interaction, Embed, app_commands
from discord.ext import commands
from dotenv import load_dotenv
from main import bot

load_dotenv()

default_guild = int(os.environ.get('DEFAULT_GUILD'))
    
class user(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    slash_user_group = app_commands.Group(name="users", description="Check User stuff.", guild_ids=[default_guild])
    info_description = "Show some information about yourself or the member specified."
    joined_description = "Show when yourself or the member specified joined this server and Discord."
    avatar_description = "Show a users avatar."
    roles_description = "Show a users roles."
    status_description = "Show a users status."
    permissions_description = "Show a member's permission, Defualts to current channel."

    async def parent(self, ctx):
        group_commands = []
        for subcommand in ctx.command.commands:
            command_string = f"{ctx.prefix + ctx.command.name + ' ' + subcommand.name}"
            group_commands.append(command_string)
        response = await ctx.reply(embed=discord.Embed(title = f"Commands in `{ctx.command.name}`", description = ", ".join(group_commands)), delete_after=30)
        invocation = response.reference.resolved
        await invocation.delete(delay=30)

    @commands.group(name = "user", aliases = ["member"], invoke_without_command = True, case_insensitive = True,)
    async def legacy_user_group(self, ctx):
       await self.parent(ctx)

    @legacy_user_group.command(name ="info", description=info_description, usage="[member]", aliases=["whois", "ui"])
    async def info_legacy(self, ctx: commands.Context, member: discord.Member = None):
        #member2 = interaction_or_context(ctx, member)
        await user_info_func(ctx, member)

    @slash_user_group.command(name="info", description=info_description)
    @app_commands.describe(member="The discord member to get information for.")
    async def info_slash(self, interaction: Interaction, member: Union[Member, User]=None):
        #member2 = interaction_or_context(interaction, member)
        await user_info_func(interaction, member)

    @legacy_user_group.command(name="joined", description = joined_description, usage="[member]", aliases=["dates", "created", "j"])
    async def joined_legacy(self, ctx, member: discord.Member = None):
        await user_joined_func(ctx, member)

    @slash_user_group.command(name="joined", description=joined_description)
    @app_commands.describe(member="The discord member to get information for.")
    async def joined_slash(self, interaction: Interaction, member: discord.Member=None):
        await user_joined_func(interaction, member)

    @legacy_user_group.command(name="avatar", description=avatar_description, usage="[member]", aliases=["av"])
    async def avatar_legacy(self, ctx, member: discord.Member = None):
        await user_avatar_func(ctx, member)

    @slash_user_group.command(name="avatar", description=avatar_description)
    @app_commands.describe(member="The discord member to get information for.")
    async def avatar_slash(self, interaction: Interaction, member: discord.Member = None):
        await user_avatar_func(interaction, member)

    @legacy_user_group.command(name="roles", description =roles_description, usage="[member]")
    async def roles_legacy(self, ctx, member: discord.Member = None):
        await user_roles_func(ctx, member)

    @slash_user_group.command(name="roles", description=roles_description)
    @app_commands.describe(member="The discord member to get information for.")
    async def roles_slash(self, interaction: Interaction, member: discord.Member = None):
        await user_roles_func(interaction, member)

    @legacy_user_group.command(name="status", description=status_description, usage = "[member]")
    async def status_legacy(self, ctx, member: discord.Member = None):
        await user_status_func(ctx, member)

    @slash_user_group.command(name="status", description=status_description)
    @app_commands.describe(member="The discord member to get information for.")
    async def status_slash(self, interaction: Interaction, member: discord.Member = None):
        await user_status_func(interaction, member)

    @legacy_user_group.command(name="permissions", description=permissions_description, usage = "[member] [channel]")
    async def permissions_legacy(self, ctx, member: discord.Member = None, channel: Union[discord.TextChannel, discord.VoiceChannel, discord.StageChannel, discord.CategoryChannel] = None):
        await user_permissions_func(ctx, member)

    @slash_user_group.command(name="permissions", description=permissions_description)
    @app_commands.describe(member="The discord member to get information for.")
    @app_commands.describe(channel="The channel to get permissions for.")
    async def permissions_slash(self, interaction: Interaction, member: discord.Member = None, channel: Union[discord.TextChannel, discord.VoiceChannel, discord.StageChannel, discord.CategoryChannel] = None):
        await user_permissions_func(interaction, member, channel)

        
    ''' @commands.guild_only()
    @commands.has_permissions(manage_guild = True)
    @legacy_user_group.command(name="permissions", description = "Show a member's permission in a channel when specified.", usage = "[member] [channel]", aliases = ["perms"])
    async def permissions_legacy(self, ctx, member: discord.Member = None, channel: Union[discord.TextChannel, discord.VoiceChannel, discord.StageChannel, discord.CategoryChannel] = None):
        channel = channel or ctx.channel
        member = member or ctx.author
        permissions = channel.permissions_for(member)
        embed = discord.Embed(title="Permission Information", colour = member.colour)
        embed.add_field(name="User", value=str(member), inline=False)
        embed.add_field(name = "Allowed", value = ", ".join([self.bot.tools.perm_format(name) for name, value in permissions if value]), inline = False)
        embed.add_field(name = "Denied", value=", ".join([self.bot.tools.perm_format(name) for name, value in permissions if not value]), inline = False)
        await ctx.reply(embed=embed) '''

@app_commands.context_menu(name="User Info")
async def info_menu(interaction: Interaction, member: Member):
    await user_info_func(interaction, member)

@app_commands.context_menu(name="User Joined\Created")
async def joined_menu(interaction: Interaction, member: Member):
    await user_joined_func(interaction, member)

@app_commands.context_menu(name="User Avatar")
async def avatar_menu(interaction: Interaction, member: Member):
    await user_avatar_func(interaction, member)

@app_commands.context_menu(name="User Roles")
async def roles_menu(interaction: Interaction, member: Member):
    await user_roles_func(interaction, member)

@app_commands.context_menu(name="User Status")
async def status_menu(interaction: Interaction, member: Member):
    await user_status_func(interaction, member)

@app_commands.context_menu(name="User Permissions")
async def permissions_menu(interaction: Interaction, member: Member):
    await user_status_func(interaction, member)
    

def setup(bot):
    bot.add_cog(user(bot))
    menus = [info_menu, joined_menu, avatar_menu, roles_menu, status_menu, permissions_menu]
    for menu in menus:
        bot.tree.add_command(menu, guild=discord.Object(id=default_guild))
    bot.tree.add_command(permissions_menu))

    ''' 
    bot.tree.add_command(info_menu, guild=discord.Object(id=default_guild))
    bot.tree.add_command(joined_menu, guild=discord.Object(id=default_guild))
    bot.tree.add_command(avatar_menu, guild=discord.Object(id=default_guild))
    bot.tree.add_command(roles_menu, guild=discord.Object(id=default_guild))
    bot.tree.add_command(status_menu, guild=discord.Object(id=default_guild))
    '''