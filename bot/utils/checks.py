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

from logging import getLogger

import discord
from discord.ext import commands

log = getLogger(__name__)

def is_bot_owner():
    def predicate(ctx):
        if ctx.author.id not in ctx.bot.configuration.owners:
            raise commands.NotOwner()
        else:
            return True
    return commands.check(predicate)


def is_bot_admin():
    def predicate(ctx):
        if ctx.author.id not in ctx.bot.configuration.admins and ctx.author.id not in ctx.bot.configuration.owners:
            raise commands.NotOwner()
        else:
            return True
    return commands.check(predicate)

def is_mod():
    async def predicate(ctx):
        has_role = False
        data = await ctx.bot.get_data(ctx.guild.id)
        roles = []
        for role in data[1]:
            if role not in roles:
                roles.append(role)
        for role in data[2]:
            if role not in roles:
                roles.append(role)
        for role in data[3]:
            if role not in roles:
                roles.append(role)
        for role in roles:
            role = ctx.guild.get_role(role)
            if not role:
                continue
            if role in ctx.author.roles:
                has_role = True
                break
        if has_role is False and ctx.author.guild_permissions.administrator is False:
            await ctx.send(embed=discord.Embed(description="You do not have access to use this command.",colour=discord.Colour.red()))
            return False
        else:
            return True

    return commands.check(predicate)


def is_banned_channel(self, ctx):
    return (
        channel.topic
        and channel.topic.startswith("ModMail Channel ")
        and channel.topic.replace("ModMail Channel ", "").split(" ")[0].isdigit()
        and (channel.topic.replace("ModMail Channel ", "").split(" ")[0] == str(user_id) if user_id else True)
    )


def is_allowed_channel(self, ctx):
    async def predicate(ctx):
        data = await ctx.bot.get_data(ctx.guild.id)
        if ctx.channel.id in data[30]:
        if not is_modmail_channel2(ctx.bot, ctx.channel):
            await ctx.send(
                embed=discord.Embed(description="This channel is not a ModMail channel.", colour=ctx.bot.error_colour)
            )
            return False
        else:
            return True

    return commands.check(predicate)




def in_database():
    async def predicate(ctx):
        async with ctx.bot.pool.acquire() as conn:
            res = await conn.fetchrow("SELECT category FROM data WHERE guild=$1", ctx.guild.id)
        if not res or not res[0]:
            await ctx.send(
                embed=discord.Embed(
                    description=f"Your server has not been set up yet. Use `{ctx.prefix}setup` first.",
                    colour=ctx.bot.error_colour,
                )
            )
        return True if res and res[0] else False

    return commands.check(predicate)


def is_premium():
    async def predicate(ctx):
        if not ctx.bot.configuration.main_server:
            return True
        async with ctx.bot.pool.acquire() as conn:
            res = await conn.fetch("SELECT guild FROM premium")
        all_premium = []
        for row in res:
            all_premium.extend(row[0])
        if ctx.guild.id not in all_premium:
            await ctx.send(
                embed=discord.Embed(
                    description="This server does not have premium. Want to get premium? More information "
                    f"is available with the `{ctx.prefix}premium` command.",
                    colour=ctx.bot.error_colour,
                )
            )
            return False
        else:
            return True

    return commands.check(predicate)


def is_patron():
    async def predicate(ctx):
        async with ctx.bot.pool.acquire() as conn:
            res = await conn.fetchrow("SELECT identifier FROM premium WHERE identifier=$1", ctx.author.id)
        if res:
            return True
        slots = await ctx.bot.tools.get_premium_slots(ctx.bot, ctx.author.id)
        if slots is False:
            await ctx.send(
                embed=discord.Embed(
                    description="This command requires you to be a patron. Want to become a patron? More "
                    f"information is available with the `{ctx.prefix}premium` command.",
                    colour=ctx.bot.error_colour,
                )
            )
            return False
        else:
            async with ctx.bot.pool.acquire() as conn:
                await conn.execute(
                    "INSERT INTO premium (identifier, guild) VALUES ($1, $2)",
                    ctx.author.id,
                    [],
                )
            return True

    return commands.check(predicate)
