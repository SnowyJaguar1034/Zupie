import aiohttp, asyncio, discord
from discord.ext import commands

import contextlib, io, os, textwrap, traceback # Needed for Eval
from discord.ext import menus # Needed for Paginator
from discord import ui # Needed for Buttons

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
		if 'view' not in value:
			value.update({'view': self})
		return value

	async def interaction_check(self, interaction):
		return interaction.user == self.ctx.author

	@ui.button(emoji='<:before_fast_check:754948796139569224>', style=discord.ButtonStyle.blurple)
	async def first_page(self, button, interaction):
		await self.show_page(0)

	@ui.button(emoji='<:before_check:754948796487565332>', style=discord.ButtonStyle.blurple)
	async def before_page(self, button, interaction):
		await self.show_checked_page(self.current_page - 1)

	@ui.button(emoji='<:stop_check:754948796365930517>', style=discord.ButtonStyle.blurple)
	async def stop_page(self, button, interaction):
		self.stop()

	@ui.button(emoji='<:next_check:754948796361736213>', style=discord.ButtonStyle.blurple)
	async def next_page(self, button, interaction):
		await self.show_checked_page(self.current_page + 1)

	@ui.button(emoji='<:next_fast_check:754948796391227442>', style=discord.ButtonStyle.blurple)
	async def last_page(self, button, interaction):
		await self.show_page(self._source.get_max_pages() - 1)

class Eval(commands.Cog):
	def __init__(self,bot):
		self.bot = bot
	async def cog_load(self):
		pass
	async def cog_unload(self):
		pass
	def clean_code(code):
		if code.startswith("```") and code.endswith("```"):
			return "\n".join(code.split("\n")[1:][:-3])
		else:
			return code	

	@commands.command(name="eval", alias=["exec"])
	async def eval(self, ctx, *, code):
		if code.startswith("```") and code.endswith("```"):
			code = "\n".join(code.split("\n")[1:][:-3])

		locaL_variables = {
			"discord": discord,
			"commands": commands,
			"bot": self.bot,
			"ctx": ctx,
			"channel": ctx.channel,
			"author": ctx.author,
			"guild": ctx.guild,
			"message": ctx.message
		}

		stdout = io.StringIO()
		try:
			with contextlib.redirect_stdout(stdout):
				exec(
					f"async def func():\n{textwrap.indent(code, '    ')}", locaL_variables,
				)

				obj = await locaL_variables["func"]()
				result = f"{stdout.getvalue()}\n-- {obj}\n"
				
		except Exception as e:
			result = "".join(traceback.format_exception(e, e, e.__traceback__))

		entries = [result[i: i + 2000] for i in range(0, len(result), 2000)]
		
		formatter = MySource(entries, per_page=1)
		#menu = menus.MenuPages(formatter)
		menu = MyMenuPages(formatter)
		await menu.start(ctx)

async def setup(bot):
	await bot.add_cog(Eval(bot))