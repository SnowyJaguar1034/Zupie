from discord.app_commands import Group
from discord.ext.commands import Cog

class CogBase(Group, Cog):
    def __init__(self, bot):
        super().__init__()
        self.bot = bot