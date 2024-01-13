import os,re,sys,json,time,asyncio
import requests
from config import SUDO_USERS
from pyrogram import filters
from aiohttp import ClientSession
from pyromod import listen
from subprocess import getstatusoutput
import Downloader.modules import
from Downloader import app



# --------------------------- DRM-DL ----------------------------------------------------------------------- #

@app.on_message(filters.command(["drm"]) & filters.user(SUDO_USERS))
async def account_login(_,message):
        user = message.from_user.id
        editable = await message.reply_text('SEND TXT FILE 🗃️ OR LINKS TO DOWNLOAD 🔗 ')
        input_msg: message = await _.listen(editable.chat.id)
        if input_msg.document:
            x = await input_msg.download()
            await input_msg.delete(True)

            path = f"./downloads/{message.chat.id}"

            try:
                with open(x, "r") as f:
                    content = f.read()
                content = [i.strip() for i in content.split("\n") if i.strip()]  # Skip empty lines
                links = [i.split("://", 1) for i in content]
                os.remove(x)
            except Exception as e:
                await m.reply_text(f"Invalid file input. Error: {str(e)}")
                os.remove(x)
                return
        else:
            content = [i.strip() for i in input_msg.text.split("\n") if i.strip()]  # Skip empty lines
            links = [i.split("://", 1) for i in content]

        await editable.edit(f"Total links found are **{len(links)}**\n\nSend From where you want to download initial is **1**")
        input_msg0: message = await _.listen(editable.chat.id)
        raw_text = input_msg0.text
        await input_msg0.delete(True)

        await editable.edit("**Enter Batch Name**")
        input1: message = await _.listen(editable.chat.id)
        raw_text0 = input1.text
        await input1.delete(True)

        await editable.edit("**Enter resolution**")
        input2: message = await _.listen(editable.chat.id)
        raw_text2 = input2.text
        await input2.delete(True)
        try:
            if raw_text2 == "144":
                res = "256x144"
            elif raw_text2 == "240":
                res = "426x240"
            elif raw_text2 == "360":
                res = "640x360"
            elif raw_text2 == "480":
                res = "854x480"
            elif raw_text2 == "720":
                res = "1280x720"
            elif raw_text2 == "1080":
                res = "1920x1080"
            else:
                res = "UN"
        except Exception:
            res = "UN"

        await editable.edit("** ENTER A CAPTION TO ADD OTHERWISE SEND 👉`no`👈 **")
        input3: message = await _.listen(editable.chat.id)
        raw_text3 = input3.text
        await input3.delete(True)
        highlighter = f"️ ⁪⁬⁮⁮⁮"
        if raw_text3 == 'no':
            MR = highlighter
        else:
            MR = raw_text3

        await editable.edit("Now send the **Thumb url**\nEg » ```https://telegra.ph/file/0633f8b6a6f110d34f044.jpg```\n\nor Send `no`")
        input6 = message = await _.listen(editable.chat.id)
        raw_text6 = input6.text
        await input6.delete(True)
        await editable.delete()

        thumb = input6.text
        if thumb.startswith("http://") or thumb.startswith("https://"):
            getstatusoutput(f"wget '{thumb}' -O 'thumb.jpg'")
            thumb = "thumb.jpg"
        else:
            thumb == "no"

        if len(links) == 1:
            count = 1
        else:
            count = int(raw_text)

        try:
            for i in range(count - 1, len(links)):
                V = links[i][1].replace("file/d/", "uc?export=download&id=").replace("www.youtube-nocookie.com/embed", "youtu.be").replace("?modestbranding=1", "").replace("/view?usp=sharing", "")  # .replace("mpd","m3u8")
                url = "https://" + V

                name1 = links[i][0].replace("\t", "").replace(":", "").replace("/", "").replace("+", "").replace("#", "").replace("|", "").replace("@", "").replace("*", "").replace(".", "").replace("https", "").replace("http", "").strip()
                name = f'{str(count).zfill(3)}) {name1[:60]}'
                
                try:
                    cc = f'** {str(count).zfill(3)}.** {𝗻𝗮𝗺𝗲𝟭}{MR}.mp4\n**Batch »** {raw_text0}\n\n'

                  
                    show = f"**⥥ Downloading »**\n\n**Name »** `{name}\nQuality » {raw_text2}`\n\n**Url »** `{url}`"
                    prog = await message.reply_text(show)
                    res_file = await helper.drm_video(url, prog, name)
                    filename = res_file
                    await prog.delete(True)
                    await helper.send_vid(m, cc, filename, thumb, name, prog)
                    count += 1
                    time.sleep(1)

                except Exception as e:
                    await message.reply_text(
                        f"**Downloading Interrupted **\n{str(e)}\n**Name** » {name}\n**Link** » `{url}`"
                    )
                    continue

        except Exception as e:
            await message.reply_text(str(e))

        await message.reply_text("Done")


