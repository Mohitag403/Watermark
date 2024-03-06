from pyrogram import filters
from Watermark import app
from config import OWNER_ID

@app.on_message((filters.document | filters.video | filters.photo) & filters.private)
async def watcher(app, message):
    if message.photo or (message.document and message.document.mime_type.startswith("photo/")):
        photo = await message.download()
        await message.reply_text("Yes, it's a photo\nWait downloading...")
        await app.send_photo(chat_id=message.chat.id, photo=photo)
        
    elif message.video or (message.document and message.document.mime_type.startswith("video/")):
        video = await message.download()
        await message.reply_text("Yes, it's a video\nwait downloading...")        
        await app.send_video(chat_id=message.chat.id, video=video)                
    else:
        pass

