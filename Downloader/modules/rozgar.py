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







@app.on_message(filters.command(["rgp"]) & filters.user(SUDO_USERS))
async def account_login(_, message):
    global cancel
    cancel = False
    editable = await message.reply_text("Send **ID & Password** in this manner otherwise bot will not respond.\n\nSend like this:-  **ID*Password**")
    rwa_url = "https://rozgarapinew.teachx.in/post/userLogin"
    hdr = {"Auth-Key": "appxapi",
           "User-Id": "-2",
           "Authorization": "",
           "User_app_category": "",
           "Language": "en",
           "Content-Type": "application/x-www-form-urlencoded",
           "Content-Length": "233",
           "Accept-Encoding": "gzip, deflate",
           "User-Agent": "okhttp/4.9.1"
          }
    info = {"email": "", "password": ""}
    
    input1: message = await _.listen(editable.chat.id)
    raw_text = input1.text
    info["email"] = raw_text.split("*")[0]
    info["password"] = raw_text.split("*")[1]
    await input1.delete(True)
    scraper = cloudscraper.create_scraper()
    res = scraper.post(rwa_url, data=info, headers=hdr).content
    output = json.loads(res)
  
    userid = output["data"]["userid"]
    token = output["data"]["token"]
    hdr1 = {
        "Host": "rozgarapinew.teachx.in",
        "Client-Service": "Appx",
        "Auth-Key": "appxapi",
        "User-Id": userid,
        "Authorization": token
        }
    
    await editable.edit("**login Successful**")

    cour_url = "https://rozgarapinew.teachx.in/get/mycourse?userid="

    res1 = requests.get("https://e1coachingcenterapi.classx.co.in/get/mycourse?userid="+userid, headers=hdr1)
    b_data = res1.json()['data']
    cool = ""
    for data in b_data:
        t_name =data['course_name']
        FFF = "**BATCH-ID - BATCH NAME - INSTRUCTOR**"
        aa = f" ```{data['id']}```      - **{data['course_name']}**\n\n"
        
        if len(f'{cool}{aa}') > 9999:
            print(aa)
            cool = ""
        cool += aa
    await editable.edit(f'{"**You have these batches :-**"}\n\n{FFF}\n\n{cool}')
    editable = await message.reply_text("**Now send the Batch ID to Download**")
    input2 : message = await _.listen(editable.chat.id)
    raw_text2 = input2.text

    scraper = cloudscraper.create_scraper()
    html = scraper.get("https://rozgarapinew.teachx.in/get/allsubjectfrmlivecourseclass?courseid=" + raw_text2,headers=hdr1).content
    output0 = json.loads(html)
    subjID = output0["data"]
    await message.reply_text(subjID)
    

    editable = await message.reply_text("**Enter the Subject Id Show in above Response")
    input3 : message = await _.listen(editable.chat.id)
    raw_text3 = input3.text

    res3 = requests.get("https://rozgarapinew.teachx.in/get/alltopicfrmlivecourseclass?courseid=" + raw_text2,"&subjectid=" + raw_text3, headers=hdr1)
    b_data2 = res3.json()['data']
   
    vj = ""
    for data in b_data2:
        tids = (data["topicid"])
        idid = f"{tids}&"
        if len(f"{vj}{idid}") > 9999:
           
            vj = ""
        vj += idid
   
    vp = ""
    for data in b_data2:
        tn = (data["topic_name"])
        tns = f"{tn}&"
        if len(f"{vp}{tn}") > 9999:
            
            vp = ""
        vp += tns
   
    cool1 = ""
   
    for data in b_data2:
        t_name = (data["topic_name"])
        tid = (data["topicid"])
        zz = len(tid)
        BBB = f"{'**TOPIC-ID    - TOPIC     - VIDEOS**'}\n"
        hh = f"```{tid}```     - **{t_name} - ({zz})**\n"
        
        if len(f'{cool1}{hh}') > 9999:
            cool1 = ""
        cool1 += hh
    await message.reply_text(f'Batch details of **{t_name}** are:\n\n{BBB}\n\n{cool1}')

    editable = await message.reply_text(f"Now send the **Topic IDs** to Download\n\nSend like this **1&2&3&4** so on\nor copy paste or edit **below ids** according to you :\n\n**Enter this to download full batch :-**\n```{vj}```")
    input4 : message = await _.listen(editable.chat.id)
    raw_text4 = input4.text

    editable = await message.reply_text("**Now send the Resolution**")
    input5 : message = await _.listen(editable.chat.id)
    raw_text5 = input5.text
    try:
        xv = raw_text4.split('&')
        for y in range(0,len(xv)):
            t =xv[y]

            hdr11 = {
                    "Host": "rozgarapinew.teachx.in",
                    "Client-Service": "Appx",
                    "Auth-Key": "appxapi",
                    "User-Id": userid,
                    "Authorization": token
                    }

            res4 = requests.get("https://rozgarapinew.teachx.in/get/livecourseclassbycoursesubtopconceptapiv3?topicid=" + t + "&start=-1&conceptid=1&courseid=" + raw_text2 + "&subjectid=" + raw_text3,headers=hdr11).json()

            topicid = res4["data"]
            vj = ""
            for data in topicid:
                tids = (data["Title"])
                idid = f"{tids}"
                if len(f"{vj}{idid}") > 9999:
                    vj = ""
                vj += idid

            vp = ""
            for data in topicid:
                tn = (data["download_link"])
                tns = f"{tn}"
                if len(f"{vp}{tn}") > 9999:
                    vp = ""
        
                vp += tn
            vs = ""
            for data in topicid:
                tn0 = (data["pdf_link"])
                tns0 = f"{tn0}"
                if len(f"{vs}{tn0}") > 9999:
                    vs = ""
            
                vs += tn0
            cool2 = ""
          
            for data in topicid:
                if data["download_link"]:
                    b64 = (data["download_link"])
                else:
                    b64 = (data["pdf_link"])
                tid = (data["Title"])
                zz = len(tid)
                key = "638udh3829162018".encode("utf8")
                iv = "fedcba9876543210".encode("utf8")
                ciphertext = bytearray.fromhex(b64decode(b64.encode()).hex())
                cipher = AES.new(key, AES.MODE_CBC, iv)
                plaintext = unpad(cipher.decrypt(ciphertext), AES.block_size)
               
                b=plaintext.decode('utf-8')
                cc0 = (f"{tid}:{b}")
                if len(f'{cool2}{cc0}') > 9999:
                   
                    cool2 = ""
                cool2 += cc0
                mm = "rojgar -Institute"
               
                
                with open(f'{mm}{t_name}.txt', 'a') as f:
                    f.write(f"{tid}:{b}\n")
        await message.reply_document(f"{mm}{t_name}.txt")
    except Exception as e:
        await message.reply_text(str(e))
    await message.reply_text("Done")
    os.remove(f"{mm}{t_name}.txt")
