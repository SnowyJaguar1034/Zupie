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
import traceback
from logging import (
    CRITICAL,
    DEBUG,
    ERROR,
    INFO,
    WARN,
    FileHandler,
    Formatter,
    StreamHandler,
    basicConfig,
    getLogger,
)
from logging.handlers import SMTPHandler

# Bulit in Imports
from os import environ

import rust

# Package Imports
from discord import Activity, ActivityType, Intents
from discord.ext import commands
from dotenv import load_dotenv

from classes.config import Config

# Custom Imports
from classes.zupie import Zupie
from configuration import activity, backend

load_dotenv()

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

# recipients = Config().RECIPIENTS.strip(" ").split(",")

basicConfig(level=DEBUG)
logger = getLogger()
# logger.setLevel(logging.DEBUG)
file = FileHandler(filename="zupie.log", encoding="utf-8", mode="w")
file.setFormatter(
    Formatter(
        """
      Time: %(asctime)s: 
      Level: %(levelname)s: 
      Logger: %(name)s: 
      Path: %(pathname)s: 
      Line: %(lineno)d:
      Function: %(funcName)s:
      Message: %(message)s
      """
    )
)
console = StreamHandler()
console.setLevel(INFO)
console.setFormatter(
    Formatter("%(asctime)s: %(levelname)s: %(name)s: (%(funcName)): %(message)s")
)
mailer = SMTPHandler(
    mailhost=(Config().MAIL_HOST, Config().MAIL_PORT),
    fromaddr=Config().MAIL_FROM,
    toaddrs=Config().RECIPIENTS.strip(" ").split(","),  # recipients,
    subject=Config().MAIL_SUBJECT or f"Zupie encountered an error",
    credentials=(Config().MAIL_USER, Config().MAIL_PASS),
    secure=(),
    timeout=Config().MAIL_TIMEOUT,
)
mailer.setLevel(INFO)
mailer.setFormatter(
    Formatter(
        """
      Time: %(asctime)s: 
      Level: %(levelname)s: 
      Logger: %(name)s: 
      Path: %(pathname)s:
      Function: %(funcName)s:
      Message: %(message)s
      <!DOCTYPE html>
      <html>
         <body>
            <h1 style="color:SlateGray;">This is an HTML Email!</h1>
         </body>
      </html>
      """
    )
)
logger.addHandler(file)
logger.addHandler(console)
logger.addHandler(mailer)

log = getLogger(__name__)

if __name__ == "__main__":
    asyncio.run(bot.main())
