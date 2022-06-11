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

import contextlib  # Needed for Eval
import io
import os
import textwrap
import traceback

import discord
from discord import ButtonStyle, Interaction, TextStyle, ui  # Needed for Buttons
from discord.ext import menus  # Needed for Paginator
from discord.ext import commands
from dotenv import load_dotenv
from main import bot

from utils.paginator import paginate

load_dotenv()

default_guild = int(os.environ.get("DEFAULT_GUILD"))


def clean_code(code):
    if code.startswith("```") and code.endswith("```"):
        return "\n".join(code.split("\n")[1:][:-3])
    else:
        return code


async def evaluate(transaction, code):
    if isinstance(transaction, Interaction):
        locaL_variables = {
            "discord": discord,
            "commands": commands,
            "bot": bot,
            "interaction": transaction,
            "channel": transaction.channel,
            "author": transaction.user,
            "guild": transaction.guild,
            "message": transaction.message,
        }
    elif isinstance(transaction, commands.Context):
        locaL_variables = {
            "discord": discord,
            "commands": commands,
            "bot": bot,
            "ctx": transaction,
            "channel": transaction.channel,
            "author": transaction.author,
            "guild": transaction.guild,
            "message": transaction.message,
        }
    else:
        pass
    clean = clean_code(code)

    stdout = io.StringIO()
    try:
        with contextlib.redirect_stdout(stdout):
            exec(
                f"async def func():\n{textwrap.indent(clean, '    ')}",
                locaL_variables,
            )

            obj = await locaL_variables["func"]()
            result = f"{stdout.getvalue()}\n-- {obj}\n"

    except Exception as e:
        result = "".join(traceback.format_exception(e, e, e.__traceback__))

    entries = [result[i : i + 1991] for i in range(0, len(result), 1991)]

    await paginate(pages=entries, per_page=1, channel=transaction, type="EVAL")

    """
    @commands.command(name="eval", alias=["exec"])
    async def eval_legacy(self, ctx: commands.Context, *, code: str):
        await self.evaluate(ctx, code)
    """


class Evaluate(ui.Modal, title="Evaluate"):
    code = ui.TextInput(
        label="What code do you want to evaluate?",
        style=TextStyle.paragraph,
        placeholder="Type the code you want to evaluate here.",
        required=True,
        max_length=4000,
        default="print('Hello World!')",
    )

    async def on_submit(self, interaction: Interaction):
        await interaction.response.defer()
        # await interaction.response.send_message(
        # f"Processing your code now {interaction.user.mention}", ephemeral=False
        # )
        await evaluate(interaction, self.code.value)

    async def on_error(self, error: Exception, interaction: Interaction) -> None:
        await interaction.response.send_message(
            f"Oops! Something went wrong.",
            embed=discord.Embed(
                description=f"```py\n{traceback.format_exc()}```",
                colour=discord.Colour.red(),
            ),
            ephemeral=True,
        )
        # see we still get the error in terminal
        print(traceback.format_exc())
