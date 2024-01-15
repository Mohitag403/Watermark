import urllib
import urllib.parse
import requests
import json
import subprocess
import os, sys, re, time
from pyromod import listen
from pyrogram import filters
from pyrogram.errors import FloodWait
from subprocess import getstatusoutput
import logging
from Downloader import app
from config import SUDO_USERS
import cloudscraper
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
from base64 import b64encode, b64decode



@app.on_message(filters.command(["exampur"]) & filters.user(SUDO_USERS))
async def account_login(_, message):
    global cancel
    cancel = False
    editable = await message.reply_text(
        "Send **ID & Password** in this manner otherwise bot will not respond.\n\nSend like this:-  **ID*Password**")
    rwa_url = "https://auth.exampurcache.xyz/auth/login"
    
    hdr = {
           "appauthtoken": "no_token",
           "User-Agent": "Dart/2.15(dart:io)",
           "content-type": "application/json; charset=UTF-8",       
           "Accept-Encoding": "gzip",
           "content-length": "94",
           "host": "auth.exampurcache.xyz" 
          }
    info={"phone_ext": "91", "phone": "", "email": "", "password": ""}
    
    input1: message = await _.listen(editable.chat.id)
    raw_text = input1.text
    info["email"] = raw_text.split("*")[0]
    info["password"] = raw_text.split("*")[1]
    await input1.delete(True)
    scraper = cloudscraper.create_scraper()
    res = scraper.post(rwa_url, data=info).content
    output = json.loads(res)
    
    token = output["data"]["authToken"]
    hdr1 = {
            "appauthtoken": token,
            "User-Agent": "Dart/2.15(dart:io)",
            "Accept-Encoding": "gzip",
            "host": "auth.exampurcache.xyz"
            }
    await editable.edit("**login Successful**")

    res1 = requests.get("https://auth.exampurcache.xyz/mycourses", headers=hdr1)
    b_data = res1.json()['data']
    cool = ""
    for data in b_data:
        FFF = "**BATCH-ID - BATCH NAME - INSTRUCTOR**"
        aa = f" ```{data['_id']}```      - **{data['title']}**\n\n"
       
        if len(f'{cool}{aa}') > 4096:
            print(aa)
            cool = ""
        cool += aa
    await editable.edit(f'{"**You have these batches :-**"}\n\n{FFF}\n\n{cool}')
    editable1 = await message.reply_text("**Now send the Batch ID to Download**")
    input2 = message = await _.listen(editable.chat.id)
    raw_text2 = input2.text

    scraper = cloudscraper.create_scraper()
    html = scraper.get("https://auth.exampurcache.xyz/course_subject/" + raw_text2,headers=hdr1).content
    output0 = json.loads(html)
    subjID = output0["data"]
    vj = ""
    for data in subjID:
       tids = (data["_id"])
       b = (data["title"])
       idid = f"{tids}&"
       if len(f"{vj}{idid}") > 4096:
          vj = ""
       vj += idid
    raw=vj
    await message.reply_text(raw)

    editable= await message.reply_text(f"Now send the **Topic IDs** to Download\n\nSend like this **1&2&3&4** so on\nor copy paste or edit **below ids** according to you :\n\n**Enter this to download full batch :-**\n```{raw}```")
    input4 = message = await _.listen(editable.chat.id)
    raw_text4 = input4.text
    try:
        xv = raw_text4.split('&')
        for y in range(0,len(xv)):
            t =xv[y]

            res4 = requests.get("https://auth.exampurcache.xyz/course_material/chapter/"+t+"/" + raw_text2,headers=hdr1)
            b_data2 = res4.json()['data']
            
            vj = ""
            for i in range(0, len(b_data2)):
               tids = (b_data2[i])
               idid = f"{tids}"
               if len(f"{vj}{idid}") > 4096:
                  vj = ""
               encoded_URL = urllib.parse.quote(idid, safe="")
               chapter = encoded_URL.replace("%28", "(").replace("%29", ")").replace("%26", "&")
               vj += chapter
               res5 = requests.get("https://auth.exampurcache.xyz/course_material/material/"+t+"/"+raw_text2+"/"+chapter,headers=hdr1)
               b_data3 = res5.json()['data']
               vk = ""
               for data in b_data3:
                  tids = (data["video_link"])
                  b = (data["title"])
                  idid = f"{tids}&"
                  if len(f"{vk}{idid}") > 4096:
                       vk = ""
                  vk += idid
                  cc = (f"{b}:{tids}")
                  mm = "Exampur"
                  with open(f'{mm}.txt', 'a') as f:
                      f.write(f"{b}:{tids}\n")
            await message.reply_document(f"{mm}.txt")
    except Exception as e:
        await message.reply_text(str(e))
    await message.reply_text("Done")