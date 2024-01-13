import os,time,asyncio,datetime,requests
import aiohttp
import logging
import subprocess
from Downloader import app
from Downloader.modules.utils import progress_bar
from pyrogram import filters



def duration(filename):
    result = subprocess.run(["ffprobe", "-v", "error", "-show_entries",
                             "format=duration", "-of",
                             "default=noprint_wrappers=1:nokey=1", filename],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT)
    return float(result.stdout)
    

async def download(url,name):
    ka = f'{name}.pdf'
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status == 200:
                f = await aiofiles.open(ka, mode='wb')
                await f.write(await resp.read())
                await f.close()
    return ka



async def download_video(url,cmd, name):
    download_cmd = f'{cmd} -R 25 --fragment-retries 25 --external-downloader aria2c --downloader-args "aria2c: -x 16 -j 32"'
    global failed_counter
    print(download_cmd)
    logging.info(download_cmd)
    k = subprocess.run(download_cmd, shell=True)
    if "visionias" in cmd and k.returncode != 0 and failed_counter <= 10:
        failed_counter += 1
        await asyncio.sleep(5)
        await download_video(url, cmd, name)
    failed_counter = 0
    try:
        if os.path.isfile(name):
            return name
        elif os.path.isfile(f"{name}.webm"):
            return f"{name}.webm"
        name = name.split(".")[0]
        if os.path.isfile(f"{name}.mkv"):
            return f"{name}.mkv"
        elif os.path.isfile(f"{name}.mp4"):
            return f"{name}.mp4"
        elif os.path.isfile(f"{name}.mp4.webm"):
            return f"{name}.mp4.webm"

        return name
    except FileNotFoundError as exc:
        return os.path.isfile.splitext[0] + "." + "mp4"


async def send_vid(m,cc,filename,thumb,name,prog):
    subprocess.run(f'ffmpeg -i "{filename}" -ss 00:01:00 -vframes 1 "{filename}.jpg"', shell=True)
    await prog.delete (True)
    reply = await m.reply_text(f"**⥣ Uploading ...** » `{name}`")
    try:
        if thumb == "no":
            thumbnail = f"{filename}.jpg"
        else:
            thumbnail = thumb
    except Exception as e:
        await m.reply_text(str(e))
    dur = int(duration(filename))
    start_time = time.time()
    try:
        await m.reply_video(filename,caption=cc, supports_streaming=True,height=720,width=1280,thumb=thumbnail,duration=dur, progress=progress_bar,progress_args=(reply,start_time))
    except Exception:
        await m.reply_video(filename,caption=cc, progress=progress_bar,progress_args=(reply,start_time))
    os.remove(filename)

    os.remove(f"{filename}.jpg")
    await reply.delete (True)


async def drm_video(url, linkkey, prog, name):
    keys = linkkey
                    
    cmd1 = f'yt-dlp -k --allow-unplayable-formats -f "bestvideo.3/bestvideo.2/bestvideo" --fixup never "{url}" --external-downloader aria2c --external-downloader-args "-x 16 -s 16 -k 1M" -o "{name}.mp4" --exec echo'
    cmd2 = f'yt-dlp -k --allow-unplayable-formats -f ba --fixup never "{url}" --external-downloader aria2c --external-downloader-args "-x 16 -s 16 -k 1M" -o "{name}.m4a" --exec echo'
    os.system(cmd1)
    os.system(cmd2)
    avDir = os.listdir
    print(avDir)
    
    await prog.edit("**Decrypting Video.....**")
    cmd3 = f'mp4decrypt --key {keys} --show-progress "{name}.mp4" "video.mp4"'
    os.system(cmd3)
    os.remove(f'{name}.mp4')
    cmd4 = f'mp4decrypt --key {keys} --show-progress "{name}.m4a" "audio.m4a"'
    os.system(cmd4)
    os.remove(f'{name}.m4a')

    await prog.edit("**Merging....**")
    cmd5 = f'ffmpeg -i "video.mp4" -i "audio.m4a" -c copy "{name}.mp4"'
    os.system(cmd5)
    os.remove(f"video.mp4")
    os.remove(f"audio.m4a")

    return f"{name}.mp4"


    
