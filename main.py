import asyncio
import os
import logging
from dotenv import load_dotenv

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    filename="jobflow.log",
)

load_dotenv()
discord_token = os.getenv("DISCORD_TOKEN")
assert discord_token, "DISCORD_TOKEN not found!"

intern_channel_id = int(os.getenv("INTERN_CHANNEL_ID", "0"))
new_grad_channel_id = int(os.getenv("NEW_GRAD_CHANNEL_ID", "0"))
assert intern_channel_id != 0, "INTERN_CHANNEL_ID not found!"
assert new_grad_channel_id != 0, "NEW_GRAD_CHANNEL_ID not found!"

import discord
from discord.ext import commands, tasks
from discord.abc import Messageable

from src.database.database import Database
from src.scrapers.scraper_manager import ScraperManager

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

db = Database()
db.init_db()
manager = ScraperManager(db)


@tasks.loop(hours=8)
async def scrape_jobs():
    logging.info("Starting scheduled scrape...")
    loop = asyncio.get_event_loop()

    new_jobs = await loop.run_in_executor(None, manager.run)
    if not new_jobs:
        logging.info("No new jobs found.")
        return

    intern_channel = bot.get_channel(intern_channel_id)
    new_grad_channel = bot.get_channel(new_grad_channel_id)

    for job in new_jobs:
        embed = discord.Embed(
            title=job.title,
            url=job.application_url,
            color=discord.Color.blue(),
        )
        embed.add_field(name="Company", value=job.company, inline=True)
        embed.add_field(name="Location", value=job.location or "N/A", inline=True)
        embed.set_footer(text="via SimplifyJobs")

        if job.job_type == "intern" and isinstance(intern_channel, Messageable):
            await intern_channel.send(embed=embed)
        elif job.job_type == "new_grad" and isinstance(new_grad_channel, Messageable):
            await new_grad_channel.send(embed=embed)


@bot.event
async def on_ready():
    logging.info(f"Logged in as {bot.user}")
    scrape_jobs.start()


bot.run(discord_token)
