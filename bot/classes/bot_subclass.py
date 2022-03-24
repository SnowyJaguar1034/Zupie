import discord, datetime, sys, traceback, os, pathlib, asyncio, aiohttp, config, asyncpg
#import logging, aioredis, asyncpg
from discord import app_commands, Object
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

token = os.environ.get('TOKEN')
version = os.environ.get('VERSION')
default_guild = int(os.environ.get('DEFAULT_GUILD'))


#log = logging.getLogger(__name__)

#COG_PATH = pathlib.Path("../cogs/")

class Zupie(commands.AutoShardedBot):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.start_time = datetime.datetime.utcnow()
        # self.cluster = kwargs.get("cluster_id")
        # self.cluster_count = kwargs.get("cluster_count")

    @property
    def uptime(self):
        return datetime.datetime.utcnow() - self.start_time

    @property
    def version(self):
        return version

    @property
    def default_guild(self):
        return discord.Object(id=int(os.environ.get('DEFAULT_GUILD')))

    @property
    def config(self):
        return config

    # @property
    # def helpers(self):
    #     return helpers

    # @property
    # def apis(self):
    #     return apis
    ''' 
    @property
    def primary_colour(self):
        return self.config.primary_colour

    @property
    def user_colour(self):
        return self.config.user_colour

    @property
    def mod_colour(self):
        return self.config.mod_colour

    @property
    def error_colour(self):
        return self.config.error_colour



    async def get_data(self, guild):
        async with self.pool.acquire() as conn:
            res = await conn.fetchrow("SELECT * FROM data WHERE guild=$1", guild)
            if not res:
                res = await conn.fetchrow(
                    "INSERT INTO data VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14, $15, $16, $17, $18, $19, $20, $21, $22, $23, $24, $25, $26, $27, $28, $29) RETURNING *",
                    guild, None, None, [], None, None, None, False, [], [], False, [], [], 0, False, 7, None, [], None, None, 0, 0, None, None, None, None, 0, None, [],
                    )
                    # guild, prefix, category, access roles, logging, welcome, goodbye, logging plus, ping roles, blacklist, anonymous, locked roles, raid channel, current count, raidmode status, acc_age, raidmode log, mistakes role, join/leave log, raidrole, isolation time, guild mistakes, counting channel, deleted messages log, edited messages log, suggestion channel, suggestion count, starbaord channel, bad words
        return res

    async def get_member_guild(self, member, guild):
        async with self.pool.acquire() as conn:
            res = await conn.fetchrow('SELECT * FROM membersguilds WHERE member=$1 and guild=$2', member, guild)
            if not res:
                res = await conn.fetchrow("INSERT INTO membersguilds (member, guild, joincount, mistakes, afk, afkmessage) VALUES ($1, $2, $3, $4, $5, $6) RETURNING *",
                    member, guild, 0, 0, False, None)
        return res

    async def get_tickets(self, post):
        async with self.pool.acquire() as conn:
            res = await conn.fetchrow('SELECT * FROM tickets WHEREpostlocal=$1', post)
            if not res: 
                res = await conn.fetchrow("INSERT INTO tickets (postlocal, postremote, member, expiry) VALUES ($1, $2, $3, $4, $5) RETURNING *",
                    post, None, None, None)
        return res

    async def get_sug(self, post, guild):
        async with self.pool.acquire() as conn:
            res = await conn.fetchrow(
                "SELECT * FROM suggestions WHERE post=$1 and guild=$2", post, guild)
            if not res:
                res = await conn.fetchrow(
                    "INSERT INTO suggestions (post, guild, member, original, message) VALUES ($1, $2, $3, $4, $5) RETURNING *",
                    post, guild, None, None, None)
        return res

    async def get_star(self, star):
        async with self.pool.acquire() as conn:
            res = await conn.fetchrow("SELECT * FROM starboard WHERE id=$1", star)
            if not res:
                res = await conn.fetchrow(
                    "INSERT INTO starboard VALUES ($1, $2, $3, $4) RETURNING *",
                    ID, 
                    None, 
                    None,
                    0,
                )
        return res

    all_prefix = {}
    banned_guilds = []
    banned_users = []

    async def connect_redis(self):
        self.redis = await aioredis.create_pool("redis://localhost", minsize=5, maxsize=10, loop=self.loop, db=0)
        info = (await self.redis.execute("INFO")).decode()
        for line in info.split("\n"):
            if line.startswith("redis_version"):
                self.redis_version = line.split(":")[1]
                break
    '''
    async def setup_hook(self) -> None:
        print(
            '------',
            f'Logged in as: {self.user}',
            f'ID: {self.user.id}',
            f'Version: {self.version}',
            f'Started at: {datetime.datetime.utcnow()}',
            '------',
            sep="\n"
        )

    async def main(self):
        async with asyncpg.create_pool(**self.config.database, max_size=10, command_timeout=60) as pool:
            async with aiohttp.ClientSession() as session:
                async with self:
                    print(
                        '------',
                        'Connected to postgres database',
                         '------',
                        sep="\n"
                        )
                    for extension in self.config.initial_extensions:
                        try:
                            await self.load_extension(extension)
                            print(f"Loaded {extension.title()}")
                        except Exception:
                            print(f"\nFailed to Load Extension {extension}\n{traceback.format_exc()}\n")
                    self.pool = pool
                    self.session = session
                    await self.start(token)

            #await self.connect_redis()
            #await self.connect_prometheus()