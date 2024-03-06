from pyrogram import Client, filters
from Watermark.core.mongo import db
from Watermark import app


async def view_thumb(client, message):    
    thumb = await db.get_thumbnail(message.from_user.id)
    if thumb:
       await client.send_photo(message.chat.id, photo=thumb)
    else:
        await query.answer("**ʏᴏᴜ ᴅᴏɴᴛ ʜᴀᴠᴇ ᴀɴʏ ᴛʜᴜᴍʙɴᴀɪʟ.**", show_alert=True) 



async def remove_thumb(client, message):
    thumb = await db.set_thumbnail(message.from_user.id, file_id=None)
    if thumb:
      await message.answer("❌️ **ʏᴏᴜʀ ᴛʜᴜᴍʙɴᴀɪʟ sᴜᴄᴄᴇssғᴜʟʟʏ ᴅᴇʟᴇᴛᴇᴅ.**", show_alert=True)
    else:
      await message.answer("Empty !! Thumbnail", show_alert=True)
	

async def add_thumb(client, message):
    mkn = await app.ask(message.chat.id, text="Give me your thumbnail photo")
    photo = mkn.text
    await db.set_thumbnail(message.from_user.id, file_id=photo)                
    await mkn.edit("✅️**ʏᴏᴜʀ ᴛʜᴜᴍʙɴᴀɪʟ sᴜᴄᴄᴇssғᴜʟʟʏ sᴀᴠᴇᴅ**")




async def add_caption(client, message):    
    cap = await app.ask(message.chat.id, text="» ɢɪᴠᴇ ᴍᴇ ᴀ ᴄᴀᴘᴛɪᴏɴ ᴛᴏ sᴇᴛ.")
    caption = cap.text
    await db.set_caption(message.from_user.id, caption=caption)
    await message.reply_text("✅ ʏᴏᴜʀ ᴄᴀᴘᴛɪᴏɴ sᴜᴄᴄᴇssғᴜʟʟʏ.")

    

async def delete_caption(client, message):
    caption = await db.get_caption(message.from_user.id)  
    if not caption:
       await message.answer("ʏᴏᴜ ᴅᴏɴʏ ʜᴀᴠᴇ ᴄᴀᴘᴛɪᴏɴ.", show_alert=True)
    await db.set_caption(message.from_user.id, caption=None)
    await message.reply_text(" ʏᴏᴜʀ ᴄᴀᴘᴛɪᴏɴ sᴜᴄᴄᴇssғᴜʟʟʏ ᴅᴇʟᴇᴛᴇᴅ.")
                                       

async def see_caption(client, message):
    caption = await db.get_caption(message.from_user.id)  
    if caption:
       await message.reply_text(f"**ʏᴏᴜʀ ᴄᴀᴘᴛɪᴏɴ:**\n\n`{caption}`")
    else:
       await message.answer("ʏᴏᴜ ᴅᴏɴᴛ ʜᴀᴠᴇ ᴀɴʏ ᴄᴀᴘᴛɪᴏɴ.", show_alert=True)




