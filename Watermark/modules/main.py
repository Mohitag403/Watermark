from pyrogram import filters
from Watermark import app

@app.on_message((filters.document | filters.video | filters.photo) & filters.private)
async def watcher(app, message):

    
