from main import bot as bot_var

# from typing import Union, Sequence
# from datetime import datetime
# from traceback import format_exc

from discord import Interaction, Embed
from discord.ext.commands import Context

from collections import Counter


def perm_format(perm):
    return perm.replace("_", " ").replace("guild", "server").title()


def shorten_message(message):
    if len(message) > 2048:
        return message[:2045] + "..."
    else:
        return message


def user_tag_format(message, member):
    tags = {
        "{user_name}": member.name,
        "{user_tag}": member.discriminator,
        "{user_id}": str(member.id),
        "{user_mention}": member.mention,
    }
    for tag, val in tags.items():
        message = message.replace(tag, val)
    return shorten_message(message)


def channel_tag_format(message, channel):
    tags = {
        "{channel_name}": channel.name,
        "{channel_id}": str(channel.id),
        "{channel_mention}": channel.mention,
    }
    for tag, val in tags.items():
        message = message.replace(tag, val)
    return shorten_message(message)


def guild_tag_format(message, guild):
    tags = {
        "{guild_name}": guild.name,
        "{guild_id}": str(guild.id),
    }
    for tag, val in tags.items():
        message = message.replace(tag, val)
    return shorten_message(message)


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
        else:
            print("ERROR: interaction_or_context : Hit ele statemnt in 'MEMBER' check")
        return member
    elif arg_type == "ROLE":
        if isinstance(transaction, Interaction):
            # role = object_arg or transaction.user.top_role
            role = transaction.user.top_role if object_arg is None else object_arg
        elif isinstance(transaction, Context):
            # role = object_arg or transaction.user.top_role
            role = transaction.author.top_role if object_arg is None else object_arg
        else:
            print("ERROR: interaction_or_context : Hit ele statemnt in 'ROLE' check")
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
                print(
                    "ERROR: interaction_or_context : Hit ele statemnt in 'SEND.EMBED' check'"
                )
        else:
            if isinstance(transaction, Interaction):
                await transaction.response.send(content=object_arg, ephemeral=ephemeral)
            elif isinstance(transaction, Context):
                await transaction.reply(content=object_arg)
            else:
                print(
                    "ERROR: interaction_or_context : Hit ele statemnt in 'SEND.CONTENT' check"
                )
    elif arg_type == "CHANNEL":
        return transaction.channel if object_arg is None else object_arg
    else:
        print("ERROR: interaction_or_context : Hit final eele statemnt")


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
