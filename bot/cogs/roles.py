from utils.helpers import Roles

from discord import Member, User, Interaction, Embed, app_commands, Object, TextChannel, VoiceChannel, StageChannel, CategoryChannel, Role
from discord.ext import commands

from typing import Union
from os import environ
from dotenv import load_dotenv
#from main import bot

load_dotenv()

default_guild = int(environ.get('DEFAULT_GUILD'))
    
class role(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    slash_role_group = app_commands.Group(name="roles", description="Check Role stuff.", guild_ids=[default_guild])
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
        response = await ctx.reply(embed=Embed(title = f"Commands in `{ctx.command.name}`", description = ", ".join(group_commands)), delete_after=30)
        invocation = response.reference.resolved
        await invocation.delete(delay=30)

    @commands.group(name = "role", invoke_without_command = True, case_insensitive = True, aliases = ["rank"])
    async def role_group(self, ctx):
        await self.parent(ctx)

    @role_group.command(name="info", description = "Show information about the given role.", usage = "<role>", aliases = ["whatis", "ri"])
    async def info_legacy(self, ctx, role: Role = None):
        await Roles(self).info_func(ctx, role)

    @role_group.command(name="members", description = "Show the members of the role specified.", usage = "[role]",)
    async def members_legacy(self, ctx, role: Role=None):
        await Roles(self).members_func(ctx, role)

    @role_group.command(name="permissions", description = "Show the members of the role specified.", usage = "[role]", aliases = ["perms"])
    async def permissions_legacy(self, ctx, role: Role=None):
        await Roles(self).permissions_func(ctx, role)
    '''
    @slash_user_group.command(name="permissions", description=permissions_description)
    @app_commands.describe(member="The discord member to get information for.")
    @app_commands.describe(channel="The channel to get permissions for.")
    async def permissions_slash(self, interaction: Interaction, member: Member = None, channel: Union[TextChannel, VoiceChannel, StageChannel, CategoryChannel] = None):
        await user_permissions_func(interaction, member, channel)
    '''

async def setup(bot):
    await bot.add_cog(role(bot))
    #menus = [info_menu, joined_menu, avatar_menu, roles_menu, status_menu]
    #for menu in menus:
        #bot.tree.add_command(menu, guild=Object(id=default_guild))
    #bot.tree.add_command(permissions_menu)
