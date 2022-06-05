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


class MessageEvents(Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bulks = {}
        self.test_log = self.bot.get_channel(847066860377342002)

    @Cog.listener()
    async def on_messsage(self, message: Message):
        print(f"Message {message.content} was sent in {message.guild.name}")

    @Cog.listener()
    async def on_message_edit(self, before: Message, after: Message):
        if before.content != after.content:
            await message_events(self.bot, message=after, event="EDIT", original=before)

    @Cog.listener()
    async def on_message_delete(self, message: Message):
        await message_events(self.bot, message=message, event="DELETE")

    @Cog.listener()
    async def on_bulk_message_delete(self, messages: list[Message]):
        pages = []
        history = ""
        data = await self.bot.get_data(messages[0].guild.id)
        channel = messages[0].channel
        cover = Embed(
            title="A bulk message deletion occured.",
            description=f"**{len(messages)}** messages were deleted from {channel.mention} ||`{channel}`||.",
            colour=Colour.dark_red(),
            timestamp=datetime.utcnow(),
        )
        cover.set_footer(text=f"Channel {channel} | {channel.id}.")
        pages.append(cover)
        for message in messages:
            page = Embed(
                title=message.author,
                description=message.content,
                colour=Colour.dark_red(),
                timestamp=message.created_at,
            )
            page.set_footer(text=f"Channel {channel} | {channel.id}.")
            page.set_author(text=f"Message: {message.id}.")
            page.set_thumbnail(url=message.avatar.url)
            pages.append(page)
            if data[2] == True:
                history = (
                    f"[{str(message.created_at.replace(microsecond=0))}]\n"
                    f"Author: {message.author}\n"
                    f"Message: ({message.id}) {message.content}\n\n" + history
                )
        if data[2] == True:
            bulks = self.bulks.get(messages[0].guild.id)
            history = StringIO(history)
            file = File(
                history,
                f"bulk_message_deletion-{bulks}-{channel.name}.txt",
            )

            bulks += 1
            self.bulks[messages[0].guild.id] = bulks

        webhook = Webhook.from_url(data[7], session=self.bot.session)
        await paginate(pages=pages, per_page=1, channel=webhook.channel, type="EMBED")


async def setup(bot):
    await bot.add_cog(MessageEvents(bot))
