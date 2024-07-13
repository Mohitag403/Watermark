from telegraph import upload_file
from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from Watermark.core.mongo import db
from Watermark import app
from Watermark.core import script
from Watermark.core.func import subscribe,


# --------------------Thumbnail--------------------- #

async def add_thumb(query):
    mkn = await app.ask(query.message.chat.id, text="Please send me your thumbnail photo.")
    if mkn.photo:
        file_name = str(query.from_user.id) + "set_thumb.jpg"
        photo_id = mkn.photo.file_id
        photo_path = await app.download_media(photo_id, file_name=file_name)
        fk = upload_file(photo_path)
        for x in fk:
            url = "https://telegra.ph" + x
        await db.set_thumbnail(query.from_user.id, url)
        await query.message.reply_text("✅️ Your thumbnail has been successfully saved.")        	
    else:
        await query.message.reply_text("❌️ Please send a valid photo for your thumbnail.")

async def remove_thumb(query):
    data = await db.get_data(query.from_user.id)  
    if data and data.get("thumb"):
        thumb = data.get("thumb")
        await db.remove_thumbnail(query.from_user.id)
        await query.answer("☘️ Your thumbnail has been successfully deleted.", show_alert=True)
    else:
        await query.answer("😜 You haven't set any thumbnails.", show_alert=True)
	
async def view_thumb(query):    
    data = await db.get_data(query.from_user.id)
    if data and data.get("thumb"):
       thumb = data.get("thumb")    
       await query.message.reply_photo(thumb)
    else:
        await query.answer("😜 You haven't set any thumbnails.", show_alert=True) 



# --------------------Caption--------------------- #

async def add_caption(query):    
    cap = await app.ask(query.message.chat.id, text="» ɢɪᴠᴇ ᴍᴇ ᴀ ᴄᴀᴘᴛɪᴏɴ ᴛᴏ sᴇᴛ.")
    caption = cap.text
    await db.set_caption(query.from_user.id, caption=caption)
    await query.message.reply_text("✅ Your caption has been successfully set.")

async def delete_caption(query):
    data = await db.get_data(query.from_user.id)  
    if data and data.get("caption"):
      await db.remove_caption(query.from_user.id)
      await query.answer("☘️ Your caption has been successfully deleted.", show_alert=True)

    else:
      await query.answer("👀 You haven't set any caption !!", show_alert=True)    

async def see_caption(query):
    data = await db.get_data(query.from_user.id)
    if data and data.get("caption"):
       caption = data.get("caption")
       await query.message.reply_text(f"**Your Caption:** `{caption}`")
    else:
       await query.answer("👀 You haven't set any caption !!", show_alert=True)



# --------------------Watermark-Text--------------------- #

async def add_watermark_text(query):    
    sos = await app.ask(query.message.chat.id, text="Give me a watermark to set.")
    watermark_text = sos.text
    await db.set_watermark_text(query.from_user.id, watermark_text)
    await query.message.reply_text("✅ Your watermark text has been successfully set.")

async def delete_watermark_text(query):
    data = await db.get_data(query.from_user.id)  
    if data and data.get("watermark_text"):
      await db.remove_watermark_text(query.from_user.id)
      await query.answer("☘️ Your watermark text has been successfully deleted.", show_alert=True)
    else:
      await query.answer("👀 You haven't set any watermark text !!", show_alert=True)    
                                             
async def view_watermark_text(query):
    data = await db.get_data(query.from_user.id)
    if data and data.get("watermark_text"):
       watermark_text = data.get("watermark_text")
       await query.message.reply_text(f"**Watermark Text**\n\n`{watermark_text}`")
    else:
       await query.answer("👀 You haven't set any watermark text !!", show_alert=True)


# --------------------Watermark-Image--------------------- #

async def add_watermark(query):
    mkn = await app.ask(query.message.chat.id, text="Please send me your watermark photo.")
    if mkn.photo:
        file_name = str(query.from_user.id) + "set_thumb.jpg"
        photo_id = mkn.photo.file_id
        photo_path = await app.download_media(photo_id, file_name=file_name)
        fk = upload_file(photo_path)
        for x in fk:
            url = "https://telegra.ph" + x
        await db.set_watermark(query.from_user.id, url)
        await query.message.reply_text("✅️ Your watermark photo has been successfully saved.")        	
    else:
        await query.message.reply_text("❌️ Please send a valid photo for your watermark.")

async def delete_watermark(query):
    data = await db.get_data(query.from_user.id)  
    if data and data.get("watermark_image"):
        thumb = data.get("watermark_image")
        await db.remove_watermark(query.from_user.id)
        await query.answer("☘️ Your watermark image has been successfully deleted.", show_alert=True)
    else:
        await query.answer("😜 You haven't set any watermark image.", show_alert=True)
	
async def view_watermark(query):    
    data = await db.get_data(query.from_user.id)
    if data and data.get("watermark_image"):
       watermark_image = data.get("watermark_image")    
       await query.message.reply_photo(watermark_image)
    else:
        await query.answer("😜 You haven't set any watermark image.", show_alert=True) 

 


buttons1 = InlineKeyboardMarkup([
            [
                InlineKeyboardButton("🏜 ᴛʜᴜᴍʙɴᴀɪʟ", callback_data="thumb_")                
            ],
	          [
                InlineKeyboardButton("📝 ᴄᴀᴘᴛɪᴏɴ", callback_data="caption_"),
		InlineKeyboardButton("📇 ᴡᴀᴛᴇʀᴍᴀʀᴋ", callback_data="watermark_")
            ]])



@app.on_message(filters.command("settings") & filters.private)
async def settings(_, message):
    join = await subscribe(_, message)
    if join == 1:
      return
    await message.reply_photo(photo="https://graph.org/file/914e6257251a02fde4203.jpg", caption=script.SETTINGS_TXT, reply_markup=buttons1)


