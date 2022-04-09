# import asyncio
# import json
# import logging
# import re
# import io

# import discord
# import psutil

from utils.helper_events import (
    guild_events,
    member_events,
    shard_events,
    message_events,
)
from utils.helpers import send_json
from utils.helper_users import timestamps_func
from utils.paginator import paginate
from discord import (
    Webhook,
    Embed,
    Colour,
    Object,
    Guild,
    Member,
    Forbidden,
    Message,
    File,
)
from discord.ext.commands import Cog

# from discord.gateway import DiscordClientWebSocketResponse
from datetime import datetime, timedelta
from typing import Optional
from random import choice as rchoice
from os import environ
from io import StringIO
from dotenv import load_dotenv

load_dotenv()

# log = logging.getLogger(__name__)

status_webhook = environ.get("STATUS_WEBHOOK")
default_guild = int(environ.get("DEFAULT_GUILD"))
default_guild_obj = Object(id=default_guild)


class Events_Cog(Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bulks = {}

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

    @Cog.listener()
    async def on_guild_join(self, guild: Guild):
        await guild_events(self.bot, guild, "JOIN")

    @Cog.listener()
    async def on_guild_remove(self, guild: Guild):
        await guild_events(self.bot, guild, "LEAVE")

    @Cog.listener()
    async def on_member_join(self, member: Member):
        await member_events(self.bot, member, "JOIN")

    @Cog.listener()
    async def on_member_remove(self, member: Member):
        await member_events(self.bot, member, "LEAVE")

    @Cog.listener()
    async def on_message_edit(self, before: Message, after: Message):
        if before.content != after.content:
            await message_events(self.bot, message=after, event="EDIT", orginal=before)

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
    await bot.add_cog(Events_Cog(bot))
