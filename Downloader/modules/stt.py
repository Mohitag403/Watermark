from pyrogram import filters
from Downloader import app



@app.on_message(filters.command(""))
async def start(_,message):
  await message.reply_text("i am working sensei !!")
