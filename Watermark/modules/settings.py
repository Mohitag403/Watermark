from pyrogram import Client, filters
from pyrogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
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


buttons1 = InlineKeyboardMarkup([
            [
                InlineKeyboardButton("Thumbnail", callback_data="thumb"),
                InlineKeyboardButton("Caption", callback_data="caption")
            ]
        ])

buttons2 = InlineKeyboardMarkup([
            [
                InlineKeyboardButton("Set Thumbnail", callback_data="Sthumb"),
                InlineKeyboardButton("Remove Thumbnail", callback_data="Rthumb")
            ],
            [
                InlineKeyboardButton("View Thumbnail", callback_data="Vthumb"),
            ]
        ])

buttons3 = InlineKeyboardMarkup([
            [
                InlineKeyboardButton("Set Caption", callback_data="Scaption"),
                InlineKeyboardButton("Remove Caption", callback_data="Rcaption")
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
        caption = await see_caption(query)
        await query.message.edit_text(f"Choose from Below\n\n**ʏᴏᴜʀ ᴄᴀᴘᴛɪᴏɴ:** `{caption}`", reply_markup=buttons3)

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


