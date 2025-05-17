import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
from src import commands as movie_commands
import logging

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    logging.info(f"Zalogowano jako {bot.user}")


movie_commands.setup(bot)

bot.run(TOKEN)
