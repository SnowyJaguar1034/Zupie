from main import bot as bot_var
from utils.helpers import interaction_or_context

from typing import Union, Sequence
from datetime import datetime
from traceback import format_exc

from discord import Member, User, Interaction, Embed, app_commands, Role, TextChannel, VoiceChannel, StageChannel, CategoryChannel, Colour, Object, Message, NotFound
from discord.ext.commands import Context

async def cog_func(task, transaction, cog):
    embed = Embed(timestamp=datetime.now())
    ephemeral = False
    try:
        if task == "LOAD":
            await bot_var.load_extension(cog)
            embed.color=(Colour.green())
        elif task == "UNLOAD":
            await bot_var.unload_extension(cog)
            embed.color=(Colour.orange())
        elif task == "RELOAD":
            await bot_var.reload_extension(cog)
            embed.color=(Colour.gold())
        embed.title=(f"__Cog {task.title()}ed__")
        embed.description=(f"{cog.split('.')[1].title()} has been {task.lower()}ed.")
    except Exception:
        embed.title=(f"__{task.title()} Error__")
        embed.description=(f"There was an error trying to {task.lower()} `{cog.split('.')[1].title()}`")
        embed.color=(Colour.red())
        embed.add_field(name="Traceback", value=f"```py\n{format_exc()}```")
        ephemeral=True
    embed.set_footer(text=f"{transaction.user}", icon_url=transaction.user.display_avatar.url)
    await interaction_or_context("SEND", transaction, embed, ephemeral)

async def cog_error(transaction, cog, task):
    embed = Embed(timestamp=datetime.now())
    embed.title=(f"__{task.title()} Error__")
    embed.description=(f"There was an error trying to {task.lower()} `{cog.split('.')[1].title()}`")
    embed.color=(Colour.red())
    embed.add_field(name="Traceback", value=f"```py\n{format_exc()}```")
    ephemeral=True
    embed.set_footer(text=f"{transaction.user}", icon_url=transaction.user.display_avatar.url)
    await interaction_or_context("SEND", transaction, embed, ephemeral)