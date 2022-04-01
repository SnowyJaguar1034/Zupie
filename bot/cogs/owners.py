from classes.cogbase import CogBase
from utils.helpers import parent
from utils.eval import Evaluate, evaluate
from utils.helper_owners import cog_func
from subprocess import check_output, STDOUT


from discord import (
    Member,
    User,
    Interaction,
    Embed,
    app_commands,
    Object,
    TextChannel,
    VoiceChannel,
    StageChannel,
    CategoryChannel,
    Colour,
    Embed,
)
from discord.ext import commands

from typing import Union
from datetime import datetime
from os import environ
from traceback import format_exc
from dotenv import load_dotenv
from main import bot

load_dotenv()

default_guild = int(environ.get("DEFAULT_GUILD"))


class Owner_Cog(
    CogBase,
    name="owner",
    description="Shows all owner related commands",
):
    def __init__(self, bot):
        super().__init__(bot)
        self.bot = bot

    eval_slash = app_commands.Group(name="eval", description="Evaluate somehting")

    @app_commands.command(name="sync-tree", description="Syncs the slash command tree")
    @app_commands.guilds(Object(id=default_guild))
    async def tree(self, interaction: Interaction):
        try:
            await self.bot.tree.sync(guild=discord.Object(id=interaction.guild_id))
        except Exception as e:
            print(f"\Failed to sync tree:\n{format_exc()}\n")
        await interaction.response.send_message(f"Synced the tree.", ephemeral=True)

    cogs_group = app_commands.Group(
        name="cog", description="work with cogs", guild_ids=[default_guild]
    )
    info_description = "Show some information about yourself or the member specified."
    joined_description = (
        "Show when yourself or the member specified joined this server and Discord."
    )
    avatar_description = "Show a users avatar."
    roles_description = "Show a users roles."
    status_description = "Show a users status."
    permissions_description = "Show a member's permission, Defualts to current channel."

    @cogs_group.command(name="load", description="loads a cog")
    @app_commands.describe(cog="the cog to load.")
    @app_commands.choices(
        cog=[
            app_commands.Choice(name=cog.split(".")[1].title(), value=cog)
            for cog in bot.config.initial_extensions
        ]
    )
    async def load_slash(self, interaction: Interaction, cog: str):
        embed = Embed(timestamp=datetime.now())
        try:
            await self.bot.load_extension(cog)
            embed.color = Colour.green()
            ephemeral = False
        except Exception as e:
            embed.description = f"There was an error trying to {interaction.command.name.lower()} `{cog.split('.')[1].title()}`"
            embed.color = Colour.red()
            embed.add_field(name="Traceback", value=f"```py\n{format_exc()}```")
            ephemeral = True
        embed.title = f"__Cog {interaction.command.name.title()}ed__"
        embed.set_footer(
            text=f"{interaction.user}", icon_url=interaction.user.display_avatar.url
        )
        await interaction.response.send_message(embed=embed, ephemeral=ephemeral)
        await self.bot.tree.sync(guild=Object(id=interaction.guild_id))

    @cogs_group.command(name="unload", description="unloads a cog")
    @app_commands.describe(cog="the cog to unload.")
    @app_commands.choices(
        cog=[
            app_commands.Choice(name=cog.split(".")[1].title(), value=cog)
            for cog in bot.config.initial_extensions
        ]
    )
    async def unload_slash(self, interaction: Interaction, cog: str):
        embed = Embed(timestamp=datetime.now())
        try:
            await self.bot.unload_extension(cog)
            embed.color = Colour.green()
            ephemeral = False
        except Exception as e:
            embed.description = f"There was an error trying to {interaction.command.name.lower()} `{cog.split('.')[1].title()}`"
            embed.color = Colour.red()
            embed.add_field(name="Traceback", value=f"```py\n{format_exc()}```")
            ephemeral = True
        embed.title = f"__Cog {interaction.command.name.title()}ed__"
        embed.set_footer(
            text=f"{interaction.user}", icon_url=interaction.user.display_avatar.url
        )
        await interaction.response.send_message(embed=embed, ephemeral=ephemeral)
        await self.bot.tree.sync(guild=Object(id=interaction.guild_id))

    @cogs_group.command(name="reload", description="reloads a cog")
    @app_commands.describe(cog="the cog to reload.")
    @app_commands.choices(
        cog=[
            app_commands.Choice(name=cog.split(".")[1].title(), value=cog)
            for cog in bot.config.initial_extensions
        ]
    )
    async def reload_slash(self, interaction: Interaction, cog: str):
        embed = Embed(timestamp=datetime.now())
        try:
            await self.bot.reload_extension(cog)
            embed.color = Colour.green()
            ephemeral = False
        except Exception as e:
            embed.description = f"There was an error trying to {interaction.command.name.lower()} `{cog.split('.')[1].title()}`"
            embed.color = Colour.red()
            embed.add_field(name="Traceback", value=f"```py\n{format_exc()}```")
            ephemeral = True
        embed.title = f"__Cog {interaction.command.name.title()}ed__"
        embed.set_footer(
            text=f"{interaction.user}", icon_url=interaction.user.display_avatar.url
        )
        await interaction.response.send_message(embed=embed, ephemeral=ephemeral)
        await self.bot.tree.sync(guild=Object(id=interaction.guild_id))

    @eval_slash.command(name="bash", description="executes a bash command")
    @app_commands.describe(command="the bash command to use")
    async def bash_slash(self, interaction: Interaction, *, command: str):
        embed = Embed()
        try:
            output = check_output(command.split(), stderr=STDOUT).decode("utf-8")
            embed.description = f"```py\n{output}\n```"
            embed.colour = Colour.green()
        except Exception as error:
            embed.description = f"```py\n{error.__class__.__name__}: {error}\n```"
            embed.colour = Colour.red()
        await interaction.response.send_message(embed=embed)

    @eval_slash.command(name="sql", description="executes a sql query")
    @app_commands.describe(query="the sql query to query")
    async def sql_slash(self, interaction: Interaction, *, query: str):
        embed = Embed()
        query_plain = query.data.removeprefix("```sql").removesuffix("```")
        async with self.bot.pool.acquire() as conn:
            try:
                res = await conn.fetch(query_plain)
            except Exception:
                embed.colour = Colour.red()
                embed.description = f"```py\n{format_exc()}```"
                return
        if res:
            embed.description = f"```sql\n{res}```"
            embed.colour = Colour.green()
        else:
            embed.description = "No results to fetch."
            embed.colour = Colour.purple()

    @eval_slash.command(name="python", description="evaluates python code")
    async def python_slash(self, interaction: Interaction):
        await interaction.response.send_modal(Evaluate())


async def setup(bot):
    await bot.add_cog(Owner_Cog(bot), guild=Object(id=default_guild))


"""
initial_extensions = ["cogs.help","cogs.events","cogs.users","cogs.roles"]
cogs = []
for entry in initial_extensions:
    cog = entry.strip('"').split('.')[1]
    Choice(name=cog.title(), value=entry),
    cogs.append(choice)
print(cogs)
cogs = [cog.strip('"').split('.')[1] for cog in initial_extensions]
cogs = [Choice(name=cog.split('.')[1].title(),value=cog) for cog in self.bot.initial_extensions]
initial_extensions = ["cogs.help","cogs.events","cogs.users","cogs.roles"]
print(cogs = [Choice(name=cog.split('.')[1].title(),value=cog) for cogin initial_extensions])
"""
