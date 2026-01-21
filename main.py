import os
import yt_dlp
from pyrogram import Client, filters
from pytgcalls import PyTgCalls
from pytgcalls.types.input_stream import AudioPiped

BOT_TOKEN = os.environ.get("BOT_TOKEN")
API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")

app = Client("shadow", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
call = PyTgCalls(app)

def download(song):
    ydl_opts = {
        "format": "bestaudio",
        "outtmpl": "song.mp3"
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([f"ytsearch:{song}"])
    return "song.mp3"

@app.on_message(filters.command("play") & filters.group)
async def play(_, msg):
    if len(msg.command) < 2:
        await msg.reply("Song name likho!")
        return
    song = msg.text.split(None, 1)[1]
    await msg.reply("Downloading 🎧...")
    file = download(song)
    await call.join_group_call(msg.chat.id, AudioPiped(file))
    await msg.reply(f"Now Playing: {song}")

@app.on_message(filters.command("stop"))
async def stop(_, msg):
    await call.leave_group_call(msg.chat.id)
    await msg.reply("Stopped ❌")

app.start()
call.start()
print("Shadow Music Bot is running...")
import time
while True:
    time.sleep(5)
