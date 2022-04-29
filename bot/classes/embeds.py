from datetime import datetime

from discord import Embed


class LogEmbed(Embed):
    def __init__(self, *args, **kwargs):
        if "timestamp" not in kwargs:
            kwargs["timestamp"] = datetime.utcnow()
        super().__init__(*args, **kwargs)
