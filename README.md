# Zupie
Zupie is a multipurpose [discord.py](https://github.com/Rapptz/discord.py) bot.

## Table of Contents

- [What is Zupie](#what-is-zupie)
- [Questions](#questions)
- [Self Hosting](#self-hosting)<br/>
&nbsp;- [Self Hosting: Prerequisites](#prerequisites)<br/>
&nbsp;- [Self Hosting: Installing the source](#installing-the-source)<br/>
&nbsp;- [Self Hosting: Setup](#setup)<br/>
&nbsp;&nbsp;- [Self Hosting: Setup: config.py](https://github.com/SnowyJaguar1034/Zupie#configpy-file)<br/>
&nbsp;&nbsp;- [Self Hosting: Setup: `.env`](https://github.com/SnowyJaguar1034/Zupie#env-file)<br/>
&nbsp;&nbsp;- [Self Hosting: Setup: Module Installation](#installing-the-modules)<br/>
&nbsp;- [Self Hosting: Running the bot](#running-the-bot)<br/>
- [Contributing](#contributing)
&nbsp;- [Contributing: Issues & Bugs](#issues-and-bugs)<br/>
&nbsp;- [Contributing: Pull Requests](#pull-requests)<br/>
&nbsp;&nbsp;- [Contributing: Pull Requests: Header](#header)<br/>
&nbsp;&nbsp;- [Contributing: Pull Requests: Body](#body)<br/>
&nbsp;&nbsp;- [Contributing: Pull Requests: Footer](#footer)<br/>
&nbsp;- [Contributing: Development Environment](#development-environment)<br/>
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

## Contributing
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

<!-- [![Anurag's GitHub stats](https://github-readme-stats.vercel.app/api?username=SnowyJaguar1034)](https://github.com/anuraghazra/github-readme-stats) -->

