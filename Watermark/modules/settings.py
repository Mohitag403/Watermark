from pyrogram import Client, filters
from Watermark.core.mongo import db
from Watermark import app


async def view_thumb(query):    
    thumb = await db.get_thumbnail(query.message.from_user.id)
    if thumb:
       await query.message.reply_photo(photo=thumb)
    else:
        await query.answer("**ʏᴏᴜ ᴅᴏɴᴛ ʜᴀᴠᴇ ᴀɴʏ ᴛʜᴜᴍʙɴᴀɪʟ.**", show_alert=True) 



async def remove_thumb(query):
    thumb = await db.set_thumbnail(query.message.from_user.id, file_id=None)
    if thumb:
      await query.answer("❌️ **ʏᴏᴜʀ ᴛʜᴜᴍʙɴᴀɪʟ sᴜᴄᴄᴇssғᴜʟʟʏ ᴅᴇʟᴇᴛᴇᴅ.**", show_alert=True)
    else:
      await query.answer("Empty !! Thumbnail", show_alert=True)
	

async def add_thumb(query):
    mkn = await app.ask(query.message.chat.id, text="Give me your thumbnail photo")
    photo = mkn.text
    await db.set_thumbnail(query.message.from_user.id, file_id=photo)                
    await query.message.reply_text("✅️**ʏᴏᴜʀ ᴛʜᴜᴍʙɴᴀɪʟ sᴜᴄᴄᴇssғᴜʟʟʏ sᴀᴠᴇᴅ**")




async def add_caption(query):    
    cap = await app.ask(query.message.chat.id, text="» ɢɪᴠᴇ ᴍᴇ ᴀ ᴄᴀᴘᴛɪᴏɴ ᴛᴏ sᴇᴛ.")
    caption = cap.text
    await db.set_caption(query.message.from_user.id, caption=caption)
    await query.message.reply_text("✅ ʏᴏᴜʀ ᴄᴀᴘᴛɪᴏɴ sᴜᴄᴄᴇssғᴜʟʟʏ.")

    

async def delete_caption(query):
    caption = await db.get_caption(query.message.from_user.id)  
    if not caption:
       await query.answer("ʏᴏᴜ ᴅᴏɴʏ ʜᴀᴠᴇ ᴄᴀᴘᴛɪᴏɴ.", show_alert=True)
    await db.set_caption(query.message.from_user.id, caption=None)
    await query.message.reply_text(" ʏᴏᴜʀ ᴄᴀᴘᴛɪᴏɴ sᴜᴄᴄᴇssғᴜʟʟʏ ᴅᴇʟᴇᴛᴇᴅ.")
                                       

async def see_caption(query):
    caption = await db.get_caption(query.message.from_user.id)  
    if caption:
       return caption
    else:
       return ("ʏᴏᴜ ᴅᴏɴᴛ ʜᴀᴠᴇ ᴀɴʏ ᴄᴀᴘᴛɪᴏɴ.")




