import os,time
from pyrogram import filters
import asyncio,threading 
import subprocess
from Watermark import app
from config import OWNER_ID
from Watermark.core.utils import progress_bar
from Watermark.modules import view_thumb, remove_thumb, add_thumb, add_caption, delete_caption, see_caption



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
        thread = threading.Thread(target=lambda: asyncio.run(dl_send(message)))
        thread.start() 
               
    else:
        pass


buttons1 = InlineKeyboardMarkup([
            [
                InlineKeyboardButton("Thumbnail", callback_data="thumb"),
                InlineKeyboardButton("Caption", callback_data="caption")
            ]
        ])

buttons2 = InlineKeyboardMarkup([
            [
                InlineKeyboardButton("Set Thumbnail", callback_data="Sthumb"),
                InlineKeyboardButton("Remove Thumbnail", callback_data="Rthumb")
            ],
            [
                InlineKeyboardButton("View Thumbnail", callback_data="Vthumb"),
            ]
        ])

buttons3 = InlineKeyboardMarkup([
            [
                InlineKeyboardButton("Set Caption", callback_data="Scaption"),
                InlineKeyboardButton("Remove Caption", callback_data="Rcaption")
            ]
        ])


@app.on_message(filters.command("settings") & filters.private)
async def settings(_, message):
    await messgae.reply_text("Choose from Below", reply_markup=buttons1)


@app.on_callback_query()
async def callback(_, query):
    if query.data=="thumb":
        await messgae.reply_text("Choose from Below", reply_markup=buttons2)

    elif query.data=="caption":
        caption = await see_caption(query)
        await messgae.reply_text(f"Choose from Below\n\n**ʏᴏᴜʀ ᴄᴀᴘᴛɪᴏɴ:** `{caption}`", reply_markup=buttons3)

    elif query.data=="Sthumb":
        await add_thumb(query)

    elif query.data=="Rthumb":
        await remove_thumb(query)

    elif query.data=="Vthumb":
        await view_thumb(query)

    elif query.data=="Scaption":
        await add_caption(query)

    elif query.data=="Rcaption":
        await delete_caption(query)
