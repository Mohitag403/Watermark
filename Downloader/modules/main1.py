import os,re,sys,json,time,asyncio
import requests
import subprocess
from config import SUDO_USERS
from aiohttp import ClientSession
from pyromod import listen
from subprocess import getstatusoutput
from Downloader import app
from Downloader.core import helper
from pyrogram import filters
from pyrogram.errors import FloodWait


# --------------------------------------------------------------------------------------------------------- #

@app.on_message(filters.command("stop") & filters.user(SUDO_USERS))
async def restart_handler(_, message):
    await message.reply_text("**STOPPED**🚦", True)
    os.execl(sys.executable, sys.executable, *sys.argv)




# --------------------------- VIDEO DOWNLOADER -------------------------------- #

@app.on_message(filters.command(["txt"]) & filters.user(SUDO_USERS))
async def account_login(_, message):
    editable = await message.reply_text("**SEND TXT FILE 🗃️ OR LINKS TO DOWNLOAD 🔗**")
    input: message = await _.listen(editable.chat.id)
    url_pattern = re.compile(r'https?://\S+|www\.\S+')
    if input.document:
        x = await input.download()
        await input.delete(True)

        path = f"./downloads/{message.chat.id}"
 
        try:
           with open(x, "r") as f:
               content = f.read()
           content = content.split("\n")
           lols = []
           for i in content:
                if i.strip() and "://" in i:
                    lols.append(i)
           os.remove(x)
            
        except Exception as e:
            await message.reply_text(f"Invalid file input. Error: {str(e)}")
            os.remove(x)
            return
    
    else:
        content = input.text
        content = content.split("\n")
        lols = []
        for i in content:
            if i.strip() and "://" in i:
                lols.append(i)

    links = []
    for lol in lols:
        link = re.findall(url_pattern, lol)
        links.append(link)
    
    await editable.edit(f"Total links found are **{len(links)}**\n\nSend From where you want to download initial is **1**")
    input0: message = await _.listen(editable.chat.id)
    raw_text = input0.text
    await input0.delete(True)

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
    
    

    await editable.edit("**Enter A Highlighter (Download By) **")
    input3: message = await _.listen(editable.chat.id)
    raw_text3 = input3.text
    await input3.delete(True)
    highlighter  = f"️ ⁪⁬⁮⁮⁮"
    if raw_text3 == 'Co':
        MR = highlighter 
    else:
        MR = raw_text3
   
    await editable.edit("Now send the **Thumb url**\nEg : ```https://telegra.ph/file/0633f8b6a6f110d34f044.jpg```\n\nor Send `no`")
    input6: message = await _.listen(editable.chat.id)
    raw_text6 = input6.text
    await input6.delete(True)
    await editable.delete()

    thumb = input6.text
    if thumb.startswith("http://") or thumb.startswith("https://"):
        getstatusoutput(f"wget '{thumb}' -O 'thumb.jpg'")
        thumb = f"thumb.jpg"
    else:
        thumb == "no"

    if len(links) == 1:
        count = 1
    else:
        count = int(raw_text)

    try:
        for i in range(count - 1, len(links)):
            url = links[i].replace("file/d/","uc?export=download&id=").replace("www.youtube-nocookie.com/embed", "youtu.be").replace("?modestbranding=1", "").replace("/view?usp=sharing","") # .replace("mpd","m3u8")

            if '/master.mpd' in url:
             id =  url.split("/")[-2]
             url =  "https://d26g5bnklkwsh4.cloudfront.net/" + id + "/master.m3u8"

            for lol in lols:
              name1 = re.sub(url_pattern, '', lol)
              name = f'{str(count).zfill(3)}) {name1[:60]}'

            if "youtu" in url:
                ytf = f"b[height<={raw_text2}][ext=mp4]/bv[height<={raw_text2}][ext=mp4]+ba[ext=m4a]/b[ext=mp4]"
            else:
                ytf = f"b[height<={raw_text2}]/bv[height<={raw_text2}]+ba/b/bv+ba"

            if "jw-prod" in url:
                cmd = f'yt-dlp -o "{name}.mp4" "{url}"'
            else:
                cmd = f'yt-dlp -f "{ytf}" "{url}" -o "{name}.mp4"'

            try:  
                cc = f'**{str(count).zfill(3)} **{name1}**.mkv **{res}** \n\n**Bᴀᴛᴄʜ :** **{raw_text0}**\n\n**Dᴏᴡɴʟᴏᴀᴅᴇᴅ Bʏ : ** **{raw_text3}**\n\n'
                cc1 = f'**{str(count).zfill(3)}\n**Pᴅғ Tɪᴛʟᴇ :** **{name1}** .pdf \n**Bᴀᴛᴄʜ :** **{raw_text0}**\n\n'

                if "drive" in url:
                    try:
                        ka = await helper.download(url, name)
                        copy = await _.send_document(message.chat.id, document=ka, caption=cc1)
                        count += 1
                        os.remove(ka)
                        time.sleep(1)
                    except FloodWait as e:
                        await m.reply_text(str(e))
                        time.sleep(e.x)
                        continue

                
                elif ".pdf" in url:
                    try:
                        cmd = f'yt-dlp -o "{name}.pdf" "{url}"'
                        download_cmd = f"{cmd} -R 25 --fragment-retries 25"
                        os.system(download_cmd)
                        copy = await _.send_document(message.chat.id, document=f'{name}.pdf', caption=cc1)
                        count += 1
                        os.remove(f'{name}.pdf')
                    except FloodWait as e:
                        await message.reply_text(str(e))
                        time.sleep(e.x)
                        continue

                else:
                    show = f"**⥥ Downloading »**\n\n**Name »** `{name}\nQuality » {raw_text2}`\n\n**Url »** `{url}`"
                    prog = await message.reply_text(show)
                    res_file = await helper.download_video(url, cmd, name)
                    filename = res_file
                    await prog.delete(True)
                    await helper.send_vid(message, cc, filename, thumb, name, prog)
                    count += 1
                    time.sleep(1)


            

            except Exception as e:
                await message.reply_text(f"Error: {str(e)}\n\n**Name** - {name}\n**Link** - `{url}`")
                continue

    except Exception as e:
        await message.reply_text(f"Error : {e}")
    await message.reply_text("Successfully downloaded all video !!")
