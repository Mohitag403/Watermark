import os
import time
import asyncio
from pathlib import Path
from PIL import Image
from hachoir.parser import createParser
from hachoir.metadata import extractMetadata
from pyrogram.errors import MessageNotModified, FloodWait
from utils import copy_file, take_screen_shot, LOGGER


async def upload_to_tg(
    message,
    local_file_name,
):
    if os.path.isdir(local_file_name):
        directory_contents = os.listdir(local_file_name)
        directory_contents.sort()
        LOGGER.info(directory_contents)

        for single_file in directory_contents:
            await upload_to_tg(
                message,
                os.path.join(local_file_name, single_file),
                from_user,
                dict_containing_uploaded_files,
                client,
                edit_media,
                yt_thumb,
            )
    else:
        try:
            size = os.path.getsize(local_file_name)
            sent_message = await upload_single_file(
                message,
                local_file_name,
                from_user,
                dict_containing_uploaded_files,
                client,
                edit_media,
                yt_thumb,
            )
        except Exception as e:
            LOGGER.error(f"Error uploading file: {e}")
    return dict_containing_uploaded_files

async def upload_single_file(
    message, local_file_name, from_user, dict_containing_uploaded_files, client, edit_media, yt_thumb
):
    await asyncio.sleep(EDIT_SLEEP_TIME_OUT)
    local_file_name = str(Path(local_file_name).resolve())
    sent_message = None
    start_time = time.time()
    thumbnail_location = os.path.join(DOWNLOAD_LOCATION, "thumbnails", str(from_user) + ".jpg")

    try:
        if local_file_name.upper().endswith(("MKV", "MP4", "WEBM", "FLV", "3GP", "AVI", "MOV", "OGG", "WMV", "M4V", "TS", "MPG", "MTS", "M2TS")):
            duration = 0
            try:
                metadata = extractMetadata(createParser(local_file_name))
                if metadata.has("duration"):
                    duration = metadata.get("duration").seconds
            except Exception as g_e:
                LOGGER.error(g_e)
            width = 0
            height = 0
            thumb_image_path = None
            if os.path.exists(thumbnail_location):
                thumb_image_path = await copy_file(
                    thumbnail_location,
                    os.path.dirname(os.path.abspath(local_file_name)),
                )
            else:
                LOGGER.info("Taking Screenshot..")
                thumb_image_path = await take_screen_shot(
                    local_file_name,
                    os.path.dirname(os.path.abspath(local_file_name)),
                    (duration / 2),
                )

            if os.path.exists(thumb_image_path):
                metadata = extractMetadata(createParser(thumb_image_path))
                if metadata.has("width"):
                    width = metadata.get("width")
                if metadata.has("height"):
                    height = metadata.get("height")
                Image.open(thumb_image_path).convert("RGB").save(thumb_image_path)
                img = Image.open(thumb_image_path)
                img.resize((320, height))
                img.save(thumb_image_path, "JPEG")

            thumb = None
            if thumb_image_path is not None and os.path.isfile(thumb_image_path):
                thumb = thumb_image_path

            await message.reply_video(
                video=local_file_name,
                caption=caption_str,
                parse_mode="html",
                duration=duration,
                width=width,
                height=height,
                thumb=thumb,
                supports_streaming=True,
                disable_notification=True,
                progress=prog.progress_for_pyrogram,
                progress_args=(
                    f"**• Uploading :** `{os.path.basename(local_file_name)}`",
                    start_time,
                ),
            )
            if thumb is not None:
                os.remove(thumb)
        elif local_file_name.upper().endswith(("MP3", "M4A", "M4B", "FLAC", "WAV")):
            metadata = extractMetadata(createParser(local_file_name))
            duration = 0
            title = ""
            artist = ""
            if metadata.has("duration"):
                duration = metadata.get("duration").seconds
            if metadata.has("title"):
                title = metadata.get("title")
            if metadata.has("artist"):
                artist = metadata.get("artist")
            thumb_image_path = None
            if os.path.isfile(thumbnail_location):
                thumb_image_path = await copy_file(
                    thumbnail_location,
                    os.path.dirname(os.path.abspath(local_file_name)),
                )
            thumb = None
            if thumb_image_path is not None and os.path.isfile(thumb_image_path):
                thumb = thumb_image_path
                sent_message = await message.reply_audio(
                    audio=local_file_name,
                    caption=caption_str,
                    parse_mode="html",
                    duration=duration,
                    performer=artist,
                    title=title,
                    thumb=thumb,
                    disable_notification=True,
                    progress=prog.progress_for_pyrogram,
                    progress_args=(
                        f"**• Uploading :** `{os.path.basename(local_file_name)}`",
                        start_time,
                    ),
                )
            if thumb is not None:
                os.remove(thumb)
    except MessageNotModified as oY:
        LOGGER.error(oY)
    except FloodWait as g:
        LOGGER.error(g)
        time.sleep(g.x)
    except Exception as e:
        LOGGER.error(e)
        await message_for_progress_display.edit_text("**FAILED**\n" + str(e))
    else:
        if message.message_id != message_for_progress_display.message_id:
            try:
                if sent_message is not None:
                    await message_for_progress_display.delete()
            except FloodWait as gf:
                time.sleep(gf.x)
            except Exception as rr:
                LOGGER.warning(str(rr))
                await asyncio.sleep(5)
    os.remove(local_file_name)
    return sent_message
