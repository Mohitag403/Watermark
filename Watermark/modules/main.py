import os,time
from pyrogram import filters
import asyncio,threading 
import subprocess
from Watermark import app
from config import OWNER_ID
from Watermark.core.utils import progress_bar
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ForceReply




async def dl_send(message):
    reply = await message.reply_text("Yes, it's a video\nwait downloading...")     
    video = await message.download()
    start_time = time.time()
    await reply.edit_text(f"**UPLOADING ...** » ")
    await app.send_video(chat_id=message.chat.id, video=video, supports_streaming=True,  progress=progress_bar, progress_args=(reply, start_time))    
 


@app.on_message((filters.document | filters.video | filters.photo) & filters.private)
async def watcher(app, message):
    if message.photo or (message.document and message.document.mime_type.startswith("photo/")):
        photo = await message.download()
        await message.reply_text("Yes, it's a photo\nWait downloading...")
        await app.send_photo(chat_id=message.chat.id, photo=photo)
        
    elif message.video or (message.document and message.document.mime_type.startswith("video/")):
        button = [[
                   InlineKeyboardButton("DOC",callback_data = "upload_document"),
                   InlineKeyboardButton("VIDEO",callback_data = "upload_document")
                 ],[
                   InlineKeyboardButton("CLOSE",callback_data = "close_data")
                 ]]
        await message.reply_text("**CHOOSE YOUR FORMAT**",          
          reply_markup=InlineKeyboardMarkup(button))
                 
        
        thread = threading.Thread(target=lambda: asyncio.run(dl_send(message)))
        thread.start() 
               
    else:
        pass


