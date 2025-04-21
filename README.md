# 🎵 Discord Music Bot

A simple yet powerful Discord music bot built using `discord.py` and `yt_dlp`. It lets you search and play songs from YouTube directly into your voice channel — with a queue, pause/resume, skip, and more.

## 🚀 Features

- 🔍 YouTube search & play with `yt_dlp`
- 📃 Music queue system
- ⏸ Pause, ▶️ Resume, ⏭ Skip, 🛑 Stop
- ⏳ Auto-disconnect after 5 minutes of inactivity
- 🎶 Plays high-quality audio using `ffmpeg`

---

## 🛠 Requirements

- Python 3.8+
- `ffmpeg` installed and in your system path
- A Discord Bot token ([create one here](https://discord.com/developers/applications))
- `yt_dlp` and `discord.py` installed

### Install Dependencies

```bash
pip install -U discord.py yt_dlp

⚙️ Setup
Clone this repo or download the files.

Set your bot token in the last line of the Python file:

bot.run('YOUR_DISCORD_BOT_TOKEN')
Make sure ffmpeg is installed and the path to the executable is correctly set in:

ffmpeg_path = r"path\to\your\ffmpeg.exe"

Run the bot:
python bot.py