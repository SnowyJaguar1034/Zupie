import asyncio
import logging
import traceback

# Bulit in Imports
from os import environ

# Package Imports
from discord import Activity, ActivityType, Intents
from discord.ext import commands
from dotenv import load_dotenv

import config

# Custom Imports
from classes.zupie import Zupie

load_dotenv()

intents = Intents.all()
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
    asyncio.run(bot.main())
