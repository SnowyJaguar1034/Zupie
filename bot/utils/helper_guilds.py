from main import bot as bot_var
from helpers import interaction_or_context

from typing import Union, Sequence
from datetime import datetime
from traceback import format_exc

from discord import Member, User, Interaction, Embed, app_commands, Role, TextChannel, VoiceChannel, StageChannel, CategoryChannel, Colour, Object, Message, NotFound
from discord.ext.commands import Context

