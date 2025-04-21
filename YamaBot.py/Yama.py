import discord
from discord.ext import commands
import asyncio
import os
from datetime import timedelta
from dotenv import load_dotenv
load_dotenv()

# Use dotenv if storing token in a .env file (recommended)
# from dotenv import load_dotenv
# load_dotenv()

intents = discord.Intents.default()
intents.message_content = True
intents.members = True  # Required for timeouts
bot = commands.Bot(command_prefix='!', intents=intents)

banned_words = ['tanga', 'bobo', 'tite']
warn_counts = {}  # {user_id: count}

@bot.event
async def on_ready():
    print(f'✅ Logged in as {bot.user}')

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    content = message.content.lower()
    for word in banned_words:
        if word in content:
            await message.delete()
            await message.channel.send(f"{message.author.mention}, Tanga Bawal mag mura.")
            
            # Add warning
            user_id = message.author.id
            warn_counts[user_id] = warn_counts.get(user_id, 0) + 1
            count = warn_counts[user_id]

            # Log to mod-logs channel if exists
            log_channel = discord.utils.get(message.guild.text_channels, name="mod-logs")
            if log_channel:
                await log_channel.send(f"⚠️ {message.author} was warned (#{count}) for saying: `{word}`")

            # Timeout user after 3 warnings
            if count >= 3:
                try:
                    duration = 5  # seconds
                    await message.author.timeout(discord.utils.utcnow() + timedelta(seconds=duration), reason="Used banned words repeatedly")
                    await message.channel.send(f"{message.author.mention} has been timed out for repeated violations.")
                    if log_channel:
                        await log_channel.send(f"⛔ {message.author} was timed out for 60 seconds.")
                except Exception as e:
                    print(f"Error timing out user: {e}")
            break

    await bot.process_commands(message)

# Run your bot (use environment variable or paste your new token directly here if testing)
bot.run(os.getenv("DISCORD_BOT_TOKEN"))

