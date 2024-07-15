import os,time, requests
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



def get_duration(filepath):
    try:
        metadata = extractMetadata(createParser(filepath))
        if metadata:
            duration = metadata.get("duration").seconds if metadata.has("duration") else 0
            width = metadata.get("width") if metadata.has("width") else 1280
            height = metadata.get("height") if metadata.has("height") else 720
            return duration, width, height
    except:
        return 0, 1280, 720



async def download_thumbnail(url):
    response = requests.get(url)
    if response.status_code == 200:
        filename = url.split("/")[-1]
        with open(filename, 'wb') as f:
            f.write(response.content)
        return filename



@app.on_message((filters.document | filters.video | filters.photo) & filters.private)
async def watcher(_, message):
    try:
        if message.photo or (message.document and message.document.mime_type.startswith("photo/")):
            photo = await message.download()
            await app.send_photo(chat_id=message.chat.id, photo=photo, reply_to_message_id=message.reply_to_message_id)
            await message.reply_text("Yes, it's a photo\nWait downloading...")

        elif message.video or (message.document and message.document.mime_type.startswith("video/")):
            data = await db.get_data(message.from_user.id)
            c_time = time.time()
            ms = await message.reply_text("ᴛʀʏɪɴɢ ᴛᴏ ᴅᴏᴡɴʟᴏᴀᴅɪɴɢ...")
            file = await message.download(progress=progress_bar, progress_args=("𝚃𝚁ʏɪɴɢ ᴛᴏ ᴅᴏᴡɴʟᴏᴀᴅ....", ms, c_time))

            output_vid = f"watermarked_{file}"

            
            watermark_text = data.get("watermark_text")
            file_generator_command = [
                "ffmpeg",
                "-i", file,
                "-vf", f"drawtext=text='{watermark_text}':x=10:y=10:fontcolor=white:fontsize=25",
                output_vid
            ]

            await message.reply_text("adding watermark...")
            process = await asyncio.create_subprocess_exec(
                *file_generator_command,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )

            stdout, stderr = await process.communicate()
            if process.returncode != 0:
                print(f"ffmpeg failed: {stderr.decode()}")
                return

            caption = data.get("caption")
            if caption:
                caption = caption
            else:
                caption = ""
                
            duration, width, height = get_duration(file)

            if duration <= 300:
                await app.send_video(
                    chat_id=message.chat.id, video=file, caption=caption,
                    height=height, width=width, duration=duration,
                    thumb=None, progress=progress_bar,
                    progress_args=('**UPLOADING:**\n', ms, c_time)
                )
                await ms.delete()
                return

            
            if data and data.get("thumb"):
                thumb_url = data.get("thumb")
                thumb_path = await download_thumbnail(thumb_url)
            else:
                try:
                    subprocess.run(f'ffmpeg -i "{file}" -ss 00:01:00 -vframes 1 "{message.chat.id}.jpg"', shell=True)
                    thumb_path = f"{message.chat.id}.jpg"
                except Exception as e:
                    print(f"failed to generate thumb: {e}")
                    thumb_path = None

            with open(output_vid, "rb") as vid:
                await app.send_video(
                    chat_id=message.chat.id,
                    video=vid,
                    caption=caption,
                    height=height,
                    width=width,
                    thumb=thumb_path,
                    duration=duration,
                    progress=progress_bar,
                    progress_args=("Trying to upload...", ms, c_time)
                )

            
            await ms.delete()
            if thumb_path:
                os.remove(thumb_path)
                os.remove(file)

    except Exception as e:
        await message.reply_text(f"An error occurred: {str(e)}")



