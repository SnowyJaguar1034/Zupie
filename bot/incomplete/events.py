import discord
import datetime


from discord import Activity, app_commands, Webhook
# from apscheduler.schedulers.asyncio import AsyncIOScheduler
# from discord_webhook import DiscordWebhook, DiscordEmbed
from dotenv import load_dotenv

load_dotenv()
class Permissions(app_commands.Group):
