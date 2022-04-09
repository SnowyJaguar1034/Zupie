import logging, asyncio, config, traceback

# Custom Imports
from classes.zupie import Zupie

# Package Imports
from discord import Activity, ActivityType, Intents
from discord.ext import commands

# Bulit in Imports
from os import environ
from dotenv import load_dotenv

load_dotenv()

intents = Intents.default()
intents.message_content = True

bot = Zupie(
    intents=intents,
    activity=Activity(
        name=f"version {environ.get('VERSION')}", type=ActivityType.playing
    ),
    owner_ids=config.backend["Owners"],
    description=environ.get("DESCRIPTION"),
    command_prefix=commands.when_mentioned,
    case_insensitive=True,
)

if __name__ == "__main__":
    try:
        asyncio.run(bot.main())
    except RuntimeError:
        print(traceback.format_exc())
