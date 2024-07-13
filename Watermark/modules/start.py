from pyrogram import filters
from Watermark import app
from Watermark.core import script
from Watermark.core.func import subscribe
from Watermark.modules.settings import *
from pyrogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton



# ------------------------------------------------------------------------------- #

# ------------------- Start-Buttons ------------------- #

buttons = InlineKeyboardMarkup(
         [[
               InlineKeyboardButton("ᴄᴏᴍᴍᴀɴᴅs", callback_data="help_"),    
         ]])




# ------------------- Settings-Buttons ------------------- #

buttons1 = InlineKeyboardMarkup([
	    [
                InlineKeyboardButton("📝 ᴄᴀᴘᴛɪᴏɴ", callback_data="caption_"),
		InlineKeyboardButton("🌐 ᴛʜᴜᴍʙ", callback_data="thumbnail_")
            ],
	    [
                InlineKeyboardButton("📊 ᴀʙᴏᴜᴛ", callback_data="about_"),
		InlineKeyboardButton("📇 ᴡᴀᴛᴇʀᴍᴀʀᴋ", callback_data="watermark_")
            ]])


# ------------------- Thumb-Buttons ------------------- #

buttons2 = InlineKeyboardMarkup([
            [
                InlineKeyboardButton("✚ sᴇᴛ ᴛʜᴜᴍʙɴᴀɪʟ", callback_data="set_thumb")              
            ],
            [
		InlineKeyboardButton("❌ ʀᴇᴍᴏᴠᴇ", callback_data="rm_thumb"),
                InlineKeyboardButton("📖 ᴠɪᴇᴡ", callback_data="views_thumb"),
            ],
            [
                InlineKeyboardButton("ʙᴀᴄᴋ", callback_data="back_"),
            ] 
        ])



# ------------------- Caption-Buttons ------------------- #


buttons3 = InlineKeyboardMarkup([
	    [                
                InlineKeyboardButton("✚ ᴀᴅᴅ ᴄᴀᴘᴛɪᴏɴ", callback_data="set_caption"),
            ],
            [                
                InlineKeyboardButton("❌ ʀᴇᴍᴏᴠᴇ", callback_data="rm_caption"),
                InlineKeyboardButton("📖 ᴠɪᴇᴡ", callback_data="views_caption")
            ],
            [
                InlineKeyboardButton("ʙᴀᴄᴋ", callback_data="c_back"),
            ]
        ])




# ------------------- Watermak-Text ------------------- #

watermark_button = InlineKeyboardMarkup(
         [[
            InlineKeyboardButton("ᴡᴀᴛᴇʀᴍᴀʀᴋ ᴛᴇxᴛ", callback_data="watermark_text"),
	 ],[
	    InlineKeyboardButton("ᴡᴀᴛᴇʀᴍᴀʀᴋ ɪᴍᴀɢᴇ", callback_data="watermark_image")   
         ]])


# ------------------- Watermak-Text ------------------- #

buttons4 = InlineKeyboardMarkup([
	    [                
                InlineKeyboardButton("✚ sᴇᴛ ᴡᴀᴛᴇʀᴍᴀʀᴋ", callback_data="set_watermarktxt")
            ],
            [                
                InlineKeyboardButton("❌ ʀᴇᴍᴏᴠᴇ", callback_data="rm_watermarktxt"),
                InlineKeyboardButton("📖 ᴠɪᴇᴡ", callback_data="views_watermarktxt")
            ],
            [
                InlineKeyboardButton("ʙᴀᴄᴋ", callback_data="back_"),
            ]
        ])

# ------------------- Watermak-Image ------------------- #

buttons5 = InlineKeyboardMarkup([
	    [                
                InlineKeyboardButton("✚ sᴇᴛ ᴡᴀᴛᴇʀᴍᴀʀᴋ", callback_data="set_watermarlimg")
            ],
            [                
                InlineKeyboardButton("❌ ʀᴇᴍᴏᴠᴇ", callback_data="rm_watermarlimg"),
                InlineKeyboardButton("📖 ᴠɪᴇᴡ", callback_data="views_watermarlimg")
            ],
            [
                InlineKeyboardButton("ʙᴀᴄᴋ", callback_data="back_"),
            ]
        ])




# ------------------------------------------------------------------------------- #


@app.on_message(filters.command("start"))
async def start(_, message):
    join = await subscribe(_, message)
    if join == 1:
        return
    await message.reply_photo(photo="https://graph.org/file/cd103d651acc5dc6edc6b.jpg",
                                  caption=script.START_TXT.format(message.from_user.mention), reply_markup=buttons)




@app.on_callback_query()
async def handle_callback(_, query):

    if query.data == "home_":                
        await query.message.edit_text(
            script.START_TXT.format(query.from_user.mention),
            reply_markup=buttons
        )

    
    elif query.data == "help_":
        reply_markup = InlineKeyboardMarkup(back_button)
        await query.message.edit_text(
            script.HELP_TXT,
            reply_markup=reply_markup
        )

    elif query.data == "thumbnail_":
        await query.message.edit_text(script.THUMBNAIL_TXT, reply_markup=buttons2)
    elif query.data == "caption_":
        await query.message.edit_text(script.CAPTI0NS_TXT, reply_markup=buttons3)
    elif query.data == "watermark_":
        await query.message.edit_text(script.WATERMARK_TXT, reply_markup=watermark_button)
    elif query.data == "watermark_text":
        await query.message.edit_text(script.WATERMARK_TXT, reply_markup=buttons4)
    elif query.data == "watermark_image":
        await query.message.edit_text(script.WATERMARK_TXT, reply_markup=buttons5)
	    
    elif query.data == "about_":
        await query.message.edit_text(script.ABOUT_TXT, reply_markup=buttons1)
    elif query.data == "back_":
        await query.message.edit_text(script.SETTINGS_TXT, reply_markup=buttons1)

    
    elif query.data == "set_thumb":
        await add_thumb(query)
    elif query.data == "rm_thumb":
        await remove_thumb(query)
    elif query.data == "views_thumb":
        await view_thumb(query)

    elif query.data == "set_caption":
        await add_caption(query)
    elif query.data == "rm_caption":
        await delete_caption(query)
    elif query.data == "views_caption":
        await see_caption(query)

    
    elif query.data == "set_watermarktxt:
        await add_watermark_text(query)
    elif query.data == "rm_watermarktxt":
        await delete_watermark_text(query)
    elif query.data == "views_watermarktxt":
        await view_watermark_text(query)
    
  
    elif query.data == "set_watermarkimg":
        await add_watermark(query)
    elif query.data == "rm_watermarkimg":
        await delete_watermark(query)
    elif query.data == "views_watermarkimg":
        await view_watermark(query)

	
	
    elif query.data == "maintainer_":    
        await query.answer("sᴏᴏɴ.... \n ʙᴏᴛ ᴜɴᴅᴇʀ ɪɴ ᴍᴀɪɴᴛᴀɪɴᴀɴᴄᴇ", show_alert=True)

    elif query.data == "close_data":
        try:
            await query.message.delete()
            await query.message.reply_to_message.delete()
        except:
            pass






