from pyrogram import Client, filters
from Watermark.core.mongo import db
from Watermark import app


async def view_thumb(client, message, user_id):    
    thumb = await db.get_thumbnail(user_id)
    if thumb:
       await client.send_photo(chat_id=message.chat.id, photo=thumb)
    else:
        await query.answer("**ʏᴏᴜ ᴅᴏɴᴛ ʜᴀᴠᴇ ᴀɴʏ ᴛʜᴜᴍʙɴᴀɪʟ.**", show_alert=True) 



async def remove_thumb(client, message, user_id):
    thumb = await db.set_thumbnail(user_id, file_id=None)
    if thumb:
      await message.answer("❌️ **ʏᴏᴜʀ ᴛʜᴜᴍʙɴᴀɪʟ sᴜᴄᴄᴇssғᴜʟʟʏ ᴅᴇʟᴇᴛᴇᴅ.**", show_alert=True)
    else:
      await message.answer("Empty !! Thumbnail", show_alert=True)
	

async def add_thumb(client, message, user_id):
    mkn = await app.ask(message.chat.id, text="Give me your thumbnail photo")
    photo = mkn.text
    await db.set_thumbnail(user_id, file_id=photo)                
    await mkn.edit("✅️**ʏᴏᴜʀ ᴛʜᴜᴍʙɴᴀɪʟ sᴜᴄᴄᴇssғᴜʟʟʏ sᴀᴠᴇᴅ**")


