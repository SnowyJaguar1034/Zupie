# Zupie
Zupie is a multipurpose [discord.py](https://github.com/Rapptz/discord.py) bot.

![Core Dev](https://dcbadge.vercel.app/api/shield/365262543872327681?theme=clean&logoColor=presence)
![Zupie](https://dcbadge.vercel.app/api/shield/bot/941314754851524639?theme=clean&logoColor=presence)
<br/>
[![Discord](https://discord.com/api/guilds/607652789304164362/widget.png)](https://discord.com/api/guilds/607652789304164362/widget.png)
[![License](https://img.shields.io/badge/License-BSD_3--Clause-blue.svg)](https://opensource.org/licenses/BSD-3-Clause)
[![Codacy Badge](https://app.codacy.com/project/badge/Grade/e531e880aad44149984ee41561918ad2)](https://www.codacy.com/gh/SnowyJaguar1034/Zupie/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=SnowyJaguar1034/Zupie&amp;utm_campaign=Badge_Grade)
[![](https://github.com/SnowyJaguar1034/Zupie/workflows/CI/badge.svg)](https://github.com/SnowyJaguar1034/Zupie/actions?query=workflow%3ACI) 
[![Maintainability](https://api.codeclimate.com/v1/badges/e3285d0b5cdca4998b2e/maintainability)](https://codeclimate.com/github/SnowyJaguar1034/Zupie/maintainability)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](https://makeapullrequest.com)
![Open pull requests](https://img.shields.io/github/issues-pr/SnowyJaguar1034/Zupie)
![Open issues](https://img.shields.io/github/issues/SnowyJaguar1034/Zupie)
![Code size in bytes](https://img.shields.io/github/languages/code-size/SnowyJaguar1034/Zupie)
![Repo language count](https://img.shields.io/github/languages/count/SnowyJaguar1034/Zupie)


## Table of Contents

- [What is Zupie](#what-is-zupie)
- [Questions](#questions)
- [Self Hosting](#self-hosting)<br/>
&nbsp;- [Prerequisites](#prerequisites)<br/>
&nbsp;- [Installing the source](#installing-the-source)<br/>
&nbsp;- [Setup](#setup)<br/>
&nbsp;&nbsp;- [Setup: `config.py`](https://github.com/SnowyJaguar1034/Zupie#configpy-file)<br/>
&nbsp;&nbsp;- [Setup: `.env`](https://github.com/SnowyJaguar1034/Zupie#env-file)<br/>
&nbsp;&nbsp;- [Setup: Module Installation](#installing-the-modules)<br/>
&nbsp;- [Running the bot](#running-the-bot)<br/>
- [Planned Plugins](#planned-plugins)
- [Contributing](#contributing)
&nbsp;- [Issues & Bugs](#issues-and-bugs)<br/>
&nbsp;- [Pull Requests](#pull-requests)<br/>
&nbsp;&nbsp;- [Pull Requests: Header](#header)<br/>
&nbsp;&nbsp;- [Pull Requests: Body](#body)<br/>
&nbsp;&nbsp;- [Pull Requests: Footer](#footer)<br/>
&nbsp;- [Development Environment](#development-environment)<br/>
- [Code of Conduct](#code-of-conduct)
- [License](#license)

## What is Zupie

## Questions

Have a question? Please avoid opening [issues](https://github.com/SnowyJaguar1034/Zupie/issues) for general questions. Instead, it is much better to
ask your question on our [Discord server](https://discord.gg/).

## Self Hosting
This self-hosting guide requires you to have some basic knowledge about [command line](https://www.computerhope.com/jargon/c/commandi.htm), [Python](https://www.python.org/), and Discord bots. We do not provide any official support for self-hosting.
### Prerequisites

In order to run Zupie, you will need to install the following software.

- [Git](https://git-scm.com)
- [Python 3](https://www.python.org/downloads/)
- [PostgreSQL](https://www.postgresql.org/download/)
<!-- - [Redis](https://redis.io/download/)-->
### Installing the source

Please fork this repository so that you can make pull requests. Then, clone your fork.

```sh
git clone https://github.com/<github-username>/zupie.git
```

Sometimes you may want to merge changes from the upstream repository to your fork.

```sh
git checkout master
git pull https://github.com/chamburr/modmail.git master
```
### Setup

Configuration is done through a `config.py` and `.env` file. 

#### `config.py` file

You should make a copy of `config-example.py` and rename it to `config.py`. All fields marked with`FILL` must be filled in with the type specfied below:
- `CLIENT_ID` : Your bot client secret as found on the [Discord Developer Portal](https://discord.com/developers/applications)
- `backend : Owners` : The ID(s) of the bots owners, these members have access to owner specfic commands
- `backend : Admins` : The ID(s) of the bots admins, these members have access to admin specfic commands
- `join_channel` : The channel ID of where the bot will send logs of it  joining/leaving a server.
- `admin_channel` : The channel ID of where the bot will send logs when Admins/Owners use a backend command.
- `database : database` : The name of your postgres database
- `database : user` : The name of user account the bot can use to access your postgres database.
- `database : host` : The host addresses of your databse, if it's running on your local machine this will be `localhost`
- `database : port` : The network port of your postgres database, postgres defualts to `5432`.

#### `.env` file

You should make a copy of `example.env` and rename it to `.env`. All fields marked with`FILL` must be filled in with the type specfied below:
- `TOKEN` : Your bots token as found on the [Discord Developer Portal](https://discord.com/developers/applications)
- `CLIENT_ID` : Your bot client ID as found on the [Discord Developer Portal](https://discord.com/developers/applications)
- `DEFAULT_GUILD` : The ID of your bots default guild / the ID of the only guild it's in
- `ACTIVITY`: The message you want your bot to show on it's profile
- `STATUS_WEBHOOK` : The URL of the webhook your bot will use to send status updates (shard connections/disconnections/restarts)

#### Installing the Modules

Zupie utilises [discord.py](https://github.com/Rapptz/discord.py) and several other modules to function properly. The list of modules can be found in `requirements.txt` and you can install them with the following command.

```sh
pip3 install -r requirements.txt
```
### Running the bot

Congratulations! You have set up everything and you can finally have the bot up and running. Use the following command to run.

```sh
(env) <Your source directory>: python main.py
```
## Planned Plugins

### Web Dashboard
The dashboard will allow users to control almost everyhting about the bot from outside of discord. The dashboard will be written in Python using the FastAPI library.
### Embed builder
This will let users create embeds json which will be stored in the db for later use in other plugins. This will mostly take the form of modal/form responses for the discord side of things but will also accept raw json input if someone has built a embed on a different platform and wants to import it. The [Dashbaord](#web-dashboard) will also include a page which connects to the embed builder so users can create their embeds outside of discord if they prefer.

### starboard
This feature is going to be similar to most starboards in other bots. It's a feature idea that I really quite like so will aim to include in Zupie. I attempted a starboard on my private bot howver it had a few probblems that I just never had time to fix, this is the code if anyones intrestedin taking a look
```py
@commands.Cog.listener()
async def on_raw_reaction_add(self, payload):
    data = await self.bot.get_data(payload.guild_id) # Accessing data from main table
    starboard = self.bot.get_channel(data[27]) # Pulling the starboard ID from main table and making it a channel object
    stars = await self.bot.get_star(payload.message_id) # Accessing from the starboard table
    #star_reactions = ["⭐", ":questionable_star:", ":star_struck:", ":star2:", ":StarPiece:", ":purple_star:"] # Listing the approved reactions to watch for
    reactions_count = stars[3] # Inilizing a reaction count
    with starboard.typing():
        for star in self.bot.config.star_reactions: # Checking each option in the approved reactions
            if payload.emoji.name == star: # Checking if the reaction used is in the approved list
                stared_message = await self.bot.get_channel(payload.channel_id).fetch_message(payload.message_id) # Getting the the original msg as a message object

                if not stared_message.author.bot and payload.member.id != stared_message.author.id: # Checking the person adding the reaction isn't a bot and/or that they aren't the person who sent the orginal message.
                    reactions_count = stars[1] + 1

                    # Declaring the Embed to post in the starboard channel
                    embed = discord.Embed(title = f"Starred message", description = f"{stared_message.content}" or "See attachment", colour = stared_message.author.colour, url = stared_message.jump_url, timestamp = datetime.datetime.utcnow())
                    if len(stared_message.attachments): # Checking if the orignal message contained a image
                        embed.set_image(url = stared_message.attachments[0].url) # Add the orginal msgs image to the embed
                    embed.set_author(name = stared_message.author, icon_url = stared_message.author.avatar_url)

                    if stared_message.id not in stars[0]: # Checking if the orignal message ID is NOT stored in the db
                        post = await starboard.send(embed = embed, content = f"Stars: {str(reactions_count)}") # Sending the embed to the starboard
                        async with self.bot.pool.acquire() as conn:
                            await conn.execute("UPDATE starboard SET Stared=$1 WHERE Post=$2, Count=$3", stared_message.id, post.id, reactions_count)
                    else:
                        temp = discord.Object(stars[2])
                        post = await self.bot.get_channel(starboard.id).fetch_message(temp) # Getting the the post msg as a message object
                        async with self.bot.pool.acquire() as conn:
                            await conn.execute("UPDATE starboard SET Count=$1", reactions_count)
                        await post.edit(embed = embed, content = f"Stars: {str(reactions_count)}")
                    
                else:
                    await stared_message.remove_reaction(payload.emoji, payload.member)
```
### Counting
I have this feature on my private bot, it works well so I will probably port it over but I'm still on the fence as this will require Zupie having the privledge message intent which I'm sure compllelty sure I want.

### Logging
I aim to add a logging plugin to Zupie which will log message deletions/edits, member join/leaves/updates, bot join/leaves etc
**Note**: All logs will be sent via webhooks for better performance, I don't want to be having to do a API call to fetch a log channel via ID each time I send a log and this also gives the user more control on where they want the logs sent as they can just change the webhook destination channel in their server settings.

### Moderation
I'm still on the fence on a full pledged moderation plugin howver the bot will most likley include `ban`, `kick`, `warn` and `timeout` commands.
#### Raidmode
This is a sub feature of the moderation plugin which I have working on my private bot so I'll most likley port this over, maybe with a few tweaks.

### Music & Leveling
There won't be a music or leveling plugin in Zupie, at least not for while and probarbly not written by me. I think there's more than enough music/leveling bots out there even after Rythm and Grrovy shut down and I really don't think the community needs another one. I've also seen bots have instability issues with music plugins (looking at Mee6 & Carl-bot). If a music plugin was to be added then i think I would want it to be a premium or patron feature to reduce the amount of potential users.

### Reminders
A reminders plugin is definatly somehting I am intreted in adding to Zupie, I just need to figure out a way to process them that won't purge them if the bot gets restarted however safeguarding the reminders won't be added to the plugin immediately.

### Custom Commands Plugin
I'm intrested in adding in a feature that lets server owners/admins/mods create custom commands for their servers but I'm not sure how I'm going to implement such a feature. I had a look at how Carl-bot is doing it using [JonSnowbd's](https://github.com/JonSnowbd/TagScript) or [PhenoM4n4n's](https://github.com/phenom4n4n/TagScript) TagScriptEngine and think one of those or somehting like them might be the way to go.

### Premium
I am definatly intrested in adding some paid for features. I'm not looking to lock entire plugins behind a paywall (other than a [music](#music--leveling) one) but rather premium will give servers addional parts of existing plugins like one or two extra starboards and counting channels and it will give patrons extra features on any server they share with the bot (not sure what those might be yet).


## Contributing

**Working on your first Pull Request?** You can learn how from this *free* series [How to Contribute to an Open Source Project on GitHub](https://kcd.im/pull-request)

Hi, thanks for your interest in contributing to Zupie! We'd love your help to make Zupie even
better than it is today. there are many ways you can contribute to this project:

- [Submitting bugs and feature requests](https://github.com/SnowyJaguar1034/Zupie/issues)
- [Reviewing changes](https://github.com/SnowyJaguar1034/Zupie/pulls)
- [Contribute directly to the code base](https://github.com/SnowyJaguar1034/Zupie/pulls)
- Sponsoring the project (Please let SbowyJaguar#1034 know on Discord)

For more information on contributing, please see the [contributing guidelines](#contributing-guide).

The issue tracker here is only for bug reports and feature requests. Please do not use it to ask a question. Instead, ask it on our [Discord server](https://discord.gg/).

### Issues and Bugs

We track bugs and features using the GitHub issue tracker. If you come across any bugs or have
feature suggestions, please let us know by submitting an issue, or even better, making a pull
request.

### Pull Requests

Please follow these guidelines related to submitting a pull request.

Please follow our commit conventions below. For subsequent commits to a pull request, it is okay not
to follow them, because they will be eventually squashed.

We follow the [Conventional Commits](https://www.conventionalcommits.org) to allow for more readable
messages in the commit history.

The commit message must follow this format:

```
<type>(<scope>): <description>
<BLANK LINE>
<body>
<BLANK LINE>
<footer>
```

Additionally, the maximum length of each line must not exceed 72 characters.
#### Header

The header is mandatory.

The type must be one of the following, the scope is optional and can be decided at your discretion.

- `build`: Changes to the build system or dependencies.
- `ci`: Changes to our CI configuration files and scripts.
- `chore`: Miscellaneous change.
- `docs`: Changes only the documentation.
- `feat`: Implements a new feature.
- `fix`: Fixes an existing bug.
- `perf`: Improves the performance of the code.
- `refactor`: Changes to code neither fixes a bug nor adds a feature.
- `style`: Changes to code that do not affect its functionality.
- `test`: Adding missing tests or correcting existing tests.

#### Body

The body is optional and can contain additional information, such as motivation for the commit.

#### Footer

The footer is optional and should contain any information about breaking changes. It is also the
place to reference GitHub issues that the commit closes.

Breaking changes should start with `BREAKING CHANGE:` with a space or two newlines. The rest of the
commit message is then used for explaining the change.
### Development Environment

To set up your development environment, follow the [self-hosting
guide here](#self-hosting). When you successfully
self-host the bot, your development environment should more or less be ready.
## Code of Conduct

## License

This project is licensed under the [BSD 3-Clause License](https://opensource.org/licenses/BSD-3-Clause)

<!-- [![Anurag's GitHub stats](https://github-readme-stats.vercel.app/api?username=SnowyJaguar1034)](https://github.com/anuraghazra/github-readme-stats) -->

