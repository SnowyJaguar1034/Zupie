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


import asyncio
import logging
import traceback
# Bulit in Imports
from os import environ

from classes.config import Config
# Custom Imports
from classes.zupie import Zupie
from configuration import activity, backend
# Package Imports
from discord import Activity, ActivityType, Intents
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename=f"zupie.log", encoding="utf-8", mode="w")
console = logging.StreamHandler()
console.setLevel(logging.WARNING)
# mailer = logging.SMTPHandler(
#     mailhost=Config.MAIL_HOST,
#     fromaddr=Config.MAIL_FROM,
#     toaddrs=Config.MAIL_TO,
#     subject=Config.MAIL_SUBJECT,
#     credentials=(Config.MAIL_USER, Config.MAIL_PASS),
#     secure=Config.MAIL_SECURE,
#     timeout=Config.MAIL_TIMEOUT,
# )
# mailer.setLevel(logging.ERROR)
formatter = logging.Formatter("%(asctime)s: %(levelname)s: %(name)s: %(message)s")
test = logging.Formatter(
    """
    Time: %(asctime)s: 
    Level: %(levelname)s: 
    Logger: %(name)s: 
    Message: %(message)s
   """
)
handler.setFormatter(test)
console.setFormatter(formatter)
# mailer.setFormatter(formatter)
logger.addHandler(handler)
logger.addHandler(console)
# logger.addHandler(mailer)

log = logging.getLogger(__name__)

intents = Intents.all()
intents.message_content = True

bot = Zupie(
    intents=intents,
    activity=Activity(name=activity, type=ActivityType.playing),
    owner_ids=backend["Owners"],
    description=Config().DESCRIPTION,
    command_prefix=commands.when_mentioned,
    case_insensitive=True,
)

if __name__ == "__main__":
    asyncio.run(bot.main())
