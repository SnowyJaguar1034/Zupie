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

from discord import Interaction  # Needed for Buttons
from discord import ButtonStyle, Embed, TextChannel, ui, utils
from discord.ext import commands
from discord.ext.menus import (  # The latter is being imported so that I can import it from the `bulk message delete` event file.
    ListPageSource, MenuPages)

log = getLogger(__name__)


class EvalSource(ListPageSource):
    async def format_page(self, menu, entries):
        return f"```py\n{entries}```"


class Pager(ui.View, MenuPages):
    def __init__(self, source):
        super().__init__(timeout=60)
        self._source = source
        self.current_page = 0
        self.interaction = None
        self.message = None

    button_style = ButtonStyle.grey

    async def start(self, interaction):
        await self._source._prepare_once()
        self.interaction = interaction
        initial_page = await self._source.get_page(0)
        kwargs = await self._get_kwargs_from_page(initial_page)
        try:
            self.message = await interaction.followup.send(**kwargs)
        except:
            self.message = await interaction.channel.send(**kwargs)

    async def _get_kwargs_from_page(self, page):
        value = await utils.maybe_coroutine(self._source.format_page, self, page)
        if isinstance(value, list):
            new_value = ""
            for s in value:
                new_value += s
            value = {"content": new_value, "embed": None}
        if isinstance(value, str):
            value = {"content": value, "embed": None}
        if isinstance(value, Embed):
            value = {"embed": value, "content": None}
        if "view" not in value:
            value.update({"view": self})
        return value

    async def interaction_check(self, interaction):
        try:
            return interaction.user == self.interaction.user
        except:
            return interaction.user == self.interaction.author

    async def show_page(self, page_number):
        page = await self._source.get_page(page_number)
        self.current_page = page_number
        kwargs = await self._get_kwargs_from_page(page)
        try:
            await self.current_interaction.response.edit_message(**kwargs)
        except:
            await self.message.edit(**kwargs)

    @ui.button(
        emoji="<:before_fast_check:754948796139569224>",
        style=button_style,
    )
    async def first_page(self, interaction, button):
        self.current_interaction = interaction
        await self.show_page(0)

    @ui.button(emoji="<:before_check:754948796487565332>", style=button_style)
    async def before_page(self, interaction, button):
        self.current_interaction = interaction
        await self.show_checked_page(self.current_page - 1)

    @ui.button(emoji="<:stop_check:754948796365930517>", style=button_style)
    async def stop_page(self, interaction, button):
        self.stop()
        try:
            await self.message.delete_original_message()
        except:
            await self.message.delete()

    @ui.button(emoji="<:next_check:754948796361736213>", style=button_style)
    async def next_page(self, interaction, button):
        self.current_interaction = interaction
        await self.show_checked_page(self.current_page + 1)

    @ui.button(emoji="<:next_fast_check:754948796391227442>", style=button_style)
    async def last_page(self, interaction, button):
        self.current_interaction = interaction
        await self.show_page(self._source.get_max_pages() - 1)


async def paginate(type: str, pages: list, channel: TextChannel, per_page: int = 1):
    formated_pages = [page for page in pages]
    if type == "EMBED":
        formatter = ListPageSource(formated_pages, per_page=per_page)
    elif type == "EVAL":
        formatter = EvalSource(formated_pages, per_page=per_page)
    elif type == "TEXT":
        formatter = TextPageSource(formated_pages, per_page=per_page)
    # menu = menus.MenuPages(formatter)
    menu = Pager(formatter)
    await menu.start(channel)
