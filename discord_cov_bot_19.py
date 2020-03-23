from covid_parser import today, get_dates_by_type, increase_daily, countries
from discord.ext.tasks import loop
from discord.ext import commands

import asyncio

import os
import discord
from dotenv import load_dotenv

def info_message_std(country='Germany'):
    return (
        f"**COVID-19-Update**\n"
        f"🇩🇪 Deutschland:\n"
    ) + message_country(country) + (
        f"🌍 Welt:\n"
        f"  → **Heute** ({get_dates_by_type('deaths')[-1]}):\n"
        f"    😷 {today('confirmed')} bestätigte Infizierte (+{increase_daily('confirmed')}% im vgl. zum Vortag); "
        f"  💀 {today('deaths')} Todesfälle (+{increase_daily('confirmed')}% im vgl. zum Vortag)\n\n"
    )

def message_country(country):
    return (
        f"  → **Heute** ({get_dates_by_type('deaths')[-1]}):\n"
        f"    😷 {today('confirmed', country)} bestätigte Infizierte (+{increase_daily('confirmed', country)}% im vgl. zum Vortag)"
        f"  💀 {today('deaths', country)} Todesfälle (+{increase_daily('deaths', country)}% im vgl. zum Vortag)\n"
    )

print(info_message_std())


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
CHANNEL = os.getenv('CHANNEL_NAME')

bot = commands.Bot(command_prefix='!')

def get_channel(guild, name):
    for channel in guild.channels:
        if channel.name == name:
            return channel
    print('channel not found:', name)
    return None

@bot.event
async def on_ready():
    guild = discord.utils.get(bot.guilds, name=GUILD)
    covid19_channel = get_channel(guild, CHANNEL)
    
    with open('covid-icon.jpg', 'rb') as f:
        await bot.user.edit(avatar=f.read())
    print(
        f'{bot.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )

    await covid19_channel.send("\n**Hallo, ich bin der covid-19-info-bot.**\nMit **'!info'** holt Ihr die neusten Zahlen!\nInfos zu einem Land können mit **!country 'Country Name'** abgerufen werden (z.B. '!country Germany').\n")


@bot.command(name='info')
async def nine_nine(ctx):
    await ctx.send(info_message_std())

@bot.command(name='country')
async def nine_nine(ctx, arg):
    if arg not in countries():
        await ctx.send("Land nicht gefunden.")
    else:
        msg = message_country(country=arg)
        await ctx.send(f"{arg}:\n" + msg)

@loop(hours=24.0)
async def info_loop():
    msg = info_message_std()
    print(msg)
    await covid19_channel.send(msg)

@info_loop.before_loop
async def info_before():
    global covid19_channel
    await bot.wait_until_ready()
    guild = discord.utils.get(bot.guilds, name=GUILD)
    covid19_channel = get_channel(guild, CHANNEL)

info_loop.start()
bot.run(TOKEN)