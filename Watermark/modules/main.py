from pyrogram import filters
from Watermark import app
from config import OWNER_ID

@app.on_message((filters.document | filters.video | filters.photo) & filters.private)
async def watcher(app, message):
    user_id = message.from_user.id
    if user_id in OWNER_ID:
        if message.photo or (message.document and message.document.mime_type.startswith("image/")):
            await message.reply_text("yes its a photo !!")
        elif message.video or (message.document and message.document.mime_type.startswith("video/")):
            await message.reply_text("yes its a video")
        else:
            await message.reply_text("htt bsdk !!")
    
