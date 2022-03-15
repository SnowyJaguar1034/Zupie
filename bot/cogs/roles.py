from utils.helpers import Roles

from discord import Role, Interaction, Embed, app_commands, Object, TextChannel, VoiceChannel, StageChannel, CategoryChannel
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
    info_description = "Show some information about a role"
    members_description = "Show the members who have this role."
    permissions_description = "Show a role's permission, Defualts to current channel."
    role_param="Defaults to your highest role"

    async def parent(self, ctx):
        group_commands = []
        for subcommand in ctx.command.commands:
            command_string = f"{ctx.prefix + subcommand.qualified_name}"
            group_commands.append(command_string)
        response = await ctx.reply(embed=Embed(title = f"Commands in `{ctx.command.name}`", description = ", ".join(group_commands)), delete_after=30)
        invocation = response.reference.resolved
        await invocation.delete(delay=30)

    @commands.group(name = "role", invoke_without_command = True, case_insensitive = True, aliases = ["rank"])
    async def role_group(self, ctx):
        await self.parent(ctx)

    @role_group.command(name="info", description=info_description, usage = "<role>", aliases = ["whatis", "ri"])
    async def info_legacy(self, ctx, role: Role = None):
        await Roles(self).info_func(ctx, role)

    @slash_role_group.command(name="info", description=info_description)
    @app_commands.describe(role=role_param)
    async def info_slash(self, interaction: Interaction, Role: Role = None, channel: Union[TextChannel, VoiceChannel, StageChannel, CategoryChannel] = None):
        await Roles(self).permissions_func(interaction, role, channel)

    @role_group.command(name="members", description=members_description, usage = "[role]",)
    async def members_legacy(self, ctx, role: Role=None):
        await Roles(self).members_func(ctx, role)

    @slash_role_group.command(name="members", description=members_description)
    @app_commands.describe(role=role_param)
    async def members_slash(self, interaction: Interaction, Role: Role = None, channel: Union[TextChannel, VoiceChannel, StageChannel, CategoryChannel] = None):
        await Roles(self).permissions_func(interaction, role, channel)

    @role_group.command(name="permissions", description = permissions_description, usage = "[role]", aliases = ["perms"])
    async def permissions_legacy(self, ctx, role: Role=None):
        await Roles(self).permissions_func(ctx, role)
    
    @slash_role_group.command(name="permissions", description=permissions_description)
    @app_commands.describe(role=role_param)
    @app_commands.describe(channel="The channel to get permissions for.")
    async def permissions_slash(self, interaction: Interaction, Role: Role = None, channel: Union[TextChannel, VoiceChannel, StageChannel, CategoryChannel] = None):
        await Roles(self).permissions_func(interaction, role, channel)


async def setup(bot):
    await bot.add_cog(role(bot))
    #menus = [info_menu, joined_menu, avatar_menu, roles_menu, status_menu]
    #for menu in menus:
        #bot.tree.add_command(menu, guild=Object(id=default_guild))
    #bot.tree.add_command(permissions_menu)
