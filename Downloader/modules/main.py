import os,re,sys,json,time,asyncio
import requests
import subprocess
from config import SUDO_USERS
from aiohttp import ClientSession
from pyromod import listen
from subprocess import getstatusoutput
from Downloader import app
from pyrogram import filters
from pyrogram.errors import FloodWait
from pyrogram.types import Message
from pyrogram.types.messages_and_media import message
from Downloader.modules import helper
from Downloader.modules.utils import progress_bar


# --------------------------------------------------------------------------------------------------------- #

@app.on_message(filters.command("stop") & filters.user(SUDO_USERS))
async def restart_handler(_, message):
    await message.reply_text("**STOPPED**🚦", True)
    os.execl(sys.executable, sys.executable, *sys.argv)




# --------------------------- VIDEO DOWNLOADER -------------------------------- #

@app.on_message(filters.command(["txt"]) & filters.user(SUDO_USERS))
async def account_login((_, m: Message):
    user = m.from_user.id if m.from_user is not None else None
    editable = await m.reply_text('SEND TXT FILE 🗃️ OR LINKS TO DOWNLOAD 🔗 ')
    input_msg: Message = await app.listen(editable.chat.id)
    if input_msg.document:
        x = await input_msg.download()
        await input_msg.delete(True)

        path = f"./downloads/{m.chat.id}"

        try:
            with open(x, "r") as f:
                content = f.read()
            content = [i.strip() for i in content.split("\n") if i.strip()]  # Skip empty lines
            links = [i.split("://", 1) for i in content]
            os.remove(x)
        except Exception as e:
            await m.reply_text(f"oops sensei Invalid file input. Error: {str(e)}")
            os.remove(x)
            return
    else:
        content = [i.strip() for i in input_msg.text.split("\n") if i.strip()]  # Skip empty lines
        links = [i.split("://", 1) for i in content]

    await editable.edit(f"Total links found are **{len(links)}**\n\nSend From where you want to download initial is **1**")
    input_msg0: Message = await app.listen(editable.chat.id)
    raw_text = input_msg0.text
    await input_msg0.delete(True)

    await editable.edit("**Enter Batch Name**")
    input1: Message = await app.listen(editable.chat.id)
    raw_text0 = input1.text
    await input1.delete(True)
 
    await editable.edit("**Enter resolution**")
    input2: Message = await app.listen(editable.chat.id)
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
    input3: Message = await app.listen(editable.chat.id)
    raw_text3 = input3.text
    await input3.delete(True)
    highlighter = f"️ ⁪⁬⁮⁮⁮"
    if raw_text3 == 'no':
        MR = highlighter
    else:
        MR = raw_text3

    await editable.edit("Now send the **Thumb url**\nEg » ```https://telegra.ph/file/0633f8b6a6f110d34f044.jpg```\n\nor Send `no`")
    input6 = message = await app.listen(editable.chat.id)
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

            if "visionias" in url:
                async with ClientSession() as session:
                    async with session.get(url, headers={'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9', 'Accept-Language': 'en-US,en;q=0.9', 'Cache-Control': 'no-cache', 'Connection': 'keep-alive', 'Pragma': 'no-cache', 'Referer': 'http://www.visionias.in/', 'Sec-Fetch-Dest': 'iframe', 'Sec-Fetch-Mode': 'navigate', 'Sec-Fetch-Site': 'cross-site', 'Upgrade-Insecure-Requests': '1', 'User-Agent': 'Mozilla/5.0 (Linux; Android 12; RMX2121) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Mobile Safari/537.36', 'sec-ch-ua': '"Chromium";v="107", "Not=A?Brand";v="24"', 'sec-ch-ua-mobile': '?1', 'sec-ch-ua-platform': '"Android"',}) as resp:
                        text = await resp.text()
                        url = re.search(r"(https://.*?playlist.m3u8.*?)\"", text).group(1)
                   
            if "awebvideos.classplusapp" in url:
        	      headers = {'Host': 'api.classplusapp.com', 'x-access-token': 'eyJhbGciOiJIUzM4NCIsInR5cCI6IkpXVCJ9.eyJuYW1lIjoiTkVFVCBDaGVtaXN0cnktIEJlV2lzZSBDbGFzc2VzIiwib3JnX2NvZGUiOiJ1Y3Z2YW8iLCJvcmdfaWQiOjU0MjQyMSwicGhvbmUiOiI5MTgyOTg3MzAwMzYiLCJzb3VyY2VfdXNlcl9pZCI6IjkyMzQyMDA1IiwidXNlcl90eXBlIjoxLCJlbWFpbCI6InN1ZGhhbnNodWpoYTE1MUBnbWFpbC5jb20iLCJjb3VudHJ5X2NvZGUiOiJJTiIsImlzX3VzZXJpZF9ldmVuIjpmYWxzZSwic291cmNlIjo1MCwic291cmNlX2FwcCI6ImNsYXNzcGx1cyIsInNlc3Npb25faWQiOiJmYmZiNjI2My1mNmFiLTRlNjAtYWViYS05OWNhN2Q0ZGI2MzUiLCJ2aXNpdG9yX2lkIjoiYTlmNDhhNzktOWQ0NC00Y2E3LTk5ODQtZDAyMDgxMjc4NWUyIiwiY3JlYXRlZF9hdCI6MTcwNDM3NTgzNzkwOSwiaWF0IjoxNzA0ODEwMTk1LCJleHAiOjE3MDYxMDYxOTV9.x0EH5qxYNrq4LtEtuffQ998ajVPkWGEJjlDYTvkgFn__lUDpcB_Qk_xioesjCswH', 'user-agent': 'Mobile-Android', 'app-version': '1.4.37.1', 'api-version': '18', 'device-id': '5d0d17ac8b3c9f51', 'device-details': '2848b866799971ca_2848b8667a33216c_SDK-30', 'accept-encoding': 'gzip'}
         	      params = (('url', f'{url}'),)
          	    response = requests.get('https://api.classplusapp.com/cams/uploader/video/jw-signed-url', headers=headers, params=params)
           	    url = response.json()['url']

            elif 'videos.classplusapp' in url:
             url = requests.get(f'https://api.classplusapp.com/cams/uploader/video/jw-signed-url?url={url}', headers={'x-access-token': 'eyJhbGciOiJIUzM4NCIsInR5cCI6IkpXVCJ9.eyJpZCI6MzgzNjkyMTIsIm9yZ0lkIjoyNjA1LCJ0eXBlIjoxLCJtb2JpbGUiOiI5MTcwODI3NzQyODkiLCJuYW1lIjoiQWNlIiwiZW1haWwiOm51bGwsImlzRmlyc3RMb2dpbiI6dHJ1ZSwiZGVmYXVsdExhbmd1YWdlIjpudWxsLCJjb3VudHJ5Q29kZSI6IklOIiwiaXNJbnRlcm5hdGlvbmFsIjowLCJpYXQiOjE2NDMyODE4NzcsImV4cCI6MTY0Mzg4NjY3N30.hM33P2ai6ivdzxPPfm01LAd4JWv-vnrSxGXqvCirCSpUfhhofpeqyeHPxtstXwe0'}).json()['url']

            elif '/master.mpd' in url:
             id =  url.split("/")[-2]
             url =  "https://d26g5bnklkwsh4.cloudfront.net/" + id + "/master.m3u8"

            name1 = links[i][0].replace("\t", "").replace(":", "").replace("/", "").replace("+", "").replace("#", "").replace("|", "").replace("@", "").replace("*", "").replace(".", "").replace("https", "").replace("http", "").strip()
            name = f'{str(count).zfill(3)}) {name1[:60]}'

            if "youtu" in url:
                ytf = f"b[height<={raw_text2}][ext=mp4]/bv[height<={raw_text2}][ext=mp4]+ba[ext=m4a]/b[ext=mp4]"
            else:
                ytf = f"b[height<={raw_text2}]/bv[height<={raw_text2}]+ba/b/bv+ba"

            if "jw-prod" in url:
                cmd = f'yt-dlp -f "bestvideo[height<={raw_text2}][ext=mp4]+bestaudio[ext=m4a]/bestvideo+bestaudio/best" -o "{name}.mp4" "{url}"'
            else:
                cmd = f'yt-dlp -f "{ytf}" "{url}" -o "{name}.mp4"'

            try:
                cc = f'** {str(count).zfill(3)}.** {𝗻𝗮𝗺𝗲𝟭}{MR}.mkv\n**Batch »** {raw_text0}\n\n'
                cc1 = f'** {str(count).zfill(3)}.** {𝗻𝗮𝗺𝗲𝟭}{MR}.pdf \n**Batch »** {raw_text0}\n\n'
                if "drive" in url:
                    try:
                        ka = await helper.download(url, name)
                        copy = await app.send_document(chat_id=m.chat.id, document=ka, caption=cc1)
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
                        copy = await app.send_document(chat_id=m.chat.id, document=f'{name}.pdf', caption=cc1)
                        count += 1
                        os.remove(f'{name}.pdf')
                    except FloodWait as e:
                        await m.reply_text(str(e))
                        time.sleep(e.x)
                        continue
                else:
                    Show = f"**⥥ Downloading »**\n\n**Name »** `{name}\nQuality » {raw_text2}`\n\n**Url »** `{url}`"
                    prog = await m.reply_text(Show)
                    res_file = await helper.download_video(url, cmd, name)
                    filename = res_file
                    await prog.delete(True)
                    await helper.send_vid(app, m, cc, filename, thumb, name, prog)
                    count += 1
                    time.sleep(1)

            except Exception as e:
                await m.reply_text(
                    f"**Downloading Interrupted **\n{str(e)}\n**Name** » {name}\n**Link** » `{url}`"
                )
                continue

    except Exception as e:
        await m.reply_text(f"Error : {e}")

    await m.reply_text("**Successfully downloaded all video !!**")