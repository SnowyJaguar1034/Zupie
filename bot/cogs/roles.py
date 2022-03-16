from utils.helpers import Roles, parent

from discord import Role, Interaction, Embed, app_commands, Object, TextChannel, VoiceChannel, StageChannel, CategoryChannel
from discord.ext import commands

from typing import Union
from os import environ
from dotenv import load_dotenv
#from main import bot

load_dotenv()

default_guild = int(environ.get('DEFAULT_GUILD'))
    
class Role_Cog(app_commands.Group, commands.Cog, name="role", description="Shows all role related commands, legacy and slash"):
    def __init__(self, bot):
        super().__init__()
        self.bot = bot

    edit_role = app_commands.Group(name="edit", description="edit Role stuff.", guild_ids=[default_guild])
    info_description = "Show some information about a role"
    members_description = "Show the members who have this role."
    permissions_description = "Show a role's permission, Defualts to current channel."
    role_param="Defaults to your highest role"

    @commands.group(name = "role", invoke_without_command = True, case_insensitive = True, aliases = ["rank"])
    async def role_group(self, ctx):
        await parent(ctx)

    @role_group.command(name="info", description=info_description, usage = "<role>", aliases = ["whatis", "ri"])
    async def info_legacy(self, ctx, role: Role = None):
        await Roles(self).info_func(ctx, role)

    @app_commands.command(name="info", description=info_description)
    @app_commands.describe(role=role_param)
    async def info_slash(self, interaction: Interaction, role: Role = None, channel: Union[TextChannel, VoiceChannel, StageChannel, CategoryChannel] = None):
        await Roles(self).permissions_func(interaction, role, channel)

    @role_group.command(name="members", description=members_description, usage = "[role]",)
    async def members_legacy(self, ctx, role: Role=None):
        await Roles(self).members_func(ctx, role)

    @app_commands.command(name="members", description=members_description)
    @app_commands.describe(role=role_param)
    async def members_slash(self, interaction: Interaction, role: Role = None, channel: Union[TextChannel, VoiceChannel, StageChannel, CategoryChannel] = None):
        await Roles(self).permissions_func(interaction, role, channel)

    @role_group.command(name="permissions", description = permissions_description, usage = "[role]", aliases = ["perms"])
    async def permissions_legacy(self, ctx, role: Role=None):
        await Roles(self).permissions_func(ctx, role)

    @app_commands.command(name="permissions", description=permissions_description)
    @app_commands.describe(role=role_param)
    @app_commands.describe(channel="The channel to get permissions for.")
    async def permissions_slash(self, interaction: Interaction, role: Role = None, channel: Union[TextChannel, VoiceChannel, StageChannel, CategoryChannel] = None):
        await Roles(self).permissions_func(interaction, role, channel)

    @role_group.group(name="edit", description = permissions_description)
    async def edit_legacy(self, ctx, role: Role=None):
         await parent(ctx)

    @edit_legacy.command(name="name")
    async def edit_name_legacy(self, interaction: Interaction, role: Role = None, *, name=str):
        print("'edit_name_legacy' print out")

    @edit_role.command(name="name")
    @app_commands.describe(role=role_param)
    @app_commands.describe(name="The name you want the role to have")
    async def edit_name_slash(self, interaction: Interaction, role: Role = None, *, name: str):
        print("edit_name_slash print out")



async def setup(bot):
    await bot.add_cog(Role_Cog(bot), guild=Object(id=default_guild))