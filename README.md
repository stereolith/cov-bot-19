## cov-bot-19

A discord bot that gives information about COVID-19 cases.

Data source: [2019 Novel Coronavirus COVID-19 (2019-nCoV) Data Repository by Johns Hopkins CSSE](https://github.com/CSSEGISandData/COVID-19/).

### Config
The following environment variables are needed:
* `DISCORD_TOKEN`: Discord API token
* `DISCORD_GUILD`: Discord Guild name
* `CHANNEL_NAME`: Channel to post periodical updates in

### Usage
The bot posts new infos peroiodically (every 24h).

Commands:
* `!info`: Prints info about local and global cases
* `!country [COUNTRY_NAME]`: Prints info about a specific country