import os
import logging
from dotenv import load_dotenv

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    filename="jobflow.log"
)

load_dotenv()
discord_token = os.getenv("DISCORD_TOKEN")
intern_channel_id = os.getenv("INTERN_CHANNEL_ID")
new_grad_channel_id = os.getenv("NEW_GRAD_CHANNEL_ID")
assert discord_token, "DISCORD_TOKEN not found!"
assert intern_channel_id, "INTERN_CHANNEL_ID not found!"
assert new_grad_channel_id, "NEW_GRAD_CHANNEL_ID not found!"

import discord
from discord.ext import commands

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    channel = bot.get_channel(int(intern_channel_id))
    await channel.send("testing. is online")


bot.run(discord_token)
