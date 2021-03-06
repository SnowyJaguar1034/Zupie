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

import datetime
import os
import traceback
from logging import getLogger

import aiohttp
import asyncpg
import configuration
import discord
# import aioredis
from discord.ext import commands
from redis import asyncio as asyncredis

from .config import Config

log = getLogger(__name__)


class Zupie(commands.AutoShardedBot):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.start_time = datetime.datetime.utcnow()
        self.redis = None

    banned_guilds = []
    banned_users = []

    @property
    def uptime(self):
        return datetime.datetime.utcnow() - self.start_time

    @property
    def version(self):
        # return version
        return Config().VERSION

    @property
    def default_guild(self):
        return discord.Object(id=int(Config().DEFAULT_GUILD))

    @property
    def config(self):
        return Config()

    @property
    def configuration(self):
        return configuration

    async def get_data(self, guild):
        async with self.pool.acquire() as conn:
            res = await conn.fetchrow("SELECT * FROM data WHERE guild=$1", guild)
            if not res:
                res = await conn.fetchrow(
                    "INSERT INTO data VALUES ($1, $2, $3, $4,) RETURNING *",
                    guild,  # Guild
                    None,  # Default logs webhook
                    False,  # Is premium guild
                    None,  # Guilds custo bot token
                )
        return res

    async def get_members(self, member):
        async with self.pool.acquire() as conn:
            res = await conn.fetchrow("SELECT * FROM member WHERE member=$1", member)
            if not res:
                res = await conn.fetchrow(
                    "INSERT INTO member VALUES ($1, $2, $3, $4,) RETURNING *",
                    member,  # Member
                    [],  # List of premium guilds
                    0,  # number of potential premium guilds
                    False,  # DM Reminders
                )
        return res

    async def get_members_guilds(self, member, guild):
        async with self.pool.acquire() as conn:
            res = await conn.fetchrow(
                "SELECT * FROM members_guilds WHERE member=$1 and guild=$2",
                member,
                guild,
            )
            if not res:
                res = await conn.fetchrow(
                    "INSERT INTO members_guilds VALUES ($1, $2, $3, $4,) RETURNING *",
                    member,  # Member
                    guild,  # Guild
                    False,  # members afk status
                    None,  # Members afk message
                )
        return res

    async def get_log(self, guild: int, log: int):
        default_log = 1
        data = await self.get_data(guild)
        if data[log] != None and log != default_log:
            return data[log]
        else:
            return data[default_log]

    async def sync_bans(self, banned_guilds=[], banned_users=[]):
        async with self.pool.acquire() as conn:
            guilds_res = await conn.fetchrow("SELECT * FROM bans WHERE category==$1", 0)
            users_res = await conn.fetchrow("SELECT * FROM bans WHERE category==$1", 1)
        banned_guilds = list(set(guilds_res + banned_guilds))
        banned_users = list(set(users_res + banned_users))
        return banned_guilds, banned_users

    async def connect_redis(self):
        self.redis = await asyncredis.Redis()
        print(f"Pinging redis: {await self.redis.ping()}")
        await self.redis.close()
        # for line in info.split("\n"):
        #     if line.startswith("redis_version"):
        #         self.redis_version = line.split(":")[1]
        #         break

    async def setup_hook(self) -> None:
        print(
            "------",
            f"Logged in as: {self.user}",
            f"ID: {self.user.id}",
            f"Version: {self.version}",
            f"Started at: {datetime.datetime.utcnow()}",
            "------",
            sep="\n",
        )

    async def main(self):
        try:  # try to connect to redis
            await self.connect_redis()
        except Exception as e:
            print(f"Could not connect to redis: {e}")
        async with asyncpg.create_pool(
            database=Config().POSTGRES_DATABASE,
            user=Config().POSTGRES_USERNAME,
            password=Config().POSTGRES_PASSWORD,
            host=Config().POSTGRES_HOST,
            port=int(Config().POSTGRES_PORT),
            max_size=10,
            command_timeout=60,
        ) as pool:
            async with aiohttp.ClientSession() as session:
                async with self:
                    print(
                        "------", "Connected to postgres database", "------", sep="\n"
                    )
                    for extension in configuration.initial_extensions:
                        try:
                            await self.load_extension(extension)
                            print(f"Loaded {extension.title()}")
                        except Exception:
                            print(
                                f"\nFailed to Load Extension {extension}\n{traceback.format_exc()}\n"
                            )
                    self.pool = pool
                    self.session = session
                    # await self.sync_bans(self.banned_guilds, self.banned_users)
                    await self.start(self.config.TOKEN)

            # await self.connect_prometheus()
