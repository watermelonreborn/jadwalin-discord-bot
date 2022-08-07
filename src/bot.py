# bot.py
import os
import random
import discord

from cogs import test, user

from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.environ.get("PRODUCTION_TOKEN")
PREFIX = os.environ.get("PRODUCTION_PREFIX")

if TOKEN == None:
    TOKEN = os.getenv("DISCORD_TOKEN")
    PREFIX = os.getenv("COMMAND_PREFIX")

bot = commands.Bot(command_prefix=PREFIX)
cogs = [test, user]

for cog in cogs:
    cog.setup(bot)

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game(name="with You"))
    print(f'{bot.user} has connected to Discord!')

bot.run(TOKEN)