import sys, discord, logging, json, asyncio, os, datetime, config, aiohttp, pathlib, traceback

from utils.services import Zupie
#from cogs.users import user

from discord import Activity, app_commands, Webhook
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

token = os.environ.get('TOKEN')
version = os.environ.get('VERSION')
webhook_url = os.environ.get('STATUS_WEBHOOK')
description=os.environ.get('DESCRIPTION')
default_guild = int(os.environ.get('DEFAULT_GUILD'))
default_guild_obj = discord.Object(id=default_guild)

extensions = [
	"cogs.users", 
	]

activity = Activity(name = f"version {version}", type = discord.ActivityType.playing)
bot = Zupie(
    intents=discord.Intents.default(),
    activity=activity,
    owner_ids=["365262543872327681"],
    description=description,
    version=version,
    command_prefix=commands.when_mentioned,
)

async def status_webhook(embed, name=None):
    async with aiohttp.ClientSession() as session:
        webhook = Webhook.from_url(webhook_url, session=session)
        await webhook.send(wait=True, username=bot.user if name is not None else name, embed=embed)

@bot.event
async def on_ready():
    print('------')
    print(
      f'Logged in as: {bot.user}',
      f'ID: {bot.user.id}',
      f'Guilds connected to: {len(bot.guilds)}',
      f'Version: {version}',
      f'Running shards: {len(bot.shards)}',
      f'Loaded cogs: {len(bot.cogs)}',
      f'Started at: {datetime.datetime.utcnow()}',
      sep='\n'
    )
    await bot.tree.sync(guild=discord.Object(id=default_guild))
    print('Sucessfully synced applications commands')
    print('------')

@bot.event
async def on_shard_ready(shard):
    #self.bot.prom.events.inc({"type": "READY"})
    embed = discord.Embed(title=f"Shard {shard} Ready", colour=discord.Colour.green(), 
    timestamp=datetime.datetime.utcnow(),)
    await status_webhook(embed)

@bot.event
async def on_shard_connect(shard):
    #self.bot.prom.events.inc({"type": "CONNECT"})
    embed = discord.Embed(title=f"Shard {shard} Connected",colour=discord.Colour.orange(),timestamp=datetime.datetime.utcnow(),)
    await status_webhook(embed)

@bot.event
async def on_shard_disconnect(shard):
    #self.bot.prom.events.inc({"type": "DISCONNECT"})
    embed = discord.Embed(title=f"Shard {shard} Disconnected", colour=discord.Colour.red(), timestamp=datetime.datetime.utcnow(),)
    await status_webhook(embed)

@bot.event
async def on_shard_resumed(shard):
    #self.bot.prom.events.inc({"type": "RESUME"})
   
    embed = discord.Embed(title=f"Shard {shard} Resumed", colour=discord.Colour.yellow(), timestamp=datetime.datetime.utcnow(),)
    await status_webhook(embed)

@app_commands.command()
@app_commands.guilds(discord.Object(id=default_guild))
async def tree(interaction: discord.Interaction):
    await bot.tree.sync(guild=discord.Object(id=interaction.guild_id))
    await interaction.response.send_message(f'Synced the tree.', ephemeral=True)
    bot.tree.add_command(tree)



if __name__ == '__main__':
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError as e:
        loop = asyncio.get_event_loop()
    loop.run_until_complete(bot.start_bot())
