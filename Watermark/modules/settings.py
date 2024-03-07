import os
from pyrogram import Client, filters
from pyrogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from Watermark.core.mongo import db
from Watermark import app



async def view_thumb(query):    
    data = await db.get_data(query.from_user.id)
    if data and data.get("thumb"):
       thumb = data.get("thumb")    
       await query.message.reply_photo(photo=thumb)
    else:
        await query.answer("ʏᴏᴜ ᴅᴏɴᴛ ʜᴀᴠᴇ ᴀɴʏ ᴛʜᴜᴍʙɴᴀɪʟ.", show_alert=True) 



async def remove_thumb(query):
    data = await db.get_data(query.from_user.id)  
    if data and data.get("thumb"):
        thumb = data.get("thumb")
        os.remove(thumb)
        await db.remove_thumbnail(query.from_user.id)
        await query.answer("❌️ ʏᴏᴜʀ ᴛʜᴜᴍʙɴᴀɪʟ sᴜᴄᴄᴇssғᴜʟʟʏ ᴅᴇʟᴇᴛᴇᴅ.", show_alert=True)
    else:
        await query.answer("Empty !! Thumbnail", show_alert=True)
	

async def add_thumb(query):
    mkn = await app.ask(query.message.chat.id, text="Please send me your thumbnail photo.")
    if mkn.photo:
        file_name = str(query.from_user.id) + "thumb.jpg"
        photo_id = mkn.photo.file_id
        photo_path = await app.download_media(photo_id, file_name=file_name)
        await db.set_thumbnail(query.from_user.id, photo_path)
        await query.message.reply_text("✅️ Your thumbnail has been successfully saved.")
    else:
        await query.message.reply_text("❌️ Please send a valid photo for your thumbnail.")



async def add_caption(query):    
    cap = await app.ask(query.message.chat.id, text="» ɢɪᴠᴇ ᴍᴇ ᴀ ᴄᴀᴘᴛɪᴏɴ ᴛᴏ sᴇᴛ.")
    caption = cap.text
    await db.set_caption(query.from_user.id, caption=caption)
    await query.message.reply_text("✅ ʏᴏᴜʀ ᴄᴀᴘᴛɪᴏɴ sᴜᴄᴄᴇssғᴜʟʟʏ.")

    

async def delete_caption(query):
    data = await db.get_data(query.from_user.id)  
    if data and data.get("caption"):
      await db.remove_caption(query.from_user.id)
      await query.answer(" ʏᴏᴜʀ ᴄᴀᴘᴛɪᴏɴ sᴜᴄᴄᴇssғᴜʟʟʏ ᴅᴇʟᴇᴛᴇᴅ.", show_alert=True)

    else:
      await query.answer("ʏᴏᴜ ᴅᴏɴᴛ ʜᴀᴠᴇ ᴄᴀᴘᴛɪᴏɴ.", show_alert=True)    
                                             

async def see_caption(query):
    data = await db.get_data(query.from_user.id)
    if data and data.get("caption"):
       caption = data.get("caption")
       await query.message.reply_text(f"**ʏᴏᴜʀ ᴄᴀᴘᴛɪᴏɴ:** `{caption}`")
    else:
       await query.answer("ʏᴏᴜ ᴅᴏɴᴛ ʜᴀᴠᴇ ᴀɴʏ ᴄᴀᴘᴛɪᴏɴ.", show_alert=True)


async def view_watermark(query):    
    data = await db.get_data(query.from_user.id)
    if data and data.get("watermark"):
       thumb = data.get("watermark")    
       await query.message.reply_photo(photo=thumb)
    else:
        await query.answer("ʏᴏᴜ ᴅᴏɴᴛ ʜᴀᴠᴇ ᴀɴʏ watermark.", show_alert=True) 



async def remove_watermark(query):
    data = await db.get_data(query.from_user.id)  
    if data and data.get("watermark"):
        watermark = data.get("watermark")
        os.remove(watermark)
        await db.remove_watermark(query.from_user.id)
        await query.answer("❌️ ʏᴏᴜʀ watermark sᴜᴄᴄᴇssғᴜʟʟʏ ᴅᴇʟᴇᴛᴇᴅ.", show_alert=True)
    else:
        await query.answer("Empty !! watermark", show_alert=True)
	

async def add_watermark(query):
    mkn = await app.ask(query.message.chat.id, text="Please send me your watermark photo.")
    if mkn.photo:
        file_name = str(query.from_user.id) + "watermark.jpg"
        photo_id = mkn.photo.file_id
        photo_path = await app.download_media(photo_id, file_name=file_name)
        await db.set_watermark(query.from_user.id, photo_path)
        await query.message.reply_text("✅️ Your watermark has been successfully saved.")
    else:
        await query.message.reply_text("❌️ Please send a valid photo for your watermark.")



buttons1 = InlineKeyboardMarkup([
            [
                InlineKeyboardButton("Thumbnail", callback_data="thumb"),
                InlineKeyboardButton("Caption", callback_data="caption")
            ],
            [
                InlineKeyboardButton("Watermark", callback_data="watermark"),
            ]
        ])

buttons2 = InlineKeyboardMarkup([
            [
                InlineKeyboardButton("Set Thumbnail", callback_data="Sthumb"),
                InlineKeyboardButton("Remove Thumbnail", callback_data="Rthumb")
            ],
            [
                InlineKeyboardButton("View Thumbnail", callback_data="Vthumb"),
            ],
            [
                InlineKeyboardButton("Back", callback_data="back"),
            ] 
        ])

buttons3 = InlineKeyboardMarkup([
            [
                InlineKeyboardButton("Set Caption", callback_data="Scaption"),
                InlineKeyboardButton("Remove Caption", callback_data="Rcaption")
            ],
            [
                InlineKeyboardButton("View Caption", callback_data="Vcaption"),
            ],
            [
                InlineKeyboardButton("Back", callback_data="back"),
            ]
        ])

buttons4 = InlineKeyboardMarkup([
            [
                InlineKeyboardButton("Set Watermark", callback_data="Swatermark"),
                InlineKeyboardButton("Remove Watermark", callback_data="Rwatermark")
            ],
            [
                InlineKeyboardButton("View Watermark", callback_data="Vwatermark"),
            ],
            [
                InlineKeyboardButton("Back", callback_data="back"),
            ]
        ])


@app.on_message(filters.command("settings") & filters.private)
async def settings(_, message):
    await message.reply_text("Choose from Below", reply_markup=buttons1)


@app.on_callback_query()
async def callback(_, query):
    if query.data=="thumb":
        await query.message.edit_text("Choose from Below", reply_markup=buttons2)

    elif query.data=="caption":
        await query.message.edit_text(f"Choose from Below", reply_markup=buttons3)

    elif query.data=="watermark":
        await query.message.edit_text("Choose from Below", reply_markup=buttons4)

    elif query.data=="back":
        await query.message.edit_text("Choose from Below", reply_markup=buttons1)

    elif query.data=="Sthumb":
        await add_thumb(query)

    elif query.data=="Rthumb":
        await remove_thumb(query)

    elif query.data=="Vthumb":
        await view_thumb(query)

    elif query.data=="Scaption":
        await add_caption(query)

    elif query.data=="Rcaption":
        await delete_caption(query)

    elif query.data=="Vcaption":
        await see_caption(query)

    elif query.data=="Swatermark":
        await add_watermark(query)

    elif query.data=="Rwatermark":
        await remove_watermark(query)

    elif query.data=="Vwatermark":
        await view_watermark(query)
