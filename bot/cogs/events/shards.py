import asyncio

# from discord.gateway import DiscordClientWebSocketResponse
from datetime import datetime, timedelta
from io import StringIO
from os import environ
from random import choice as rchoice
from typing import Optional

from discord import (
    AuditLogEntry,
    Colour,
    Embed,
    Emoji,
    File,
    Guild,
    GuildSticker,
    Integration,
    Interaction,
    Invite,
    Member,
    Message,
    Object,
    Role,
    ScheduledEvent,
    StageChannel,
    StageInstance,
    TextChannel,
    Thread,
    ThreadMember,
    User,
    VoiceChannel,
    VoiceState,
    Webhook,
)
from discord.abc import GuildChannel
from discord.ext.commands import Cog
from dotenv import load_dotenv
from humanfriendly import format_timespan
from utils.helper_events import (
    guild_events,
    member_events,
    message_events,
    shard_events,
)
from utils.helper_users import timestamps_func
from utils.helpers import send_json, shorten_message, webhook_constructor
from utils.paginator import paginate

# import json
# import logging
# import re
# import io

# import discord
# import psutil


load_dotenv()

# log = logging.getLogger(__name__)

status_webhook = environ.get("STATUS_WEBHOOK")
default_guild = int(environ.get("DEFAULT_GUILD"))
default_guild_obj = Object(id=default_guild)


class ShardEvents(Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bulks = {}
        self.test_log = self.bot.get_channel(847066860377342002)

    @Cog.listener()
    async def on_ready(self):
        await self.bot.tree.sync(guild=Object(id=default_guild))
        print(
            f"Guilds connected to: {len(self.bot.guilds)}",
            f"Running shards: {len(self.bot.shards)}",
            f"Loaded cogs: {len(self.bot.cogs)}",
            "Sucessfully synced applications commands",
            "------",
            sep="\n",
        )

    @Cog.listener()
    async def on_shard_ready(self, shard: int):
        await shard_events(self.bot, shard, "READY")

    @Cog.listener()
    async def on_shard_connect(self, shard: int):
        await shard_events(self.bot, shard, "CONNECT")

    @Cog.listener()
    async def on_shard_disconnect(self, shard: int):
        await shard_events(self.bot, shard, "DISCONNECT")

    @Cog.listener()
    async def on_shard_resumed(self, shard: int):
        await shard_events(self.bot, shard, "RESUME")


async def setup(bot):
    await bot.add_cog(ShardEvents(bot))
