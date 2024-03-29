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

from datetime import datetime, timedelta
from io import StringIO
from os import environ
from random import choice as rchoice
from typing import Optional

from discord import Colour, Embed, Forbidden, Guild, Member, Message, Object
from discord.ext import commands
from dotenv import load_dotenv
from utils.helper_users import timestamps_func
from utils.helpers import tag_format, webhook_constructor

load_dotenv()

from logging import getLogger

log = getLogger(__name__)

status_webhook = environ.get("STATUS_WEBHOOK")


async def guild_events(bot, guild: Guild, event: str):
    embed = Embed(
        title="Guild {event.title}",
        timestamp=datetime.utcnow(),
        description=f"{guild.name} ({guild.id})",
    )
    if event == "JOIN":
        embed.colour = Colour.green()
        if guild.id in bot.banned_guilds:
            await guild.leave()
        async with bot.pool.acquire() as conn:
            await conn.execute()
    elif event == "LEAVE":
        embed.colour = Colour.red()
    embed.set_footer(text=f"{len(bot.guilds)} servers")
    if bot.config.JOIN_ChANNEL:
        await webhook_constructor(bot=bot, url=bot.config.JOIN_ChANNEL, embed=embed)


async def raidmode(
    bot, member: Member, joincount: int = 0, required: int = 0, log: str = None
):
    embed = Embed(timestamp=datetime.utcnow())
    acc_age = datetime.utcnow() - member.created_at
    if acc_age < timedelta(days=required):
        if joincount > 3:
            embed.title = "Member Banned!"
            embed.description = f"{member}'s account is **{acc_age.days}** days old and has joined the server **{joincount}** times so the member was banned by raidmode."
            await member.ban(
                reason=f"Raidmode enabled: {member}'s account was deemeed too new by your raidmode configuration. The required age is {required} days old and this users account is {acc_age.days} days old. You can check the current required age with the modconfig command. This user has also joined the server {joincount} times which resulted in their ban."
            )
            webhook = await webhook_constructor(
                bot=bot, url=log, embed=embed, name="Raidmode Logs", edit=True
            )
            try:
                await member.send(
                    f"This server has raidmode **active** and requires users have a account that is older than **{required}** days old and to have not joined more than **3** times. As your account is less than the servers threshold and you have joined {joincount} times you have been banned."
                )
            except Forbidden:
                await webhook.edit(
                    "{member.id}",
                    embed=embed,
                    content=f"I was unable to DM {member} due to their DM's being closed.",
                )
        else:
            embed.title = "Member Kicked!"
            embed.description = f"{member} account is **{acc_age.days}** days old and so the member was kicked by raidmode."
            await member.ban(
                reason=f"Raidmode enabled: {member}'s account was deemeed too new by your raidmode configuration. The required age is {required} days old and this users account is {acc_age.days} days old. You can check the current required age with the modconfig command."
            )
            webhook = await webhook_constructor(
                bot=bot, url=log, embed=embed, name="Raidmode Logs", edit=True
            )
            try:
                await member.send(
                    f"This server has raidmode **active** and requires users have a account that is older than **{required}** days old. As your account is less than the servers threshold you have been kicked."
                )
            except Forbidden:
                await webhook.edit(
                    embed=embed,
                    content=f"I was unable to DM {member} due to their DM's being closed.",
                )


async def join_leaves(bot, member: Member, event: str, log: str):
    embed = Embed(colour=Colour.blue())
    member_status = "No status" if member.activity is None else member.activity.name

    embed.title = f"Member {event.title}"
    embed.description = f"{member.mention} joined {member.guild.name}"
    embed.set_author(name=f"{member} | {member.id}", icon_url=member.avatar.url)
    embed.set_thumbnail(url=member.avatar.url)
    embed.set_footer(text=f"Members: {member.guild.member_count}")
    embed.add_field(
        name=f"Status **{member.status}**", value=f"*{member_status}*", inline=False
    )
    await timestamps_func(member, embed, True)
    await webhook_constructor(bot=bot, url=log, embed=embed, edit=True)


async def bot_join(bot, member: Member, log: int, role: Object):
    log = bot.get_channel(log)
    member_status = "No status" if member.activity is None else member.activity.name
    await member.add_roles(*role, reason=f"{member} is a bot!", atomic=True)

    # async for entry in member.guild.audit_logs(action = discord.AuditLogAction.bot_add):
    # print(f'{0.user} added {0.target}')
    await log.send(f"{member.mention} was added.\n**Status:** {member_status}")


async def shard_events(bot, shard_id, event: str):
    embed = Embed(timestamp=datetime.utcnow())
    if event == "READY":
        embed.colour = Colour.green()
        embed.title = f"Shard {shard_id} Ready"
    elif event == "CONNECT":
        embed.colour = Colour.orange()
        embed.title = f"Shard {shard_id} Connected"
    elif event == "DISCONNECT":
        embed.colour = Colour.red()
        embed.title = f"Shard {shard_id} Disconnected"
    elif event == "RESUME":
        embed.colour = Colour.yellow()
        embed.title = f"Shard {shard_id} Resumed"
    await webhook_constructor(bot=bot, url=status_webhook, embed=embed)
    # for guild in bot.guilds:
    # if guild.shard_id == shard_id:
    # pass


async def member_events(bot, member: Member, event: str):
    data = await bot.get_data(member.guild.id)
    joincount = bot.get_members_guilds(member.id, member.guild.id)
    if event == "JOIN":
        count = joincount[2] + 1
        if data[5] == True:  # Raidmode status
            await raidmode(
                bot=bot,
                member=member,
                joincount=joincount[4],
                required=data[3],
                log=bot.get_log(guild=member.guild.id, log=11),
            )
        if data[12] == True:  # Member logs status
            await join_leaves(
                bot=bot,
                member=member,
                event=event,
                log=bot.get_log(member.guild.id, 11),
            )
        if data[16] == True and member.bot == False:  # Greet member status
            log = bot.get_channel(data[17])
            message = tag_format(
                payload=rchoice(data[18]),
                member=member,
                guild=member.guild,
            )
            await log.send(message)
        if data[15] == True:  # Assign bot role status
            log = bot.get_channel(bot.get_log(guild=member.guild.id, log=18))
            role = [Object(data[14])]
            member_status = (
                "No status" if member.activity is None else member.activity.name
            )
            await member.add_roles(*role, reason=f"{member} is a bot!", atomic=True)

        async with bot.pool.acquire() as conn:
            await conn.execute(
                "UPDATE members_guilds SET joincount=$1 WHERE member=$2 and guild=$3",
                count,
                member.id,
                member.guild.id,
            )
    elif event == "LEAVE":
        if data[12] == True:  # Member logs status
            await join_leaves(
                bot=bot,
                member=member,
                event=event,
                log=bot.get_log(member.guild.id, 11),
            )
        if data[23] == True or data[24] == True:  # Greet member status
            log = bot.get_channel(bot.get_log(guild=member.guild.id, log=18))
            message = tag_format(
                payload=rchoice(data[20]),
                member=member,
                guild=member.guild,
            )
            await log.send(message)


async def message_events(
    bot, message: Message, event: str, original: Optional[Message] = None
):
    embed = Embed(timestamp=datetime.utcnow())
    embed.set_footer(text=f"Message ID: {message.id}.")
    embed.set_author(
        name=f"{message.author} | {message.author.id}",
        icon_url=message.author.display_avatar.url,
    )
    if event == "DELETE":
        embed.colour = Colour.red()
        embed.title = "🗑 Message Deleteded"
        embed.description = f"{message.author.display_name} deleted a message in {message.channel.mention} ||`{message.channel}`||"
        embed.add_field(name="Content", value=f"{message.content}", inline=False)
    elif event == "EDIT":
        embed.title = "📝 Message Edited"
        embed.colour = Colour.dark_orange()
        embed.description = f"{message.author.display_name} edited a message in {message.channel.mention} ||`{message.channel}`||"
        embed.url = message.jump_url
        embed.add_field(name="Old Message:", value=f"{original.content}", inline=False)
        embed.add_field(name="New Message:", value=f"{message.content}", inline=False)
    await webhook_constructor(
        bot=bot, url=bot.get_log(guild=message.guild.id, log=8), embed=embed
    )
