from datetime import datetime
from traceback import format_exc
from typing import Sequence, Union

from discord import (CategoryChannel, Colour, Embed, Interaction, Member,
                     Message, NotFound, Object, Role, StageChannel,
                     TextChannel, User, VoiceChannel, app_commands)
from discord.ext.commands import Context
from helpers import interaction_or_context

from main import bot as bot_var
