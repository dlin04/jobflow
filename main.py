import os
from dotenv import load_dotenv

load_dotenv()
discord_token = os.getenv("DISCORD_TOKEN")
assert discord_token, "DISCORD_TOKEN not found!"

import discord
from discord.ext import commands

# setup intents
intents = discord.Intents.default()
intents.message_content = True

# bot instance
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"logged in as {bot.user}")
    print("bot is online")

bot.run(discord_token)
