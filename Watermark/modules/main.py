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






@app.on_callback_query(filters.regex('close_data'))
async def close_data(_,query):
	try:
           await query.message.delete()
	except:
           return


@app.on_callback_query(filters.regex("upload"))
async def doc(_,query):
     type = query.data.split("_")[1]
     new_name = query.message.text
     new_filename = new_name.split(":-")[1]
     file_path = f"downloads/{new_filename}"
     file = query.message.reply_to_message
     ms = await query.message.edit("ᴛʀʏɪɴɢ ᴛᴏ ᴅᴏᴡɴʟᴏᴀᴅɪɴɢ...")
     c_time = time.time()
     try:
     	path = await _.download_media(message = file, progress=progress_bar ,progress_args=( "𝚃𝚁𝚈𝙸𝙽𝙶 𝚃𝙾 𝙳𝙾𝚆𝙽𝙻𝙾𝙰𝙳....",  ms, c_time))
     except Exception as e:
     	await ms.edit(e)
     	return 
     splitpath = path.split("/downloads/")
     dow_file_name = splitpath[1]
     old_file_name =f"downloads/{dow_file_name}"
     os.rename(old_file_name,file_path)
     duration = 0
     try:
        metadata = extractMetadata(createParser(file_path))
        if metadata.has("duration"):
           duration = metadata.get('duration').seconds
     except:
        pass
     user_id = int(query.message.chat.id) 
     ph_path = None 
     media = getattr(file, file.media.value)
     c_caption = await db.get_caption(query.message.chat.id)
     c_thumb = await db.get_thumbnail(query.message.chat.id)
     if c_caption:
         try:
             caption = c_caption.format(filename=new_filename, filesize=humanize.naturalsize(media.file_size), duration=convert(duration))
         except Exception as e:
             await ms.edit(text=f"» ʏᴏᴜʀ ᴄᴀᴘᴛɪᴏɴ ᴇʀʀᴏʀ ᴜɴᴇxᴘᴇᴄᴛᴇᴅ ᴋᴇʏᴡᴏʀᴅ ●> ({e})")
             return 
     else:
         caption = f"**{new_filename}**"
     if (media.thumbs or c_thumb):
         if c_thumb:
            ph_path = await _.download_media(c_thumb) 
         else:
            ph_path = await _.download_media(media.thumbs[0].file_id)
         Image.open(ph_path).convert("RGB").save(ph_path)
         img = Image.open(ph_path)
         img.resize((320, 320))
         img.save(ph_path, "JPEG")
     await ms.edit("ᴛʀʏɪɴɢ ᴛᴏ ᴜᴘʟᴏᴀᴅɪɴɢ...")
     c_time = time.time() 
     try:
        if type == "document":
           await _.send_document(
		    query.message.chat.id,
                    document=file_path,
                    thumb=ph_path, 
                    caption=caption, 
                    progress=progress_bar,
                    progress_args=( "ᴛʀʏɪɴɢ ᴛᴏ ᴜᴘʟᴏᴀᴅɪɴɢ...",  ms, c_time))
        elif type == "video": 
            await _.send_video(
		    query.message.chat.id,
		    video=file_path,
		    caption=caption,
		    thumb=ph_path,
		    duration=duration,
		    progress=progress_bar,
		    progress_args=( "ᴛʀʏɪɴɢ ᴛᴏ ᴜᴘʟᴏᴀᴅɪɴɢ...",  ms, c_time))
        
     except Exception as e: 
         await ms.edit(f" Error {e}") 
         os.remove(file_path)
         if ph_path:
           os.remove(ph_path)
         return 
     await ms.delete() 
     os.remove(file_path) 
     if ph_path:
        os.remove(ph_path) 





