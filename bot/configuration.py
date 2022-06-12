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

from os import getenv

from dotenv import load_dotenv

load_dotenv()

activity = f"Version {getenv('VERSION')}"

backend = {
    "Owners": [
        "365262543872327681",
    ],
    "Admins": [],
}

invite_plain = f"https://discord.com/api/oauth2/authorize?client_id={getenv('CLIENT_ID')}&permissions=1644971950071&scope=bot%20applications.commands"
invite_hyperlink = f"[Invite Zupie](invite_plain)"

initial_extensions = [
    "cogs.help",
    "cogs.events",
    "cogs.owners",
    "cogs.users",
    "cogs.roles",
    "cogs.code_snippets",
    "cogs.source",
    "cogs.events.calendar",
    "cogs.events.guilds",
    "cogs.events.intergrations",
    "cogs.events.invites",
    "cogs.events.messages",
    "cogs.events.shards",
    "cogs.events.threads",
    "cogs.events.users",
    "cogs.events.voices",
]


guild_perms = [
    "administrator",
    "manage_guild",
    "manage_webhooks",
    "manage_channels",
    "manage_roles",
    "manage_emojis",
    "manage_messages",
    "manage_nicknames",
    "view_audit_log",
    "view_guild_insights",
    "kick_members",
    "ban_members",
    "move_members",
    "deafen_members",
    "mute_members",
    "read_messages",
    "send_messages",
    "send_tts_messages",
    "embed_links",
    "attach_files",
    "read_message_history",
    "add_reactions",
    "external_emojis",
    "connect",
    "speak",
    "priority_speaker",
    "use_voice_activation",
    "stream",
    "create_instant_invite",
    "change_nickname",
    "mention_everyone",
]

key_perms = [
    "administrator",
    "manage_guild",
    "manage_roles",
    "manage_channels",
    "manage_messages",
    "manage_webhooks",
    "manage_nicknames",
    "manage_emojis",
    "kick_members",
    "mention_everyone",
]
