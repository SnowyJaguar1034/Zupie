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

from datetime import datetime
from logging import getLogger
from traceback import format_exc
from typing import Sequence, Union

from discord import (CategoryChannel, Colour, Embed, Interaction, Member,
                     Message, NotFound, Object, Role, StageChannel,
                     TextChannel, User, VoiceChannel, app_commands)
from discord.ext.commands import Context
from main import bot as bot_var
from utils.helpers import interaction_or_context

log = getLogger(__name__)


async def cog_func(task, transaction, cog):
    embed = Embed(timestamp=datetime.now())
    ephemeral = False
    try:
        if task == "LOAD":
            await bot_var.load_extension(cog)
            embed.color = Colour.green()
        elif task == "UNLOAD":
            await bot_var.unload_extension(cog)
            embed.color = Colour.orange()
        elif task == "RELOAD":
            await bot_var.reload_extension(cog)
            embed.color = Colour.gold()
        embed.title = f"__Cog {task.title()}ed__"
        embed.description = f"{cog.split('.')[1].title()} has been {task.lower()}ed."
    except Exception:
        embed.title = f"__{task.title()} Error__"
        embed.description = (
            f"There was an error trying to {task.lower()} `{cog.split('.')[1].title()}`"
        )
        embed.color = Colour.red()
        embed.add_field(name="Traceback", value=f"```py\n{format_exc()}```")
        ephemeral = True
    embed.set_footer(
        text=f"{transaction.user}", icon_url=transaction.user.display_avatar.url
    )
    await interaction_or_context("SEND", transaction, embed, ephemeral)


async def cog_error(transaction, cog, task):
    embed = Embed(timestamp=datetime.now())
    embed.title = f"__{task.title()} Error__"
    embed.description = (
        f"There was an error trying to {task.lower()} `{cog.split('.')[1].title()}`"
    )
    embed.color = Colour.red()
    embed.add_field(name="Traceback", value=f"```py\n{format_exc()}```")
    ephemeral = True
    embed.set_footer(
        text=f"{transaction.user}", icon_url=transaction.user.display_avatar.url
    )
    await interaction_or_context("SEND", transaction, embed, ephemeral)
