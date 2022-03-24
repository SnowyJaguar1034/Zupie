import sys, discord, logging, json, asyncio, os, datetime, config, aiohttp, pathlib, traceback

from classes.bot_subclass import Zupie
#from cogs.users import user

from discord import Activity, app_commands, Webhook
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

version = os.environ.get('VERSION')
description=os.environ.get('DESCRIPTION')

activity = Activity(name = f"version {version}", type = discord.ActivityType.playing)
bot = Zupie(
    intents=discord.Intents.default(),
    activity=activity,
    owner_ids=["365262543872327681"],
    description=description,
    command_prefix=commands.when_mentioned,
    case_insensitive = True
)

#bot.tree.add_command(tree)

if __name__ == '__main__':
    try:
        asyncio.run(bot.main())
    except RuntimeError:
        print(traceback.format_exc())
