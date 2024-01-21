from pyrogram import filters
from Downloader import app
from Downloader.core.database import db



@app.on_message(filters.command("viewthumb"))
async def viewthumb(client, message):    
    thumb = await db.get_thumbnail(message.from_user.id)
    if thumb:
       await client.send_photo(
	   chat_id=message.chat.id, 
	   photo=thumb)
    else:
        await message.reply_text("**ʏᴏᴜ ᴅᴏɴᴛ ʜᴀᴠᴇ ᴀɴʏ ᴛʜᴜᴍʙɴᴀɪʟ.**") 


@app.on_message(filters.command("delthumb"))
async def removethumb(client, message):
    await db.set_thumbnail(message.from_user.id, file_id=None)
    await message.reply_text("❌️ **ʏᴏᴜʀ ᴛʜᴜᴍʙɴᴀɪʟ sᴜᴄᴄᴇssғᴜʟʟʏ ᴅᴇʟᴇᴛᴇᴅ.**")


@app.on_message(filters.private & filters.photo)
async def addthumbs(client, message):
    lol = await message.reply_text("ᴘʟᴇᴀsᴇ ᴡᴀɪᴛ...↻")
    await db.set_thumbnail(message.from_user.id, file_id=message.photo.file_id)                
    await lol.edit("✅️**ʏᴏᴜʀ ᴛʜᴜᴍʙɴᴀɪʟ sᴜᴄᴄᴇssғᴜʟʟʏ sᴀᴠᴇᴅ**")



