from utils.helpers import Users, parent

from discord import Member, User, Interaction, Embed, app_commands, Object, TextChannel, VoiceChannel, StageChannel, CategoryChannel, Colour, Embed
from discord.ext import commands

from typing import Union
from datetime import datetime
from os import environ
from traceback import format_exc
from dotenv import load_dotenv
#from main import bot

load_dotenv()

default_guild = int(environ.get('DEFAULT_GUILD'))
    
class Owner_Cog(app_commands.Group, commands.Cog, name="owner", description="Shows all owner related commands"):
    def __init__(self, bot):
        super().__init__()
        self.bot = bot

    @app_commands.command(name="sync tree", description="Syncs the slash command tree")
    @app_commands.guilds(Object(id=default_guild))
    async def tree(interaction: Interaction):
        try:
            await self.bot.tree.sync(guild=discord.Object(id=interaction.guild_id))
        except Exception as e:
            print(f"\Failed to sync tree:\n{format_exc()}\n")
        await interaction.response.send_message(f'Synced the tree.', ephemeral=True)

    cogs_group = app_commands.Group(name="cog", description="work with cogs", guild_ids=[default_guild])
    info_description = "Show some information about yourself or the member specified."
    joined_description = "Show when yourself or the member specified joined this server and Discord."
    avatar_description = "Show a users avatar."
    roles_description = "Show a users roles."
    status_description = "Show a users status."
    permissions_description = "Show a member's permission, Defualts to current channel."

    @cogs_group.command(name="load", description="loads a cog")
    @app_commands.describe(cog="the cog to load.")
    @app_commands.choices(cogs=[Choice(name=cog.split('.')[1].title(),value=cog) for cog in self.bot.initial_extensions])
    async def load_slash(self, interaction: Interaction, cog: str):
        embed = Embed(timestamp=datetime.datetime.now())
        try:
            await self.bot.load_extension(cog)
            embed.title=("__Cog Loaded__")
            embed.description=(f"{cog} has been Loaded.")
            embed.color=(Colour.green())
        except Exception as e:
            embed.title=("__Load Error__")
            embed.description=(f"There was an error trying to load *{cog}*")
            embed.color=(Colour.red())
            embed.add_field(name="Traceback", description=format_exc)
        embed.set_footer(text=f"{interaction.user}", icon_url=interaction.user.display_avatar.url)
        await interaction.response.send_message(embed= embed, ephemeral=True)			
    

async def setup(bot):
    await bot.add_cog(Owner_Cog(bot), guild=Object(id=default_guild))

'''
initial_extensions = ["cogs.help","cogs.events","cogs.users","cogs.roles"]
cogs = []
for entry in initial_extensions:
    cog = entry.strip('"').split('.')[1]
    Choice(name=cog.title(), value=entry),
    cogs.append(choice)
print(cogs)
cogs = [cog.strip('"').split('.')[1] for cog in initial_extensions]
cogs = [Choice(name=cog.split('.')[1].title(),value=cog) for cog in self.bot.initial_extensions]
initial_extensions = ["cogs.help","cogs.events","cogs.users","cogs.roles"]
print(cogs = [Choice(name=cog.split('.')[1].title(),value=cog) for cogin initial_extensions])
'''