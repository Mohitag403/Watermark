import os,time
from pyrogram import filters
import asyncio,threading 
import subprocess
from Watermark import app
from config import OWNER_ID
from Watermark.core.utils import progress_bar


async def dl_send(message):
    reply = await message.reply_text("Yes, it's a video\nwait downloading...")     
    video = await message.download()
    video_id = message.video.file_id
    subprocess.run(f'ffmpeg -i "{video}" -ss 00:01:00 -vframes 1 "{video_id}.jpg"', shell=True)
   # thumbnail = f"{video_id}.jpg"
    dur = int(duration(video))
    start_time = time.time() 
#    await app.send_video(chat_id=message.chat.id, video=video) 
    await reply.edit_text(f"**⥣ Uploading ...** » `")
    await app.send_video(chat_id=message.chat.id, video=video, supports_streaming=True, duration=dur, progress=progress_bar, progress_args=(reply, start_time))    
  #  os.remove(f"{video_id}.jpg") 

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
        thread = threading.Thread(target=lambda: asyncio.run(dl_send(message)))
        thread.start() 
               
    else:
        pass

