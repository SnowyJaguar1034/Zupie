import asyncio

# from discord.gateway import DiscordClientWebSocketResponse
from datetime import datetime, timedelta
from io import StringIO
from os import environ
from random import choice as rchoice
from typing import Optional

from classes.embeds import LogEmbed, NegativeEmbed, NeutralEmbed, PositiveEmbed
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


class GuildEvents(Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bulks = {}
        self.test_log = self.bot.get_channel(847066860377342002)

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
        embed = PositiveEmbed(
            title=f"Channel {channel.name} created",
            description=f"{channel.mention}",
            url=channel.jump_url,
        )
        embed.set_footer(text=f"Channel ID: {channel.id}")
        embed.add_field(name="Channel category", value=f"{channel.category.mention}")
        # add a field for channel posistion of type int, value 0 is top channel and value 500 is bottom channel
        embed.add_field(
            name="Channel position",
            value=f"Top: 0, Bottom: 500 - Position: {channel.position}",
        )
        embed.add_field(name="Channel creation time", value=f"{channel.created_at}")
        embed.add_field(
            name="Channel permission overwrites",
            value=f"{channel.overwrites}",
        )
        embed.add_field(
            name="Permissions Synced",
            value="Permissions synced"
            if channel.permissions_synced is True
            else "Permissions not synced",
        )
        embed.add_field(
            name="Roles with overwritten permissions",
            value=", ".join(
                [
                    role.mention
                    for role in channel.overwrites
                    if len(channel.changed_roles) >= 1
                ]
            ),
        )
        await webhook_constructor(bot=self.bot, url=SQL_NEEDED, embed=embed)

    @Cog.listener()
    async def on_guild_channel_delete(self, channel: GuildChannel):
        embed = NegativeEmbed(
            title=f"Channel {channel.name} deleted",
            description=f"{channel.mention}",
        )
        embed.set_footer(text=f"Channel ID: {channel.id}")
        embed.add_field(name="Channel category", value=f"{channel.category.mention}")
        embed.add_field(
            name="Channel position",
            value=f"Top: 0, Bottom: 500 - Position: {channel.position}",
        )
        embed.add_field(name="Channel creation time", value=f"{channel.created_at}")
        embed.add_field(
            name="Channel permission overwrites",
            value=f"{channel.overwrites}",
        )
        embed.add_field(
            name="Permissions Synced",
            value="Permissions synced"
            if channel.permissions_synced is True
            else "Permissions not synced",
        )
        embed.add_field(
            name="Roles with overwritten permissions",
            value=", ".join(
                [
                    role.mention
                    for role in channel.overwrites
                    if len(channel.changed_roles) >= 1
                ]
            ),
        )
        await webhook_constructor(bot=self.bot, url=SQL_NEEDED, embed=embed)

    @Cog.listener()
    async def on_guild_channel_update(self, before: GuildChannel, after: GuildChannel):
        embed = NeutralEmbed(title="Channel updated")
        embed.set_footer(text=f"Channel ID: {after.id}")
        if before.name is not after.name:
            embed.description = f"{before.mention} -> {after.mention}"
        else:
            embed.description = f"{before.mention}"
        if before.category is not after.category:
            embed.add_field(
                name="Channel category",
                value=f"{before.category.mention} -> {after.category.mention}",
            )
        if before.position is not after.position:
            embed.add_field(
                name="Channel position",
                value=f"Top: 0, Bottom: 500 - Position: {before.position} -> {after.position}",
            )
        embed.add_field(
            name="Permissions Synced",
            value="Permissions not synced -> Permissions synced"
            if before.permissions_synced is False and after.permissions_synced is True
            else "Permissions synced -> Permissions not synced"
            if before.permissions_synced is True and after.permissions_synced is False
            else "Permissions synced -> Permissions synced"
            if before.permissions_synced is True and after.permissions_synced is True
            else "Permissions not synced -> Permissions not synced",
        )
        if before.changed_roles is not after.changed_roles:
            embed.add_field(
                name="Roles with overwritten permissions",
                value=", ".join(
                    [
                        role.mention
                        for role in after.overwrites
                        if len(after.changed_roles) >= 1
                    ]
                ),
            )
        await webhook_constructor(bot=self.bot, url=SQL_NEEDED, embed=embed)

        print(f"Channel {before.name} was updated in {before.guild.name}")

    @Cog.listener()
    async def on_guild_channel_pins_update(
        self, channel: TextChannel, last_pin: datetime
    ):
        print(
            f"New pin was added to {channel.name} at <t:{int(last_pin.timestamp())}:R>"
        )

    @Cog.listener()
    async def on_guild_role_create(self, role: Role):
        print(f"Role {role.name} was created in {role.guild.name}")

    @Cog.listener()
    async def on_guild_role_delete(self, role: Role):
        print(f"Role {role.name} was deleted in {role.guild.name}")

    @Cog.listener()
    async def on_guild_role_update(self, before: Role, after: Role):
        print(f"Role {before.name} was updated in {before.guild.name}")

    @Cog.listener()
    async def on_guild_emojis_update(
        self, guild: Guild, before: list[Emoji], after: list[Emoji]
    ):
        print(f"Emojis were updated in {guild.name}")

    @Cog.listener()
    async def on_guild_sticker_update(
        self, guild: Guild, before: list[GuildSticker], after: list[GuildSticker]
    ):
        print(f"Stickers were updated in {guild.name}")


async def setup(bot):
    await bot.add_cog(GuildEvents(bot))
