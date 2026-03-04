# JobFlow

A Discord bot that scrapes software engineering job listings and posts them to your server automatically.

- Scrapes new internship and new grad listings every 8 hours
- Posts jobs to separate Discord channels by type (`intern` / `new_grad`)
- Tracks seen listings in a local SQLite database to avoid duplicate posts

## Setup

**1. Clone the repo**

```bash
git clone https://github.com/yourname/jobflow.git
cd jobflow
```

**2. Create a virtual environment and install dependencies**

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

**3. Create a `.env` file**

```
DISCORD_TOKEN=your_bot_token_here
INTERN_CHANNEL_ID=123456789
NEW_GRAD_CHANNEL_ID=987654321
```

**4. Run**

```bash
python main.py
```

## Discord Bot Setup

Refer to the [discord.py documentation](https://discordpy.readthedocs.io/en/stable/) for bot setup instructions.
