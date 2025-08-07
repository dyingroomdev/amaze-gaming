import os
import asyncio
from dotenv import load_dotenv
from discord.ext import commands
import discord
from bot.utils.checks import is_mod_or_admin  # Correct import

# Load environment variables from .env
load_dotenv()
TOKEN = os.getenv("DISCORD_BOT_TOKEN")

if not TOKEN:
    raise ValueError("Discord bot token not found in environment variables. Please set DISCORD_BOT_TOKEN in your .env file")

# Set up bot with required intents
intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Amaze Gaming Bot is online as {bot.user}!")

# Optional: global check
@bot.check
async def global_check(ctx):
    return True

async def main():
    async with bot:
        # Load extensions with proper package paths
        extensions = [
            "bot.extensions.moderation",
            "bot.extensions.welcome",
            "bot.extensions.permissions",
            "bot.extensions.leveling",
            "bot.extensions.role_manager",
            "bot.extensions.say",
            "bot.extensions.utility",
            "bot.extensions.minecraft",
            "bot.extensions.fun",
            "bot.extensions.logging",
            "bot.extensions.dm_welcome"
            # Add others if needed
        ]

        for ext in extensions:
            print(f"[DEBUG] Loading extension: {ext}")
            await bot.load_extension(ext)

        print("[DEBUG] Starting bot...")
        await bot.start(TOKEN)

if __name__ == "__main__":
    asyncio.run(main())
