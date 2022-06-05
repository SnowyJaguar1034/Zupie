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
