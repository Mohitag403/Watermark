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



# ---------------------------------------------------------------------------------------------------------------------  #
# EXTRA AFTER CHECHKING I WILL REMOVED THIS CODE {ANON}  

ACCOUNT_ID = "6206459123001"
BCOV_POLICY = "BCpkADawqM1474MvKwYlMRZNBPoqkJY-UWm7zE1U769d5r5kqTjG0v8L-THXuVZtdIQJpfMPB37L_VJQxTKeNeLO2Eac_yMywEgyV9GjFDQ2LTiT4FEiHhKAUvdbx9ku6fGnQKSMB8J5uIDd"
bc_url = (f"https://edge.api.brightcove.com/playback/v1/accounts/{ACCOUNT_ID}/videos")
bc_hdr = {"BCOV-POLICY": BCOV_POLICY}


# ---------------------------------------------------------------------------------------------------------------------  #


@app.on_message(filters.command(["cw"]) & filters.user(SUDO_USERS))
async def account_login(_, message):
    global cancel
    cancel = False

    url = "https://elearn.crwilladmin.com/api/v3/login-other"
    data = {
        "deviceType": "android",
        "password": "",
        "deviceIMEI": "08750aa91d7387ab",
        "deviceModel": "Realme RMX2001",
        "deviceVersion": "R(Android 11.0)",
        "email": "",
        "deviceToken": "fYdfgaUaQZmYP7vV4r2rjr:APA91bFPn3Z4m_YS8kYQSthrueUh-lyfxLghL9ka-MT0m_4TRtlUu7cy90L8H6VbtWorg95Car6aU9zjA-59bZypta9GNNuAdUxTnIiGFxMCr2G3P4Gf054Kdgwje44XWzS9ZGa4iPZh"
       }
    headers = {
        "Host": "web.careerwill.com",
        "Token": "",
        "Usertype": "2",
        "Appver": "1.55",
        "Apptype": "android",
        "Content-Type": "application/json; charset=UTF-8",
        "Content-Length": "313",
        "Accept-Encoding": "gzip, deflate, br",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36",
        'Connection': 'Keep-Alive'
       }
    
    editable = await message.reply_text("Send **ID & Password** in this manner otherwise bot will not respond.\n\nSend like this:-  **ID*Password** \n or \nSend **TOKEN** like This this:-  **TOKEN**" )
    input1: message = await _.listen(editable.chat.id)
    raw_text = input1.text
    s = requests.Session()
    if "*" in raw_text:
      data["email"] = raw_text.split("*")[0]
      data["password"] = raw_text.split("*")[1]
      await input1.delete(True)
      s = requests.Session()
      response = s.post(url = url, headers=headers, json=data, timeout=10)
      if response.status_code == 200:
          data = response.json()
          token = data["data"]["token"]
          await message.reply_text(token)
      else:
           await message.reply_text("go back to response")
      
      await message.reply_text(f"Token: ```{token}```")
    else:
      token = raw_text
    html1 = s.get("https://web.careerwill.com/api/v3/comp/my-batch?&token=" + token).json()
    topicid = html1["data"]["batchData"]
    cool=""
    for data in topicid:
        instructorName=(data["instructorName"])
        FFF="**BATCH-ID - BATCH NAME - INSTRUCTOR**"
        aa =f" ```{data['id']}```      - **{data['batchName']}**\n{data['instructorName']}\n\n"

        if len(f'{cool}{aa}')>4096:
            await message.reply_text(aa)
            cool =""
        cool+=aa
    await editable.edit(f'{"**You have these batches :-**"}\n\n{FFF}\n\n{cool}')
    editable1= await message.reply_text("**Now send the Batch ID to Download**")
    input2 = message = await _.listen(editable.chat.id)
    raw_text2 = input2.text
    html2 = s.get("https://web.careerwill.com/api/v3/comp/batch-topic/"+raw_text2+"?type=class&token="+token).json()
    topicid = html2["data"]["batch_topic"]
    bn = html2["data"]["batch_detail"]["name"]
    vj=""
    for data in topicid:
        tids = (data["id"])
        idid=f"{tids}&"
        if len(f"{vj}{idid}")>4096:
            await message.reply_text(idid)
            vj = ""
        vj+=idid
    vp = ""
    for data in topicid:
        tn = (data["topicName"])
        tns=f"{tn}&"
        if len(f"{vp}{tn}")>4096:
            await message.reply_text(tns)
            vp=""
        vp+=tns
    cool1 = ""
    for data in topicid:
        t_name=(data["topicName"].replace(" ",""))
        tid = (data["id"])
        scraper = cloudscraper.create_scraper()
        ffx = s.get("https://web.careerwill.com/api/v3/comp/batch-detail/"+raw_text2+"?redirectBy=mybatch&topicId="+tid+"&token="+token).json()
           
        vcx =ffx["data"]["class_list"]["batchDescription"]
        vvx =ffx["data"]["class_list"]["classes"]
        vvx.reverse()
        zz= len(vvx)
        BBB = f"{'**TOPIC-ID - TOPIC - VIDEOS**'}"
        hh = f"```{tid}```     - **{t_name} - ({zz})**\n"



        if len(f'{cool1}{hh}')>4096:
            await message.reply_text(hh)
            cool1=""
        cool1+=hh
    await message.reply_text(f'Batch details of **{bn}** are:\n\n{BBB}\n\n{cool1}\n\n**{vcx}**')
    editable2= await message.reply_text(f"Now send the **Topic IDs** to Download\n\nSend like this **1&2&3&4** so on\nor copy paste or edit **below ids** according to you :\n\n**Enter this to download full batch :-**\n```{vj}```")    
    input3 = message = await _.listen(editable.chat.id)
    raw_text3 = input3.text
    try:
        xv = raw_text3.split('&')
        for y in range(0,len(xv)):
            t =xv[y]
        


            html4 = s.get("https://web.careerwill.com/api/v3/comp/batch-detail/"+raw_text2+"?redirectBy=mybatch&topicId="+t+"&token="+token).content
            ff = json.loads(html4)
            
            mm = ff["data"]["class_list"]["batchName"].replace("/ "," ")
            vv =ff["data"]["class_list"]["classes"]
            vv.reverse()
            
            count = 1
            try:
                for data in vv:
                    vidid = (data["id"])
                    lessonName = (data["lessonName"]).replace("/", "_")
                    
                    bcvid = (data["lessonUrl"][0]["link"])
                   

                    if bcvid.startswith("62"):
                        try:
                           
                            html6 = s.get(f"{bc_url}/{bcvid}", headers=bc_hdr).content
                            video = json.loads(html6)
                            video_source = video["sources"][5]
                            video_url = video_source["src"]
                        
                            html5 = s.get("https://web.careerwill.com/api/v3/livestreamToken?type=brightcove&vid="+vidid+"&token="+token).content
                            surl = json.loads(html5)
                            stoken = surl["data"]["token"]
                            
                            
                            link = (video_url+"&bcov_auth="+stoken)
                            
                        except Exception as e:
                            print(str(e))
                    
                    elif bcvid.startswith("63"):
                        try:
                            
                            html7 = s.get(f"{bc_url}/{bcvid}", headers=bc_hdr).content
                            video1 = json.loads(html7)
                            video_source1 = video1["sources"][5]
                            video_url1 = video_source1["src"]
                            
                            html8 = s.get("https://web.careerwill.com/api/v3/livestreamToken?type=brightcove&vid="+vidid+"&token="+token).content
                            surl1 = json.loads(html8)
                            stoken1 = surl1["data"]["token"]
                            
                            
                            link = (video_url1+"&bcov_auth="+stoken1)
                          
                        except Exception as e:
                            print(str(e))
                    
                    else:
                        link=("https://www.youtube.com/embed/"+bcvid)
                    cc = (f"{lessonName}::{link}")
                    with open(f"{mm }{t_name}.txt", 'a') as f:
                        f.write(f"{lessonName}:{link}\n")
                    await message.reply_document(f"{mm }{t_name}.txt")
            except Exception as e:
                await message.reply_text(str(e))
        await message.reply_document(f"{mm }{t_name}.txt")
        os.remove(f"{mm }{t_name}.txt")
    except Exception as e:
        await message.reply_text(str(e))
    try:
        notex = await message.reply_text("Do you want download notes ?\n\nSend **y** or **n**")
        input5:message = await _.listen (editable.chat.id)
        raw_text5 = input5.text
        if raw_text5 == 'y':
            scraper = cloudscraper.create_scraper()
            html7 = scraper.get("https://web.careerwill.com/api/v3/comp/batch-notes/"+raw_text2+"?topicid="+raw_text2+"&token="+token).content
            pdfD=json.loads(html7)
            k=pdfD["data"]["notesDetails"]
            bb = len(pdfD["data"]["notesDetails"])
            ss = f"Total PDFs Found in Batch id **{raw_text2}** is - **{bb}** "
            await message.reply_text(ss)
            k.reverse()
            count1 = 1
            try:
                
                for data in k:
                    name=(data["docTitle"])
                    s=(data["docUrl"]) 
                    xi =(data["publishedAt"])
                    with open(f"{mm }{t_name}.txt", 'a') as f:
                        f.write(f"{name}:{s}\n")
                    continue
                await message.reply_document(f"{mm }{t_name}.txt")
                    
            except Exception as e:
                await message.reply_text(str(e))
            
    except Exception as e:
        print(str(e))
    await message.reply_text("Done")
