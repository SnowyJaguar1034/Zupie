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
