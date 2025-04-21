import discord
from discord.ext import commands
import yt_dlp as youtube_dl
import asyncio
from dotenv import load_dotenv
load_dotenv()
import os

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)

# Music Queue (stores tuples of (url, title))
queue = []

# Async YouTube search
async def search_youtube(query):
    ydl_opts = {
        'format': 'bestaudio',
        'noplaylist': True,
        'quiet': True,
        'default_search': 'ytsearch',
        'extract_flat': False,
    }

    loop = asyncio.get_event_loop()
    try:
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info = await loop.run_in_executor(None, lambda: ydl.extract_info(f"ytsearch:{query}", download=False))
            if 'entries' in info and len(info['entries']) > 0:
                entry = info['entries'][0]
                return entry['webpage_url'], entry.get('title', 'Unknown Title')
            else:
                return None, None
    except Exception as e:
        print(f"[ERROR] YouTube Search: {e}")
        return None, None

# Connect to a voice channel
async def connect_to_voice(ctx):
    if not ctx.author.voice:
        await ctx.send("❗ You need to join a voice channel first!")
        return None
    return await ctx.author.voice.channel.connect()

# Play the next song in the queue
async def play_next(ctx, voice_client):
    if len(queue) == 0:
        await ctx.send("🎵 Queue ended. I'll stay in voice for 5 minutes in case you add more songs...")

        async def delayed_disconnect():
            await asyncio.sleep(300)
            if not voice_client.is_playing() and len(queue) == 0:
                await ctx.send("👋 No new songs added. Disconnecting now.")
                await voice_client.disconnect()

        bot.loop.create_task(delayed_disconnect())
        return

    url, title = queue.pop(0)
    ffmpeg_path = r"C:\Users\kevin\OneDrive\Desktop\Discord Bot\Discord-Bot-Yama\DiscordMUSICEXE\bin\ffmpeg.exe"

    ydl_opts = {
        'format': 'bestaudio/best',
        'quiet': True,
        'noplaylist': True,
    }

    loop = asyncio.get_event_loop()
    try:
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info = await loop.run_in_executor(None, lambda: ydl.extract_info(url, download=False))
            audio_url = info['url']
    except Exception as e:
        await ctx.send(f"❌ Failed to fetch audio: {e}")
        return

    ffmpeg_options = {
        'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
        'options': '-vn'
    }

    audio_source = discord.FFmpegPCMAudio(audio_url, executable=ffmpeg_path, **ffmpeg_options)
    source = discord.PCMVolumeTransformer(audio_source)

    def after_playing(error):
        if error:
            print(f"[ERROR] Playback: {error}")
        fut = asyncio.run_coroutine_threadsafe(play_next(ctx, voice_client), bot.loop)
        try:
            fut.result()
        except Exception as e:
            print(f"[ERROR] After Callback: {e}")

    voice_client.play(source, after=after_playing)
    await ctx.send(f"🎶 Now playing: **{title}**")

# Play command
@bot.command(name='play')
async def play(ctx, *, search: str):
    url, title = await search_youtube(search)

    if not url:
        await ctx.send("❌ Couldn't find anything on YouTube.")
        return

    voice_client = ctx.voice_client or await connect_to_voice(ctx)
    if not voice_client:
        return

    queue.append((url, title))

    if not voice_client.is_playing():
        await play_next(ctx, voice_client)
    else:
        await ctx.send(f"✅ Added to queue: **{title}**")

@bot.command(name='pause')
async def pause(ctx):
    vc = ctx.voice_client
    if vc and vc.is_playing():
        vc.pause()
        await ctx.send("⏸️ Music paused.")
    else:
        await ctx.send("❌ Nothing is playing right now.")

@bot.command(name='resume')
async def resume(ctx):
    vc = ctx.voice_client
    if vc and vc.is_paused():
        vc.resume()
        await ctx.send("▶️ Resumed playing.")
    else:
        await ctx.send("❌ Music is not paused.")

@bot.command(name='skip')
async def skip(ctx):
    vc = ctx.voice_client
    if vc and vc.is_playing():
        vc.stop()
        await ctx.send("⏭️ Skipped.")
    else:
        await ctx.send("❌ Nothing is playing to skip.")

@bot.command(name='stop')
async def stop(ctx):
    vc = ctx.voice_client
    if vc:
        queue.clear()
        await vc.disconnect()
        await ctx.send("🛑 Stopped and disconnected.")
    else:
        await ctx.send("❌ I'm not connected to a voice channel.")

# ⚠️ Replace this with your actual bot token
bot.run(os.getenv("DISCORD_BOT_TOKEN"))
