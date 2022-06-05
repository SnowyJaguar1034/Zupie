import asyncio
import logging
import traceback
# Bulit in Imports
from os import environ

# Package Imports
from discord import Activity, ActivityType, Intents
from discord.ext import commands
from dotenv import load_dotenv

from classes.config import Config
# Custom Imports
from classes.zupie import Zupie
from configuration import activity, backend

load_dotenv()

intents = Intents.all()
intents.message_content = True

bot = Zupie(
    intents=intents,
    activity=Activity(name=activity, type=ActivityType.playing),
    owner_ids=backend["Owners"],
    description=Config().DESCRIPTION,
    command_prefix=commands.when_mentioned,
    case_insensitive=True,
)

if __name__ == "__main__":
    asyncio.run(bot.main())
