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


class VoiceEvents(Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bulks = {}
        self.test_log = self.bot.get_channel(847066860377342002)

    @Cog.listener()
    async def on_voice_state_update(
        self, member: Member, before: VoiceState, after: VoiceState
    ):
        embed = Embed(timestamp=datetime.utcnow())
        embed.set_author(name=f"{member} | {member.id}", icon_url=member.avatar.url)

        if before.channel is None:  # Member cold joining a VC/Stage
            embed.description = f"{after.channel.mention}"
            embed.colour = Colour.dark_teal()
            embed.set_footer(text=f"Channel ID: {after.channel.id}")
            if isinstance(after.channel, VoiceChannel):
                embed.title = f"{member} joined a voice channel."
            elif isinstance(after.channel, StageChannel):
                embed.title = f"{member} joined a stage channel."

        if after.channel is None:  # Member left a VC/Stage
            embed.description = f"{before.channel.mention}"
            embed.colour = Colour.dark_magenta()
            embed.set_footer(text=f"Channel ID: {before.channel.id}")
            if isinstance(before.channel, VoiceChannel):
                embed.title = f"{member} left a voice channel."
            elif isinstance(before.channel, StageChannel):
                embed.title = f"{member} left a stage channel."

        if (
            before.channel is not None and after.channel is not None
        ):  # Member moved from one VC/Stage to another
            if before.channel.id is not after.channel.id:
                embed.description = (
                    f"{before.channel.mention} -> {after.channel.mention}"
                )
                embed.colour = Colour.dark_blue()
                embed.set_footer(
                    text=f"Channel IDs: {before.channel.id} -> {after.channel.id}"
                )
                if isinstance(before.channel, VoiceChannel) and isinstance(
                    after.channel, VoiceChannel
                ):
                    embed.title = f"{member} moved between voice channels."
                elif isinstance(before.channel, StageChannel) and isinstance(
                    after.channel, StageChannel
                ):
                    embed.title = f"{member} moved between stage channels."
                elif isinstance(before.channel, VoiceChannel) and isinstance(
                    after.channel, StageChannel
                ):
                    embed.title = (
                        f"{member} moved from a voice channel to a stage channel."
                    )
                elif isinstance(before.channel, StageChannel) and isinstance(
                    after.channel, VoiceChannel
                ):
                    embed.title = (
                        f"{member} moved from a stage channel to a voice channel."
                    )
        embed2 = Embed(
            title=f"{member} additional voice state update.",
            timestamp=datetime.utcnow(),
        )
        embed2.set_author(name=f"{member} | {member.id}", icon_url=member.avatar.url)
        embed2.colour = Colour.dark_orange()
        values = []
        message = ""
        values.append(f"{'Mod Unmuted' if after.mute is False else 'Mod Muted'}"),
        values.append(f"{'Mod Undeafened' if after.deaf is False else 'Mod Deafened'}"),
        values.append(
            f"{'Self Unmuted' if after.self_mute is False else 'Self Muted'}",
        )
        values.append(
            f"{'Self Undeafened' if after.self_deaf is False else 'Self Deafened'}"
        ),
        values.append(
            f"{'Not-Streaming' if after.self_stream is False else 'Streaming'}",
        )
        values.append(
            f"{'No Video' if after.self_video is False else 'Video'}",
        )
        values.append(
            f"{'Not Suppressed' if after.suppress is False else 'Suppressed'}",
        )
        if after.requested_to_speak_at:
            embed2.add_field(
                name="Requested to speak at",
                value=f"<t:{int(after.requested_to_speak_at.timestamp())}:R>",
                inline=False,
            )

        for value in values:
            if value is values[0]:
                message = message + value
            else:
                message = message + ", " + value
        embed2.description = message

        self.test_log = self.bot.get_channel(847066860377342002)
        embeds = []

        if embed.title:
            embeds.append(embed)
        if values is not None:
            embeds.append(embed2)
        if embeds:
            await self.test_log.send(embeds=embeds)


async def setup(bot):
    await bot.add_cog(VoiceEvents(bot))
