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





@app.on_message((filters.document | filters.video | filters.photo) & filters.private)
async def watcher(_, message):
    if message.photo or (message.document and message.document.mime_type.startswith("photo/")):
        photo = await message.download()
        await app.send_photo(chat_id=message.chat.id, photo=photo, reply_to_message_id=message.reply_to_message_id)
        await message.reply_text("Yes, it's a photo\nWait downloading...")

    elif message.video or (message.document and message.document.mime_type.startswith("video/")):
        ms = await message.reply_text("ᴛʀʏɪɴɢ ᴛᴏ ᴅᴏᴡɴʟᴏᴀᴅɪɴɢ...")
        path = await dl(message, ms)
        await upload(message, path, ms)
     


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


async def upload(message, path, ms):
    button = [
        [
            InlineKeyboardButton("DOC", callback_data=f"upload_document:{path}:{ms}"),
            InlineKeyboardButton("VIDEO", callback_data=f"upload_video:{path}:{ms}")
        ]
    ]  
    await message.reply("**CHOOSE YOUR FORMAT**", reply_markup=InlineKeyboardMarkup(button))


@app.on_callback_query(filters.regex("^upload"))
async def doc(_, query):
    c_time = time.time()
    path = query.data.split(":")[1]
    ms = query.data.split(":")[2]
    try:
        duration = 0
        try:
            metadata = extractMetadata(createParser(path))
            if metadata.has("duration"):
                duration = metadata.get('duration').seconds
        except:
            pass

        c_caption = await db.get_caption(query.message.chat.id)
        c_thumb = await db.get_thumbnail(query.message.chat.id)
        file_name = path.split("/")[-1]
        
        if c_caption:
            try:
                caption = c_caption.format(filename=file_name, filesize=humanize.naturalsize(os.path.getsize(path)), duration=duration)
            except Exception as e:
                await query.message.reply_text(f"» Your caption has an unexpected keyword error: {e} \nSo Processing further without Your Caption")
                pass
                caption = f"**{file_name}**"
        else:
            caption = f"**{file_name}**"

        if c_thumb:
            ph_path = await _.download_media(c_thumb) 
            img = Image.open(ph_path)
            resized_img = img.resize((320, 320))
            resized_img.convert("RGB").save(ph_path, "JPEG")
        else:
            subprocess.run(f'ffmpeg -i "{path}" -ss 00:01:00 -vframes 1 "{file_name}.jpg"', shell=True)
            ph_path = f"{file_name}.jpg"

        if query.data.startswith("upload_video_"):
            await _.send_video(
                query.message.chat.id,
                video=path,
                caption=caption,
                thumb=ph_path,
                duration=duration,
                progress=progress_bar,
                progress_args=("Trying to uploading...", ms, c_time)
            )
        elif query.data.startswith("upload_document_"):
            await _.send_document(
                query.message.chat.id,
                document=path,
                caption=caption,
                progress=progress_bar,
                progress_args=("Trying to uploading...", ms, c_time)
            )
        
    except Exception as e:
        await _.edit_message_text(f"Error: {e}")
        if os.path.exists(ph_path):
            os.remove(ph_path)
        return

    await ms.delete()
    if os.path.exists(ph_path):
        os.remove(ph_path)
    os.remove(path)



