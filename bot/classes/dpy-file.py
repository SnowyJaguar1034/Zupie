 file = discord.File(
    history, f"modmail_log_{tools.get_modmail_user(ctx.channel).id}.txt"
)

try:
    msg = await channel.send(embed, file=file)
except discord.Forbidden:
    return

log_url = msg.attachments[0].url[39:-4]
log_url = log_url.replace("modmail_log_", "")
log_url = [hex(int(some_id))[2:] for some_id in log_url.split("/")]
log_url = f"{self.bot.config.BASE_URI}/logs/{'-'.join(log_url)}"
embed.add_field("Message Logs", log_url, False)