import os,time
from pyrogram import filters
import asyncio,threading 
import subprocess
from Watermark import app
from config import OWNER_ID
from Watermark.core.utils import progress_bar
from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip



async def dl_send(message):
    reply = await message.reply_text("Yes, it's a video\nwait downloading...")     
    video1 = await message.download()
    video = VideoFileClip(video1)
    watermark_text = await app.ask(message.chat.id, text="send your text")
    watermark_text = str(watermark_text)
    fontsize = 50
    color = 'white'
    font = 'Arial-Bold'
    txt_clip = TextClip(watermark_text, fontsize=fontsize, color=color, font=font)
    position = ('bottom', 'right')
    padding = (10, 10)
    if position[0] == 'top':
        y = padding[1]
    elif position[0] == 'bottom':
        y = video.size[1] - txt_clip.size[1] - padding[1]
    else:
        raise ValueError("Invalid position")

    if position[1] == 'left':
        x = padding[0]
    elif position[1] == 'right':
        x = video.size[0] - txt_clip.size[0] - padding[0]
    else:
        raise ValueError("Invalid position")
    watermark = txt_clip.set_position((x, y)).set_duration(video.duration)
    video_with_watermark = CompositeVideoClip([video, watermark])
    video_with_watermark.write_videofile("output_video.mp4", codec='libx264')
    video.close()
    video_with_watermark.close()
    start_time = time.time()
    await reply.edit_text(f"**UPLOADING ...** » ")
    await app.send_video(chat_id=message.chat.id, video=video_with_watermark, supports_streaming=True,  progress=progress_bar, progress_args=(reply, start_time))    
 


@app.on_message((filters.document | filters.video | filters.photo) & filters.private)
async def watcher(app, message):     
    if message.video or (message.document and message.document.mime_type.startswith("video/")):
#        thread = threading.Thread(target=lambda: asyncio.run(dl_send(message)))
#        thread.start() 
        await dl_send(message)
    else:
        pass
