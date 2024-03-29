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

from datetime import datetime
from logging import getLogger

from discord import Colour, Embed

log = getLogger(__name__)


class BaseEmbed(Embed):
    def __init__(self, arg_dict: dict, *args, **kwargs):
        if arg_dict.key() not in kwargs:
            kwargs[arg_dict.key()] = arg_dict.value()
        super().__init__(*args, **kwargs)


class LogEmbed(Embed):
    def __init__(self, *args, **kwargs):
        super().__init__(arg_dict={"timestamp": datetime.utcnow()}, *args, **kwargs)


class PositiveEmbed(LogEmbed):
    def __init__(self, *args, **kwargs):
        super().__init__(arg_dict={"colour": Colour.dark_teal()}, *args, **kwargs)


class NegativeEmbed(LogEmbed):
    def __init__(self, *args, **kwargs):
        super().__init__(arg_dict={"colour": Colour.dark_magenta()}, *args, **kwargs)


class NeutralEmbed(LogEmbed):
    def __init__(self, *args, **kwargs):
        super().__init__(arg_dict={"colour": Colour.dark_orange()}, *args, **kwargs)
