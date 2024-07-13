from pyrogram import filters
from Restriction import app
from Restriction.core import script
from Restriction.core.func import subscribe
from Restriction.modules.settings import *
from pyrogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton



# ------------------------------------------------------------------------------- #

# ------------------- Start-Buttons ------------------- #

buttons = InlineKeyboardMarkup(
         [[
               InlineKeyboardButton("ᴀᴅᴍɪɴs ᴘᴀɴɴᴇʟ", callback_data="admin_"),    
         ],[
               InlineKeyboardButton("ᴄᴏᴍᴍᴀɴᴅs", callback_data="help_"),    
         ]])




# ------------------- Settings-Buttons ------------------- #

buttons1 = InlineKeyboardMarkup([
            [
                InlineKeyboardButton("🏜 ᴛʜᴜᴍʙɴᴀɪʟ", callback_data="thumb_")                
            ],
	    [
                InlineKeyboardButton("📝 ᴄᴀᴘᴛɪᴏɴ", callback_data="caption_"),
		InlineKeyboardButton("🌐 ᴄʜᴀɴɴᴇʟ", callback_data="channel_")
            ],
	    [
                InlineKeyboardButton("📊 sᴇssɪᴏɴ", callback_data="session_"),
		InlineKeyboardButton("📇 ᴡᴀᴛᴇʀᴍᴀʀᴋ", callback_data="maintainer_")
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

buttons4 = InlineKeyboardMarkup([
	    [                
                InlineKeyboardButton("✚ sᴇᴛ sᴇssɪᴏɴ", callback_data="set_session")
            ],
            [                
                InlineKeyboardButton("❌ ʀᴇᴍᴏᴠᴇ", callback_data="rm_session"),
                InlineKeyboardButton("📖 ᴠɪᴇᴡ", callback_data="views_session")
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

    elif query.data == "thumb_":
        await query.message.edit_text(script.THUMBNAIL_TXT, reply_markup=buttons2)
    elif query.data == "caption_":
        await query.message.edit_text(script.CAPTI0NS_TXT, reply_markup=buttons4)
    elif query.data == "watermark_":
        await query.message.edit_text(script.SESSION_TXT, reply_markup=buttons3)
    elif query.data == "about_":
        await query.message.edit_text(script.CHANNEL_TXT, reply_markup=buttons5)
    elif query.data == "back_":
        await query.message.edit_text(script.SETTINGS_TXT, reply_markup=buttons1)

    elif query.data == "renew_":
        await query.message.edit_text(script.CAPTI0NS_TXT, reply_markup=renew_button)
    elif query.data == "replace_":
        await query.message.edit_text(script.CAPTI0NS_TXT, reply_markup=replace_button)
    elif query.data == "words_":
        await query.message.edit_text(script.CAPTI0NS_TXT, reply_markup=words_button)    
    elif query.data == "c_back":
        await query.message.edit_text(script.CAPTI0NS_TXT, reply_markup=buttons4)

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

    
    elif query.data == "views_session":
        await view_session(query)
    elif query.data == "rm_session":
        await delete_session(query)
    elif query.data == "set_session":
        await add_session(query)

  
    elif query.data == "set_chat":
        await add_channel(query)
    elif query.data == "views_chat":
        await view_channel(query)
    elif query.data == "rm_chat":
        await delete_channel(query)
	
    elif query.data == "maintainer_":    
        await query.answer("sᴏᴏɴ.... \n ʙᴏᴛ ᴜɴᴅᴇʀ ɪɴ ᴍᴀɪɴᴛᴀɪɴᴀɴᴄᴇ", show_alert=True)

    elif query.data == "close_data":
        try:
            await query.message.delete()
            await query.message.reply_to_message.delete()
        except:
            pass






