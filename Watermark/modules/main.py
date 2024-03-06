from pyrogram import filters
from Watermark import app
from config import OWNER_ID

@app.on_message((filters.document | filters.video | filters.photo) & filters.private)
async def watcher(app, message):
    if message.photo:
        photo = await message.download()
        await app.send_photo(chat_id=message.chat.id, photo=photo)
        
    elif message.video or (message.document and message.document.mime_type.startswith("video/")):
        await message.reply_text("Yes, it's a video")
    else:
        await message.reply_text("none !!! kuch nhi dono me se")


