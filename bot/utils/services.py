import discord, datetime, sys, traceback, os, pathlib, asyncio, aiohttp, config
#import logging, aioredis, asyncpg
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

token = os.environ.get('TOKEN')

#log = logging.getLogger(__name__)

#COG_PATH = pathlib.Path("../cogs/")

class Zupie(commands.AutoShardedBot):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.start_time = datetime.datetime.utcnow()
        self.session = aiohttp.ClientSession(loop=self.loop)
        self.cluster = kwargs.get("cluster_id")
        self.cluster_count = kwargs.get("cluster_count")

    @property
    def uptime(self):
        return datetime.datetime.utcnow() - self.start_time

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
    #async def connect_postgres(self):
        #self.pool = await asyncpg.create_pool(**self.config.database, max_size=10, command_timeout=60)
    ''' 
    async def connect_prometheus(self):
        self.prom = prometheus.Prometheus(self)
        if self.config.testing is False:
            await self.prom.start()
    '''

    async def start_bot(self):
        #await self.connect_redis()
        #await self.connect_postgres()
        #await self.connect_prometheus()
        for extension in self.config.initial_extensions:
            try:
                self.load_extension(extension)
                print(f"Loaded {extension} Cog")
            except Exception as e:
                exc = '{}: {}'.format(type(e).__name__, e)
                print(f"Failed to Load Extension {extension}\n{exc}")
                #print(f"Failed to load extension {extension}.", file=sys.stderr)
                #print(traceback.print_exc())
        await self.start(token)
