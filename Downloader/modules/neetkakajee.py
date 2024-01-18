import json
import os
import requests
from pyrogram import filters
from pyromod import listen
import cloudscraper
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
from base64 import b64decode
from Downloader import app
from config import SUDO_USERS

def decrypt_data(encoded_data, key, iv):
    decoded_data = b64decode(encoded_data)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted_data = unpad(cipher.decrypt(decoded_data), AES.block_size)
    return decrypted_data.decode('utf-8')

@app.on_message(filters.command(["nkj"]) & filters.user(SUDO_USERS))
async def neetkaka_login(_, message):
    global cancel
    cancel = False
    editable = await message.reply_text(
        "Send **ID & Password** in this manner, otherwise, the bot will not respond.\n\nSend like this: **ID*Password**"
    )
    raw_url = "https://neetkakajeeapi.classx.co.in/post/userLogin"
    hdr = {
        "Auth-Key": "appxapi",
        "User-Id": "-2",
        "Authorization": "",
        "User_app_category": "",
        "Language": "en",
        "Content-Type": "application/x-www-form-urlencoded",
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
    res = scraper.post(raw_url, data=info, headers=hdr).content
    output = json.loads(res)

    userid = output["data"]["userid"]
    token = output["data"]["token"]

    hdr1 = {
            "Host": "neetkakajeeapi.classx.co.in",
            "Client-Service": "Appx",
            "Auth-Key": "appxapi",
            "User-Id": userid,
            "Authorization": token
            }

    await editable.edit("**login Successful**")
    res1 = requests.get("https://neetkakajeeapi.classx.co.in/get/mycourseweb?userid="+userid, headers=hdr1)
    b_data = res1.json()['data']
    cool = ""
    for data in b_data:
        t_name =data['course_name']
        FFF = "BATCH-ID - BATCH NAME - INSTRUCTOR"
        aa = f"**`{data['id']}`      - `{data['course_name']}`**\n\n"
        if len(f'{cool}{aa}') > 4096:
            print(aa)
            cool = ""
        cool += aa
    await editable.edit(f'{"**You have these batches :-"}\n\n{FFF}\n\n{cool}')
    editable = await message.reply_text("**Now send the Batch ID to Download**")
    input2: message = await _.listen(editable.chat.id)
    raw_text2 = input2.text

    scraper = cloudscraper.create_scraper()
    html = scraper.get(f"https://neetkakajeeapi.classx.co.in/get/allsubjectfrmlivecourseclass?courseid={raw_text2}",headers=hdr1).content
    output0 = json.loads(html)
    subjID = output0["data"]
    subjID_data = output0["data"]
    cool = ""
    for sub in subjID:
        subjid = sub["subjectid"]
        subjname = sub["subject_name"]
        aa = f"`{subjid}` - `{subjname}`\n\n"
        cool += aa
    await editable.edit(cool)
    


    editable = await message.reply_text("**Enter the Subject Id Show in above Response")
    input3: message = await _.listen(editable.chat.id)
    raw_text3 = input3.text

    res3 = requests.get("https://neetkakajeeapi.classx.co.in/get/alltopicfrmlivecourseclass?courseid=" +raw_text2+"&subjectid="+raw_text3, headers=hdr1)
    b_data2 = res3.json()['data']

    vj = ""
    vp = ""
    lol = ""   

    for data in b_data2:
        t_name = data["topic_name"]
        tid = data["topicid"]
        zz = len(tid)
        BBB = f"{'**TOPIC-ID    - TOPIC     - VIDEOS**'}\n"
        hh = f'`{tid}`     - **{t_name} - ({zz})**\n'
    
        vj += f"{tid}&"
        vp += f"{t_name}&"
    
        if len(f'{lol}{hh}') > 4096:
            lol = ""
    
        lol += hh
    
    await message.reply_text(f"Batch details of **{t_name}** are:\n\n{BBB}\n\n{lol}")

    
    editable = await message.reply_text(f"Now send the **Topic IDs** to Download\n\nSend like this **1&2&3&4** so on\nor copy paste or edit **below ids** according to you :\n\n**Enter this to download full batch :-**\n`{vj}`")
    input4: message = await _.listen(editable.chat.id)
    raw_text4 = input4.text

    editable = await message.reply_text("**Now send the Resolution**")
    input5: message = await _.listen(editable.chat.id)
    raw_text5 = input5.text
    try:
        xv = raw_text4.split('&')
        for y in range(0,len(xv)):
            t =xv[y]

            hdr11 = {
                    "Host": "neetkakajeeapi.classx.co.in",
                    "Client-Service": "Appx",
                    "Auth-Key": "appxapi",
                    "User-Id": userid,
                    "Authorization": token
                    }

            res4 = requests.get("https://neetkakajeeapi.classx.co.in/get/livecourseclassbycoursesubtopconceptapiv3?topicid=" + t + "&start=-1&courseid=" + raw_text2 + "&subjectid=" + raw_text3,headers=hdr11).json()

            topicid = res4["data"]
            vj = ""
            for data in topicid:
                tids = (data["Title"])
                idid = f"{tids}"
                if len(f"{vj}{idid}") > 4096:
                    vj = ""
                vj += idid

            vp = ""
            for data in topicid:
                tn = (data["download_link"])
                tns = f"{tn}"
                if len(f"{vp}{tn}") > 4096:
                    vp = ""
                vp += tn
            vs = ""
            for data in topicid:
                tn0 = (data["pdf_link"])
                tns0 = f"{tn0}"
                if len(f"{vs}{tn0}") > 4096:
                    vs = ""
                vs += tn0
            cool2 = ""
            for data in topicid:
                if data["download_link"]:
                    b64s = (data["download_link"])
                else:
                    b64s = (data["pdf_link"])
                tid = (data["Title"])
                zz = len(tid)
                key = "638udh3829162018".encode("utf8")
                iv = "fedcba9876543210".encode("utf8")
                for b64 in b64s:
                    encoded_part, encrypted_part = encoded_string.split(':')
                    b = decrypt_data(encoded_part, key, iv)
                cc0 = (f"{tid}:{b}")
                if len(f'{cool2}{cc0}') > 4096:
                    cool2 = ""
                cool2 += cc0
                mm = "NEET Kaka JEE"   
                
            with open(f'{mm}.txt', 'a') as f:
                f.write(f"{vk} : {vm}\n {vn}")
            await message.reply_document(f"{mm}.txt")
            file_path = f"{mm}.txt"
            os.remove(file_path)
    except Exception as e:
        await message.reply_text(str(e))
    await message.reply_text("Done")
