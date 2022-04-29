from collections import Counter
from re import findall
from typing import Optional, Union

from discord import Embed, Guild, Interaction, Member, Role, User, Webhook
from discord.abc import GuildChannel
from discord.ext.commands import Context
from discord.http import MultipartParameters


async def webhook_constructor(
    bot, url: str, embed: Embed, name: str = None, edit: bool = False
):
    webhook = Webhook.from_url(url, session=bot.session)
    sent = await webhook.send(
        wait=True,
        username=bot.user.name if name is not None else name,
        embed=embed,
    )
    if edit == True:
        return sent


async def send_json(
    json_: dict,
    bot,
    channel_id: int = None,
    interaction: Union[Interaction, Context] = None,
):
    if channel_id is None:
        channel_id = interaction.channel.id
    payload = MultipartParameters(payload=json_, files=None, multipart=None)
    await bot.http.send_message(channel_id, payloads=payload)


def perm_format(perm):
    return perm.replace("_", " ").replace("guild", "server").title()


def shorten_message(message, max_length: Optional[int]):
    if len(message) > max_length:  # 2048
        return message[:max_length] + "..."
    else:
        return message


def tag_format(
    payload: str,
    member: Union[Member, User],
    guild: Guild,
    role: Role,
    channel: GuildChannel,
):
    tags = {
        # member tags
        "{member.name}": member.name,
        "{member.discriminator}": member.discriminator,
        "{member.id}": str(member.id),
        "{member.mention}": member.mention,
        "{member.avatar}": member.avatar.url,
        "{member.avatar.png}": member.avatar.with_format("png"),
        "{member.avatar.gif}": member.avatar.with_format("gif"),
        "{member.avatar.jpeg}": member.avatar.with_format("jpeg"),
        "{member.display_avatar}": member.display_avatar.url,
        "{member.display_avatar.png}": member.display_avatar.with_format("png"),
        "{member.display_avatar.gif}": member.display_avatar.with_format("gif"),
        "{member.display_avatar.jpeg}": member.display_avatar.with_format("jpeg"),
        # channel tags
        "{channel.name}": channel.name,
        "{channel.id}": str(channel.id),
        "{channel.mention}": channel.mention,
        # guild tags
        "{guild.name}": guild.name,
        "{guild.id}": str(guild.id),
        "{guild.mention}": guild.mention,
        "{guild.owner}": guild.owner,
        "{guild.owner.mention}": guild.owner.mention,
        "{guild.owner.name}": guild.owner.name,
        "{guild.owner.discriminator}": guild.owner.discriminator,
        "{guild.owner.id}": str(guild.owner.id),
        "{guild.owner.avatar}": guild.owner.avatar.url,
        "{guild.owner.avatar.png}": guild.owner.avatar.with_format("png"),
        "{guild.owner.avatar.gif}": guild.owner.avatar.with_format("gif"),
        "{guild.owner.avatar.jpeg}": guild.owner.avatar.with_format("jpeg"),
        "{guild.owner.display_avatar}": guild.owner.display_avatar.url,
        "{guild.owner.display_avatar.png}": guild.owner.display_avatar.with_format(
            "png"
        ),
        "{guild.owner.display_avatar.gif}": guild.owner.display_avatar.with_format(
            "gif"
        ),
        "{guild.owner.display_avatar.jpeg}": guild.owner.display_avatar.with_format(
            "jpeg"
        ),
        "{guild.icon}": guild.icon_url,
        "{guild.icon.png}": guild.icon_url.with_format("png"),
        "{guild.icon.gif}": guild.icon_url.with_format("gif"),
        "{guild.icon.jpeg}": guild.icon_url.with_format("jpeg"),
        # role tags
        "{role.name}": role.name,
        "{role.id}": str(role.id),
        "{role.mention}": role.mention,
        "{role.color}": str(role.color),
        "{role.color.hex}": role.color.hex(),
        "{role.created_at}": role.created_at.strftime("%Y-%m-%d %H:%M:%S"),
        "{role.created_at.year}": role.created_at.year,
        "{role.created_at.month}": role.created_at.month,
        "{role.created_at.day}": role.created_at.day,
        "{role.created_at.hour}": role.created_at.hour,
        "{role.created_at.minute}": role.created_at.minute,
        "{role.created_at.second}": role.created_at.second,
        "{role.created_at.microsecond}": role.created_at.microsecond,
        "{role.created_at.timestamp}": role.created_at.timestamp(),
        "{role.display_icon}": role.display_icon.url,
        "{role.display_icon.png}": role.display_icon.with_format("png"),
        "{role.display_icon.gif}": role.display_icon.with_format("gif"),
        "{role.display_icon.jpeg}": role.display_icon.with_format("jpeg"),
        "{role.hoist}": str(role.hoist),
        "{role.mentionable}": str(role.mentionable),
        "{role.permissions}": str(role.permissions),
        "{role.position}": str(role.position),
        "{role.tags}": str(role.tags),
        "{role.unicode_emoji}": str(role.unicode_emoji),
        # message tags
        "{message.id}": str(payload.id),
        # emoji tags
        "{emoji.name}": payload.split(":")[2],
        "{emoji.id}": payload.split(":")[1],
        "{emoji.url}": payload.split(":")[0],
    }
    for tag, val in tags.items():
        payload = payload.replace(tag, val)
    return shorten_message(payload)


async def parent(ctx):
    group_commands = []
    for subcommand in ctx.command.commands:
        command_string = f"{ctx.prefix + subcommand.qualified_name}"
        group_commands.append(command_string)
    response = await ctx.reply(
        embed=Embed(
            title=f"Commands in `{ctx.command.name}`",
            description=", ".join(group_commands),
        ),
        delete_after=30,
    )
    invocation = response.reference.resolved
    await invocation.delete(delay=30)


async def interaction_or_context(arg_type, transaction, object_arg, ephemeral=False):
    if arg_type == "MEMBER":
        if isinstance(transaction, Interaction):
            member = transaction.user if object_arg is None else object_arg
        elif isinstance(transaction, Context):
            member = transaction.author if object_arg is None else object_arg
        return member
    elif arg_type == "ROLE":
        if isinstance(transaction, Interaction):
            # role = object_arg or transaction.user.top_role
            role = transaction.user.top_role if object_arg is None else object_arg
        elif isinstance(transaction, Context):
            # role = object_arg or transaction.user.top_role
            role = transaction.author.top_role if object_arg is None else object_arg
        return role
    elif arg_type == "SEND":
        if isinstance(object_arg, Embed):
            if isinstance(transaction, Interaction):
                await transaction.response.send_message(
                    embed=object_arg, ephemeral=ephemeral
                )
            elif isinstance(transaction, Context):
                await transaction.reply(embed=object_arg)
        else:
            if isinstance(transaction, Interaction):
                await transaction.response.send(content=object_arg, ephemeral=ephemeral)
            elif isinstance(transaction, Context):
                await transaction.reply(content=object_arg)
    elif arg_type == "CHANNEL":
        return transaction.channel if object_arg is None else object_arg


def _emoji_counter_(guild):
    emoji_stats = Counter()
    for emoji in guild.emojis:
        if emoji.animated:
            emoji_stats["animated"] += 1
            emoji_stats["animated_disabled"] += not emoji.available
        else:
            emoji_stats["regular"] += 1
            emoji_stats["disabled"] += not emoji.available

        fmt = f'Regular: {emoji_stats["regular"]}/{guild.emoji_limit} |     Animated: {emoji_stats["animated"]}/{guild.emoji_limit}'
        if emoji_stats["disabled"] or emoji_stats["animated_disabled"]:
            fmt = f'{fmt} Disabled: {emoji_stats["disabled"]} regular, {emoji_stats["animated_disabled"]} animated\n'

        fmt = f"{fmt} | Total Emojis: {len(guild.emojis)}/{guild.emoji_limit*2}"

    return fmt
