initial_extensions  = [
	"cogs.users", 
]

owners =[
    "365262543872327681",
]

backend = {
    "Owners": ["365262543872327681",],
    "Admins": []
    
}

# Channels to send logs
join_channel = 816480943228452895
event_channel = 816480957288546314
admin_channel = 816480968830353458


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
    "connect", "speak", 
    "priority_speaker", 
    "use_voice_activation", 
    "stream", 
    "create_instant_invite", 
    "change_nickname",
    "mention_everyone"
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
    "mention_everyone"
]

# Invite strctures
invite_plain = "https://discord.com/api/oauth2/authorize?client_id=941314754851524639&permissions=1644971950071&scope=bot%20applications.commands"
invite_hyperlink = f"[Invite Wyvern](invite_plain)"

# Postgres DataBase credentials
database = {
    "database": "postgres",
    "user": "postgres",
    "password": "onapostitunderthekeyboard",
    "host": "localhost",
    "port": 5432
}

