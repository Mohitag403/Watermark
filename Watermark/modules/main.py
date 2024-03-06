import os,time
from pyrogram import filters
import asyncio,threading 
import subprocess
from Watermark import app
from config import OWNER_ID
from hachoir.metadata import extractMetadata
from hachoir.parser import createParser
from Watermark.core.mongo import db
import humanize
from PIL import Image
from Watermark.core.utils import progress_bar, convert
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ForceReply


user_data = {}


@app.on_message((filters.document | filters.video | filters.photo) & filters.private)
async def watcher(_, message):
    global user_data
    if message.photo or (message.document and message.document.mime_type.startswith("photo/")):
        photo = await message.download()
        await app.send_photo(chat_id=message.chat.id, photo=photo, reply_to_message_id=message.reply_to_message_id)
        await message.reply_text("Yes, it's a photo\nWait downloading...")

    elif message.video or (message.document and message.document.mime_type.startswith("video/")):
        ms = await message.reply_text("ᴛʀʏɪɴɢ ᴛᴏ ᴅᴏᴡɴʟᴏᴀᴅɪɴɢ...")
        path = await dl(message, ms)
        user_data[message.chat.id] = {'path': path, 'ms': ms}
        await upload(ms)
     


@app.on_callback_query(filters.regex('close_data'))
async def close_data(_,query):
	try:
           await query.message.delete()
	except:
           return


async def dl(message, ms):
    c_time = time.time()
    try:
        path = await message.download(progress=progress_bar ,progress_args=( "𝚃𝚁𝚈𝙸𝙽𝙶 𝚃𝙾 𝙳𝙾𝚆𝙽𝙻𝙾𝙰𝙳....",  ms, c_time))
        return path
    except Exception as e:
    	await ms.edit(e)
    	return


async def upload(ms):
    button = [
        [
            InlineKeyboardButton("DOC", callback_data=f"upload_document"),
            InlineKeyboardButton("VIDEO", callback_data=f"upload_video")
        ]
    ]  
    await ms.edit("**CHOOSE YOUR FORMAT**", reply_markup=InlineKeyboardMarkup(button))


@app.on_callback_query(filters.regex("^upload"))
async def doc(_, query):
    global user_data
    user = user_data.get(query.message.chat.id, {})
    path = user.get('path')
    ms = user.get('ms')

    c_time = time.time()
    try:
        duration = 0
        try:
            metadata = extractMetadata(createParser(path))
            if metadata.has("duration"):
                duration = metadata.get('duration').seconds
            if metadata.has("width") and metadata.has("height"):
                width, height = metadata.get("width"), metadata.get("height")
            else:
                width, height = 1280, 720   
        except:
            pass

        data = await db.get_data(query.from_user.id)
        file_name = path.split("/")[-1]
        
        if data and data.get("caption"):
            try:
                c_caption = data.get("caption")
                caption = c_caption.format(filename=file_name, filesize=humanize.naturalsize(os.path.getsize(path)), duration=duration)
            except Exception as e:
                await query.message.reply_text(f"» Your caption has an unexpected keyword error: {e} \nSo Processing further without Your Caption")
                pass
                caption = f"**{file_name}**"
        else:
            caption = f"**{file_name}**"

        if data and data.get("thumb"):
            ph_path = c_thumb = data.get("thumb")
#            img = Image.open(c_thumb)
#            img = img.resize((width, height), Image.LANCZOS)
#            img.save(f"{file_name}.jpg")
        else:
            subprocess.run(f'ffmpeg -i "{path}" -ss 00:01:00 -vframes 1 "{file_name}.jpg"', shell=True)
            ph_path = f"{file_name}.jpg"

        if query.data=="upload_video":
            await _.send_video(
                query.message.chat.id,
                video=path,
                caption=caption,
                height=720, 
                width=1280,
                thumb=ph_path,
                duration=duration,
                progress=progress_bar,
                progress_args=("Trying to uploading...", ms, c_time)
            )
        elif query.data=="upload_document":
            await _.send_document(
                query.message.chat.id,
                document=path,
                caption=caption,
                progress=progress_bar,
                progress_args=("Trying to uploading...", ms, c_time)
            )
        
    except Exception as e:
        await ms.edit(f"Error: {e}")
        if os.path.exists(path):
            os.remove(path)
        return



