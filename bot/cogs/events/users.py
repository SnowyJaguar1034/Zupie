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


class UserEvents(Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bulks = {}
        self.test_log = self.bot.get_channel(847066860377342002)

    @Cog.listener()
    async def on_member_join(self, member: Member):
        await member_events(self.bot, member, "JOIN")

    @Cog.listener()
    async def on_member_remove(self, member: Member):
        await member_events(self.bot, member, "LEAVE")

    @Cog.listener()
    async def on_member_update(self, before: Member, after: Member):
        print(f"Member {before.name} was updated in {before.guild.name}")

    @Cog.listener()
    async def on_user_update(self, before: User, after: User):
        print(f"User {before.name} was updated in {before.guild.name}")

    @Cog.listener()
    async def on_presence_update(self, before: Member, after: Member):
        print(f"{before.name}'s presence was updated in {before.guild.name}")

    @Cog.listener()
    async def on_member_ban(self, guild: Guild, user: User):
        print(f"{user.name} was banned from {guild.name}")

    @Cog.listener()
    async def on_member_unban(self, guild: Guild, user: User):
        print(f"{user.name} was unbanned from {guild.name}")


async def setup(bot):
    await bot.add_cog(UserEvents(bot))
