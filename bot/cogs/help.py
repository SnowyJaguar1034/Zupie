from discord import Embed
from discord.ext.commands import MinimalHelpCommand, Cog

class MyNewHelp(MinimalHelpCommand):
    
    async def send_pages(self):
        destination = self.get_destination()
        for page in self.paginator.pages:
            emby = Embed(description=page)
            await destination.send(embed=emby)

    async def send_command_help(self, command):
        embed = Embed(title=self.get_command_signature(command))
        command_has_alias = command.aliases
        command_has_help = command.help
        if command_has_help:
          embed.add_field(name="Help", value=command.help)
        if command_has_alias:
          embed.add_field(name="Aliases", value=", ".join(command.aliases), inline=False)

        channel = self.get_destination()
        await channel.send(embed=embed)
    
    async def send_error_message(self, error):
        embed = Embed(title="Error", description=error)
        channel = self.get_destination()
        await channel.send(embed=embed)

class Help_Cog(Cog, name="help", description="Shows the custom help menu"):
    def __init__(self, bot):
      self.bot = bot
      self.bot.help_command = MyNewHelp()

async def setup(bot):
    await bot.add_cog(Help_Cog(bot))