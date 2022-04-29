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


class Events_Cog(Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bulks = {}
        self.test_log = self.bot.get_channel(847066860377342002)

    # ------------------------------------------------- Bot Events ----------------------------------------------- #

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

    # ------------------------------------------------------------------------------------------------------------ #

    # ----------------------------------------------- Guild Events ----------------------------------------------- #

    @Cog.listener()
    async def on_guild_join(self, guild: Guild):
        await guild_events(self.bot, guild, "JOIN")

    @Cog.listener()
    async def on_guild_remove(self, guild: Guild):
        await guild_events(self.bot, guild, "LEAVE")

    @Cog.listener()
    async def on_guild_update(self, before: Guild, after: Guild):
        async def channel_check(self, before, after):
            if before or after:
                if before is not None and after is not None:
                    if before.id != after.id:
                        return f"{before.mention} -> {after.mention}"
                elif before is not None and after is None:
                    return f"{before.mention} -> None"
                elif before is None and after is not None:
                    return f"None -> {after.mention}"

        async def description_check(self, before, after):
            description = []
            if before.strip():
                description.append(f"Old description: {before}")
            if after.strip():
                description.append(f"New description: {after}")
            description = "\n".join(description)

            description = shorten_message(message=description, max_length=1024)

            return description

        embed = Embed(
            title="Guild updated",
        )
        if "COMMUNITY" in before.features or "COMMUNITY" in after.features:
            embed.description = (
                await description_check(
                    self, before=before.description, after=after.description
                ),
            )
        embed.set_thumbnail(url=before.icon.url)
        if after.banner is not None:
            embed.set_image(url=after.banner.url)
        elif after.banner is None and before.banner is not None:
            embed.set_image(url=before.banner.url)
        elif after.banner is None and before.banner is None:
            embed.set_image(url=after.icon.url)
        if before.owner is not after.owner:
            embed.set_author(
                name=f"{before.owner} -> {after.owner}",
                icon_url=after.owner.display_avatar.url,
            )
            embed.set_footer(text=f"Owner ID: {before.owner.id} -> {after.owner.id}")
        else:
            embed.set_author(
                name=f"{before.owner}",
                icon_url=after.owner.display_avatar.url,
            )
            embed.set_footer(text=f"Owner ID: {before.owner.id}")

        if before.afk_channel or after.afk_channel:
            embed.add_field(
                name="AFK Channel",
                value=await channel_check(
                    self, before=before.afk_channel, after=after.afk_channel
                ),
            )

        if before.system_channel or after.system_channel:
            embed.add_field(
                name="System channel",
                value=await channel_check(
                    self, before.system_channel, after.system_channel
                ),
            )
        if before.public_updates_channel or after.public_updates_channel:
            embed.add_field(
                name="Public updates channel",
                value=await channel_check(
                    self,
                    before=before.public_updates_channel,
                    after=after.public_updates_channel,
                ),
            )
        if before.rules_channel or after.rules_channel:
            embed.add_field(
                name="Rules channel",
                value=await channel_check(
                    self, before=before.rules_channel, after=after.rules_channel
                ),
            )

        if before.afk_timeout or after.afk_timeout:
            embed.add_field(
                name="Afk timeout",
                value=f"{f'{format_timespan(before.afk_timeout)}' if before.afk_timeout is not None else None} -> {f'{format_timespan(after.afk_timeout)}' if after.afk_timeout is not None else None}",
            )
        if before.name != after.name:
            embed.add_field(name="Name", value=f"{before.name} -> {after.name}")
        if before.emoji_limit is not after.emoji_limit:
            embed.add_field(
                name="Emoji Limit", value=f"{before.emoji_limit} -> {after.emoji_limit}"
            )
        if before.sticker_limit is not after.sticker_limit:
            embed.add_field(
                name="Sticker Limit",
                value=f"{before.sticker_limit} -> {after.sticker_limit}",
            )
        if before.verification_level is not after.verification_level:
            embed.add_field(
                name="Verification level",
                value=f"{before.verification_level} -> {after.verification_level}",
            )
        if before.explicit_content_filter is not after.explicit_content_filter:
            embed.add_field(
                name="Explicit content filter",
                value=f"{before.explicit_content_filter} -> {after.explicit_content_filter}",
            )
        if before.default_notifications is not after.default_notifications:
            embed.add_field(
                name="Default notifications",
                value=f"{before.default_notifications} -> {after.default_notifications}",
            )

        if before.preferred_locale is not after.preferred_locale:
            embed.add_field(
                name="Preferred locale",
                value=f"{before.preferred_locale} -> {after.preferred_locale}",
            )
        if before.premium_subscriber_role is not after.premium_subscriber_role:
            embed.add_field(
                name="Premium subscriber role",
                value=f"{before.premium_subscriber_role.mention} -> {after.premium_subscriber_role.mention}",
            )
        if before.mfa_level is not after.mfa_level:
            embed.add_field(
                name="MFA level",
                value=f"{before.mfa_level} -> {after.mfa_level}",
            )
        if (
            before.premium_progress_bar_enabled
            is not after.premium_progress_bar_enabled
        ):
            embed.add_field(
                name="Premium progress bar",
                value=f"{f'Enabled' if before.premium_progress_bar_enabled is True else 'Disabled'} -> {f'Enabled' if after.premium_progress_bar_enabled is True else 'Disabled'}",
            )
        if before.premium_tier is not after.premium_tier:
            embed.add_field(
                name="Premium tier",
                value=f"{before.premium_tier} -> {after.premium_tier}",
            )
        if before.premium_subscription_count is not after.premium_subscription_count:
            embed.add_field(
                name="Premium subscription count",
                value=f"{before.premium_subscription_count} -> {after.premium_subscription_count}",
            )

        await webhook_constructor(bot=self.bot, url=SQL_NEEDED, embed=embed)

    @Cog.listener()
    async def on_guild_channel_create(self, channel: GuildChannel):
        pass

    @Cog.listener()
    async def on_guild_channel_delete(self, channel: GuildChannel):
        pass

    @Cog.listener()
    async def on_guild_role_create(self, role: Role):
        pass

    @Cog.listener()
    async def on_guild_role_delete(self, role: Role):
        pass

    @Cog.listener()
    async def on_guild_role_update(self, before: Role, after: Role):
        pass

    @Cog.listener()
    async def on_guild_channel_update(self, before: GuildChannel, after: GuildChannel):
        pass

    @Cog.listener()
    async def on_guild_channel_pins_update(
        self, channel: TextChannel, last_pin: datetime
    ):
        pass

    @Cog.listener()
    async def on_guild_emojis_update(
        self, guild: Guild, before: list[Emoji], after: list[Emoji]
    ):
        pass

    @Cog.listener()
    async def on_guild_sticker_update(
        self, guild: Guild, before: list[GuildSticker], after: list[GuildSticker]
    ):
        pass

    # ------------------------------------------------------------------------------------------------------------ #

    # --------------------------------------- Member / User Events ----------------------------------------------- #

    @Cog.listener()
    async def on_member_join(self, member: Member):
        await member_events(self.bot, member, "JOIN")

    @Cog.listener()
    async def on_member_remove(self, member: Member):
        await member_events(self.bot, member, "LEAVE")

    @Cog.listener()
    async def on_member_update(self, before: Member, after: Member):
        pass

    @Cog.listener()
    async def on_user_update(self, before: User, after: User):
        pass

    @Cog.listener()
    async def on_presence_update(self, before: Member, after: Member):
        pass

    @Cog.listener()
    async def on_member_ban(self, guild: Guild, user: User):
        pass

    @Cog.listener()
    async def on_member_unban(self, guild: Guild, user: User):
        pass

    # ------------------------------------------------------------------------------------------------------------ #

    # ------------------------------------ Message Events -------------------------------------------------------- #

    @Cog.listener()
    async def on_messsage(self, message: Message):
        pass

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

    # ------------------------------------------------------------------------------------------------------------ #

    # ------------------------------------------ Voice Events ---------------------------------------------------- #

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

    # ------------------------------------------------------------------------------------------------------------ #

    # ----------------------------------------- Invite Events ---------------------------------------------------- #

    @Cog.listener()
    async def on_invite_create(self, invite: Invite):
        pass

    @Cog.listener()
    async def on_invite_delete(self, invite: Invite):
        pass

    # ------------------------------------------------------------------------------------------------------------ #

    # ------------------------------------ Intergration Events --------------------------------------------------- #

    @Cog.listener()
    async def on_intergration_create(self, integration: Integration):
        pass

    @Cog.listener()
    async def on_intergration_update(self, before: Integration, after: Integration):
        pass

    @Cog.listener()
    async def on_guild_integration_update(self, guild: Guild, integration: Integration):
        pass

    @Cog.listener()
    async def on_webhook_update(self, before: Webhook, after: Webhook):
        pass

    @Cog.listener()
    async def on_interaction(self, interaction: Interaction):
        pass

    # ------------------------------------------------------------------------------------------------------------ #

    # ------------------------------------------ Event Events ---------------------------------------------------- #

    @Cog.listener()
    async def on_scheduled_event_create(self, event: ScheduledEvent):
        pass

    @Cog.listener()
    async def on_scheduled_event_delete(self, event: ScheduledEvent):
        pass

    @Cog.listener()
    async def on_scheduled_event_update(
        self, before: ScheduledEvent, after: ScheduledEvent
    ):
        pass

    @Cog.listener()
    async def on_scheduled_event_user_add(self, event: ScheduledEvent, user: User):
        pass

    @Cog.listener()
    async def on_scheduled_event_user_remove(self, event: ScheduledEvent, user: User):
        pass

    # ------------------------------------------------------------------------------------------------------------ #

    # ------------------------------------------Stage Events ----------------------------------------------------- #

    @Cog.listener()
    async def on_stage_instance_create(self, stage_instance: StageInstance):
        pass

    @Cog.listener()
    async def on_stage_instance_delete(self, stage_instance: StageInstance):
        pass

    @Cog.listener()
    async def on_stage_instance_update(
        self, before: StageInstance, after: StageInstance
    ):
        pass

    # ------------------------------------------------------------------------------------------------------------ #

    # ------------------------------------------ Thread Events ----------------------------------------------------- #

    @Cog.listener()
    async def on_thread_create(self, thread: Thread):
        pass

    @Cog.listener()
    async def on_thread_delete(self, thread: Thread):
        pass

    @Cog.listener()
    async def on_thread_update(self, before: Thread, after: Thread):
        pass

    @Cog.listener()
    async def on_thread_remove(self, thread: Thread):
        pass

    @Cog.listener()
    async def on_thread_member_join(self, member: ThreadMember):
        pass

    @Cog.listener()
    async def on_thread_member_remove(self, member: ThreadMember):
        pass


async def setup(bot):
    await bot.add_cog(Events_Cog(bot))
