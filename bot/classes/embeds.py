from datetime import datetime

from discord import Colour, Embed


class LogEmbed(Embed):
    def __init__(self, *args, **kwargs):
        if "timestamp" not in kwargs:
            kwargs["timestamp"] = datetime.utcnow()
        super().__init__(*args, **kwargs)


class PositiveEmbed(LogEmbed):
    def __init__(self, *args, **kwargs):
        if "colour" not in kwargs:
            kwargs["colour"] = Colour.dark_teal()
        super().__init__(*args, **kwargs)


class NegativeEmbed(LogEmbed):
    def __init__(self, *args, **kwargs):
        if "colour" not in kwargs:
            kwargs["colour"] = Colour.dark_magenta()
        super().__init__(*args, **kwargs)


class NeutralEmbed(LogEmbed):
    def __init__(self, *args, **kwargs):
        if "colour" not in kwargs:
            kwargs["colour"] = Colour.dark_orange()
        super().__init__(*args, **kwargs)
