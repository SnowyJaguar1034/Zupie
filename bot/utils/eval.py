import aiohttp, asyncio, discord
from discord.ext import commands

from main import bot

import contextlib, io, os, textwrap, traceback  # Needed for Eval
from discord.ext import menus  # Needed for Paginator
from discord import ui, Interaction, TextStyle, ButtonStyle  # Needed for Buttons

from dotenv import load_dotenv

load_dotenv()

default_guild = int(os.environ.get("DEFAULT_GUILD"))


class MySource(menus.ListPageSource):
    async def format_page(self, menu, entries):
        return f"```py\n{entries}```"


class MyMenuPages(ui.View, menus.MenuPages):
    def __init__(self, source):
        super().__init__(timeout=60)
        self._source = source
        self.current_page = 0
        self.ctx = None
        self.message = None

    async def start(self, ctx):
        await self._source._prepare_once()
        self.ctx = ctx
        self.message = await self.send_initial_message(ctx, ctx.channel)

    async def _get_kwargs_from_page(self, page):
        value = await super()._get_kwargs_from_page(page)
        if "view" not in value:
            value.update({"view": self})
        return value

    async def interaction_check(self, interaction):
        if isinstance(interaction, commands.Context):
            return interaction.user == self.ctx.author
        elif isinstance(interaction, Interaction):
            return interaction.user == self.user

    @ui.button(
        emoji="<:before_fast_check:754948796139569224>",
        style=ButtonStyle.blurple,
    )
    async def first_page(self, button, interaction):
        await self.show_page(0)

    @ui.button(emoji="<:before_check:754948796487565332>", style=ButtonStyle.blurple)
    async def before_page(self, button, interaction):
        await self.show_checked_page(self.current_page - 1)

    @ui.button(emoji="<:stop_check:754948796365930517>", style=ButtonStyle.blurple)
    async def stop_page(self, button, interaction):
        self.stop()

    @ui.button(emoji="<:next_check:754948796361736213>", style=ButtonStyle.blurple)
    async def next_page(self, button, interaction):
        await self.show_checked_page(self.current_page + 1)

    @ui.button(emoji="<:next_fast_check:754948796391227442>", style=ButtonStyle.blurple)
    async def last_page(self, button, interaction):
        await self.show_page(self._source.get_max_pages() - 1)


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

    entries = [result[i : i + 2000] for i in range(0, len(result), 2000)]

    formatter = MySource(entries, per_page=1)
    # menu = menus.MenuPages(formatter)
    menu = MyMenuPages(formatter)
    await menu.start(transaction)

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
        await interaction.response.send_message(
            f"Processing your code now {interaction.user.mention}", ephemeral=False
        )
        await evaluate(interaction, self.code.value)

    async def on_error(self, error: Exception, interaction: Interaction) -> None:
        await interaction.response.send_message(
            f"Oops! Something went wrong.\n{traceback.format_exc()}", ephemeral=True
        )
        print(traceback.format_exc())
