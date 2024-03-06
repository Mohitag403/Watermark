import os,time
from pyrogram import filters
import asyncio,threading 
import subprocess
from Watermark import app
from config import OWNER_ID





@app.on_message((filters.document | filters.video | filters.photo) & filters.private)
async def watcher(_, message):
    if message.photo or (message.document and message.document.mime_type.startswith("photo/")):
        photo = await message.download()
        await app.send_photo(chat_id=message.chat.id, photo=photo)
        await message.reply_text("Yes, it's a photo\nWait downloading...")

    elif message.video or (message.document and message.document.mime_type.startswith("video/")):
	vide_path = await message.download()
        await app.send_video(chat_id=message.chat.id, video=video_path)
        await message.reply_text("Yes, it's a photo\nWait downloading...")
	    
        watermark_image = "https://graph.org/file/e65a93d5e442326c4b895.jpg"
        output_video = "output_video.mp4"
        (
            ffmpeg
            .input(video_path)
            .output(output_video, vf=f"movie={watermark_image} [watermark]; [in][watermark] overlay=10:10 [out]")
            .run()
        )

        
        await app.send_video(chat_id=message.chat.id, video=output_video)
        await message.reply_text("Video with watermark added and sent!")







         




