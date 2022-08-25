# bot.py
import asyncio
import discord
import os
import uvicorn
import threading

from cogs import test, user
from models.reminder import Reminder
from services.message_service import MessageService
from services.guild_service import GuildService

from discord.ext import commands
from dotenv import load_dotenv
from fastapi import FastAPI
from typing import List

load_dotenv()
TOKEN = os.environ.get("PRODUCTION_TOKEN")
PREFIX = os.environ.get("PRODUCTION_PREFIX")

if TOKEN == None:
    TOKEN = os.getenv("DISCORD_TOKEN")
    PREFIX = os.getenv("COMMAND_PREFIX")

app = FastAPI()
bot = commands.Bot(command_prefix=PREFIX)

cogs = [test, user]
for cog in cogs:
    cog.setup(bot)

@app.post('/reminder')
async def reminder(reminders: List[Reminder]):
    asyncio.create_task(MessageService.send_reminder(reminders))
    return {'data': 'OK'}

@bot.event
async def on_ready():
    GuildService.bot = bot
    await bot.change_presence(activity=discord.Game(name="with You"))
    print(f'{bot.user} has connected to Discord!')

# TODO: Add keyboard interrupt for bot run or use .start
if __name__ == '__main__':
    threading.Thread(target=lambda: bot.run(TOKEN)).start()
    uvicorn.run(app, port=5000)
# bot.run(TOKEN)
