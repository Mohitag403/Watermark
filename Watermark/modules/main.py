import os,time
from pyrogram import filters
import asyncio,threading 
import subprocess
from Watermark import app
from config import OWNER_ID
from hachoir.metadata import extractMetadata
from hachoir.parser import createParser
from Watermark.core.mongo import db
from Watermark.core.utils import progress_bar, convert
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ForceReply


user_data = {}


async def down(message, ms):
    data = await db.get_data(message.from_user.id)        
    c_time = time.time()
    try:
        file = await message.download(progress=progress_bar, progress_args=("𝚃𝚁𝚈𝙸𝙽𝙶 𝚃𝙾 𝙳𝙾𝚆𝙽𝙻𝙾𝙰𝙳....", ms, c_time))
        try:
            output_vid = f"watermarked_{file}"

            if data and data.get("watermark_image"):
                watermark_image = data.get("watermark_image")
                file_generator_command = [
                    "ffmpeg",
                    "-i", file,
                    "-i", watermark_image,
                    "-filter_complex", "overlay=10:10",  # Top-left corner with 10px padding
                    output_vid
                ]
            else:
                watermark_text = data.get("watermark_text")
                file_generator_command = [
                    "ffmpeg",
                    "-i", file,
                    "-vf", f"drawtext=text='{watermark_text}':x=10:y=10:fontcolor=white:fontsize=24",
                    output_vid
                ]

            process = await asyncio.create_subprocess_exec(
                *file_generator_command,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )

            stdout, stderr = await process.communicate()
            if process.returncode != 0:
                print(f"ffmpeg failed: {stderr.decode()}")
                return

            with open(output_vid, "rb") as vid:
                await message.reply_video(vid)
                
            return output_vid
        except Exception as e:
            print(f"Error during watermarking: {e}")
            return file
    except Exception as e:
        await ms.edit(str(e))
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
        user_data[message.from_user.id] = {'path': path, 'ms': ms}
        await message.reply_video(path)
        await upload(ms)
        
        
     



@app.on_callback_query(filters.regex("^upload"))
async def doc(client, query):
    
    user = user_data.get(query.from_user.id, {})
    path = user.get('path')
    ms = user.get('ms')

    c_time = time.time()
    try:
        duration = 0
        width, height = 1280, 720

        try:
            metadata = extractMetadata(createParser(path))
            if metadata.has("duration"):
                duration = metadata.get('duration').seconds
            if metadata.has("width") and metadata.has("height"):
                width, height = metadata.get("width"), metadata.get("height")
        except Exception as e:
            print(f"Metadata extraction error: {e}")

        data = await db.get_data(query.from_user.id)
        file_name = "lol_1234"

        caption = f"**{file_name}**"
        if data and data.get("caption"):
            try:
                c_caption = data.get("caption")
                caption = c_caption.format(filename=file_name, filesize=naturalsize(os.path.getsize(path)), duration=duration)
            except Exception as e:
                await query.message.reply_text(f"» Your caption has an unexpected keyword error: {e} \nSo Processing further without Your Caption")

        ph_path = data.get("thumb") if data and data.get("thumb") else f"{file_name}.jpg"
        if not data or not data.get("thumb"):
            subprocess.run(f'ffmpeg -i "{path}" -ss 00:01:00 -vframes 1 "{ph_path}"', shell=True)

        if query.data == "upload_video":
            async with open(path, "rb") as vid:
                try:
                    await client.send_video(
                        query.message.chat.id,
                        video=vid,
                        caption=caption,
                        height=height,
                        width=width,
                        thumb=ph_path,
                        duration=duration,
                        progress=progress_bar,
                        progress_args=("Trying to upload...", ms, c_time)
                    )
                except Exception:
                    await client.send_video(
                        query.message.chat.id,
                        video=path,
                        caption=caption,
                        progress=progress_bar,
                        progress_args=("Trying to upload...", ms, c_time)
                    )
        elif query.data == "upload_document":
            await client.send_document(
                query.message.chat.id,
                document=path,
                caption=caption,
                progress=progress_bar,
                progress_args=("Trying to upload...", ms, c_time)
            )

        await ms.delete()
        os.remove(ph_path) if os.path.exists(ph_path) else None
        os.remove(path) if os.path.exists(path) else None

    except Exception as e:
        await ms.edit(f"Error: {e}")
        os.remove(ph_path) if os.path.exists(ph_path) else None
        os.remove(path) if os.path.exists(path) else None





