# 🎵 YamaBot - Discord Music Bot

YamaBot is a simple, powerful Discord music bot written in Python that plays music from YouTube using yt_dlp and discord.py.

---

## 🚀 Features

- ✅ Search and play music from YouTube  
- 📃 Queue system  
- ⏸️ Pause, ▶️ Resume, ⏭️ Skip, 🛑 Stop  
- 🎧 Auto disconnect after 5 min of inactivity  
- 🔒 Secure token via .env

---

## 📦 Requirements

- Python 3.9+  
- FFmpeg (installed or included)  
- A Discord Bot Token  
- Python packages:
  pip install -r requirements.txt

---

## ⚙️ Setup Instructions

1. Clone the repo:
   git clone https://github.com/KevinS4160/Discord-Bot-Yama.git
   cd Discord-Bot-Yama

2. Install dependencies:
   pip install -r requirements.txt

3. Create a `.env` file in the project folder with:
   DISCORD_TOKEN=your_token_here

4. Add FFmpeg:
   - Put the path in your script (MusicYama.py)
   - OR add FFmpeg to system PATH

5. Run the bot:
   python MusicYama.py

---

## ❗ GitHub Tips

- Add a `.gitignore`:

- Got secret push error? Remove your token from code & history, then recommit.

---

## 🧾 Bot Commands

!play <song name> – Plays a song  
!pause – Pauses current song  
!resume – Resumes music  
!skip – Skips current song  
!stop – Stops and disconnects

---

## 📄 License

MIT License

---

Made with 💻 by KevinS4160
