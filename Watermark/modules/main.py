import os,time
from pyrogram import filters
import subprocess
from Watermark import app
from config import OWNER_ID
from Watermark.core.utils import progress_bar


def duration(filename):
    result = subprocess.run(["ffprobe", "-v", "error", "-show_entries",
                             "format=duration", "-of",
                             "default=noprint_wrappers=1:nokey=1", filename],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT)
    return float(result.stdout)


@app.on_message((filters.document | filters.video | filters.photo) & filters.private)
async def watcher(app, message):
    if message.photo or (message.document and message.document.mime_type.startswith("photo/")):
        photo = await message.download()
        await message.reply_text("Yes, it's a photo\nWait downloading...")
        await app.send_photo(chat_id=message.chat.id, photo=photo)
        
    elif message.video or (message.document and message.document.mime_type.startswith("video/")):
        video = await message.download()
        await message.reply_text("Yes, it's a video\nwait downloading...")     
        subprocess.run(f'ffmpeg -i "{video}" -ss 00:01:00 -vframes 1 "video.jpg"', shell=True)
        thumbnail = f"video.jpg"
        dur = int(duration(video))
        start_time = time.time() 
#        await app.send_video(chat_id=message.chat.id, video=video) 
        await app.send_video(chat_id=message.chat.id, video=video, caption=cc, supports_streaming=True, height=720, width=1280, thumb=thumbnail, duration=dur, progress=progress_bar, progress_args=(reply, start_time))    
        os.remove("video.jpg")        
    else:
        pass

