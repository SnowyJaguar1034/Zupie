import sys, discord, logging, json, asyncio, os, datetime, config, aiohttp, pathlib, traceback

from utils.services import Zupie
#from cogs.users import user

from discord import Activity, app_commands, Webhook
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

version = os.environ.get('VERSION')
description=os.environ.get('DESCRIPTION')
default_guild = int(os.environ.get('DEFAULT_GUILD'))
default_guild_obj = discord.Object(id=default_guild)

extensions = [
	"cogs.users", 
	]

activity = Activity(name = f"version {version}", type = discord.ActivityType.playing)
bot = Zupie(
    intents=discord.Intents.default(),
    activity=activity,
    owner_ids=["365262543872327681"],
    description=description,
    command_prefix=commands.when_mentioned,
)

@app_commands.command()
@app_commands.guilds(discord.Object(id=default_guild))
async def tree(interaction: discord.Interaction):
    await bot.tree.sync(guild=discord.Object(id=interaction.guild_id))
    await interaction.response.send_message(f'Synced the tree.', ephemeral=True)

bot.tree.add_command(tree)



if __name__ == '__main__':
    try:
        asyncio.run(bot.main())
    except RuntimeError as e:
        print(e)
