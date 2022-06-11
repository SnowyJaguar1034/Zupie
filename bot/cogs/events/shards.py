"""
BSD 3-Clause License (BSD-3)

Copyright (c) 2022, SnowyJaguar1034(Teagan Collyer)
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this
   list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice,
   this list of conditions and the following disclaimer in the documentation
   and/or other materials provided with the distribution.

3. Neither the name of the copyright holder nor the names of its
   contributors may be used to endorse or promote products derived from
   this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY COPYRIGHT HOLDER "AS IS" AND ANY EXPRESS OR
IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF
MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO
EVENT SHALL COPYRIGHT HOLDER BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS;
OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR
OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF
ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""

import asyncio
# from discord.gateway import DiscordClientWebSocketResponse
from datetime import datetime, timedelta
from io import StringIO
from os import environ
from random import choice as rchoice
from typing import Optional

from discord import (AuditLogEntry, Colour, Embed, Emoji, File, Guild,
                     GuildSticker, Integration, Interaction, Invite, Member,
                     Message, Object, Role, ScheduledEvent, StageChannel,
                     StageInstance, TextChannel, Thread, ThreadMember, User,
                     VoiceChannel, VoiceState, Webhook)
from discord.abc import GuildChannel
from discord.ext.commands import Cog
from dotenv import load_dotenv
from humanfriendly import format_timespan
from utils.helper_events import (guild_events, member_events, message_events,
                                 shard_events)
from utils.helper_users import timestamps_func
from utils.helpers import send_json, shorten_message, webhook_constructor
from utils.paginator import paginate

# import json

# import re
# import io

# import discord
# import psutil


load_dotenv()

from logging import getLogger

log = getLogger(__name__)

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
