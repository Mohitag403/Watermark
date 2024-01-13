import requests
import json
from pyrogram import filters
from pyromod import listen
import cloudscraper
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
from base64 import b64decode
from Downloader import app



async def gentxt(app, message):
    def decode(tn):
        key = "638udh3829162018".encode("utf8")
        iv = "fedcba9876543210".encode("utf8")
        ciphertext = bytearray.fromhex(b64decode(tn.encode()).hex())
        cipher = AES.new(key, AES.MODE_CBC, iv)
        plaintext = unpad(cipher.decrypt(ciphertext), AES.block_size)
        url = plaintext.decode('utf-8')
        return url

    rw_url = "https://rgvikramjeetapi.classx.co.in/post/userLogin"
    hdr = {
        "Auth-Key": "appxapi",
        "User-Id": "-2",
        "Authorization": "",
        "User_app_category": "",
        "Language": "en",
        "Content-Type": "application/x-www-form-urlencoded",
        "Content-Length": "233",
        "Accept-Encoding": "gzip, deflate",
        "User-Agent": "okhttp/4.9.1"
    }

    try:
        editable = await message.reply_text("\nSend **ID & Password** in this manner otherwise the bot will not respond.\n\nSend like this:- **ID*Password**")
        input_str, message = await app.listen(editable.chat.id)
        info = {"email": "", "password": ""}
        info["email"] = input_str.split("*")[0]
        info["password"] = input_str.split("*")[1]

        scraper = cloudscraper.create_scraper()
        res = scraper.post(rw_url, data=info, headers=hdr).content
        output = json.loads(res)
        print(output)
        userid = output["data"]["userid"]
        token = output["data"]["token"]
        print(f"userid: {userid}, token: {token}")

        hdr1 = {
            "Host": "rgvikramjeetapi.classx.co.in",
            "Client-Service": "Appx",
            "Auth-Key": "appxapi",
            "User-Id": userid,
            "Authorization": token
        }
        print("**login Successful**")
        cour_url = "https://rgvikramjeetapi.classx.co.in/get/mycourse?userid="
        res1 = scraper.get("https://rgvikramjeetapi.classx.co.in/get/mycourse?userid="+userid, headers=hdr1)
        b_data = res1.json()['data']
        cool = ""
        for data in b_data:
            t_name = data['course_name']
            FFF = "**BATCH-ID - BATCH NAME - INSTRUCTOR**"
            aa = f" ```{data['id']}```  - **{data['course_name']}**\n\n"
            if len(f'{cool}{aa}') > 4096:
                print(aa)
                cool = ""
            cool += aa
        print(f'{"**You have these batches :-**"}\n\n{FFF}\n\n{cool}')

        editable = await message.reply_text("\nNow send the Batch ID to Download")
        input1_str, message = await app.listen(editable.chat.id)
        raw_text1 = input1_str
        scraper2 = cloudscraper.create_scraper()  # Use a different variable name for the second scraper instance
        html = scraper2.get("https://rgvikramjeetapi.classx.co.in/get/course_by_id?id=" + raw_text1, headers=hdr1).json()
        course_title = html["data"][0]["course_name"]
        html = scraper2.get("https://rgvikramjeetapi.classx.co.in/get/allsubjectfrmlivecourseclass?courseid=" + raw_text1, headers=hdr1).content
        output0 = json.loads(html)
        subjID = output0["data"]
        cool = ""
        vj = ""
        for sub in subjID:
            subjid = sub["subjectid"]
            idid = f"{subjid}&"
            subjname = sub["subject_name"]
            aa = f" ```{subjid}```  -  **{subjname}**\n\n"
            #cool1 += aa
            #vj += idid
        print(f'{"**You have these batches :-**"}\n\n{subjid}\n\n{subjname}')
        editable = await message.reply_text(f"Now send the **Topic IDs** to Download\n\nSend like this **1&2&3&4** so on\nor copy-paste or edit **below ids** according to you :\n\n**Enter this to download the full batch :-**\n```{vj}```")
        input2_str, message = await app.listen(editable.chat.id)
        raw_text2 = input2_str

        output_dict = {}
        videos_dict = {}
        mm = "Rgvikramjeet"
        xv = raw_text2.split('&')
        for y in range(0, len(xv)):
            raw_text2 = xv[y]
            res2 = requests.get("https://rgvikramjeetapi.classx.co.in/get/alltopicfrmlivecourseclass?courseid=" + raw_text1, "&subjectid=" + raw_text2, headers=hdr1)
            b_data2 = res2.json()['data']
            for data in b_data2:
                t_name = (data["topic_name"])
                tid = (data["topicid"])
                hdr11 = {
                    "Host": "rgvikramjeetapi.classx.co.in",
                    "Client-Service": "Appx",
                    "Auth-Key": "appxapi",
                    "User-Id": userid,
                    "Authorization": token
                }
                par = {
                    'courseid': raw_text1, 'subjectid': raw_text2, 'topicid': tid, 'start': '-1'
                }
                res3 = requests.get('https://rgvikramjeetapi.classx.co.in/get/allconceptfrmlivecourseclass', params=par, headers=hdr11).json()
                b_data3 = res3['data']
                for data in b_data3:
                    cid = (data["conceptid"])
                    par2 = {
                        'courseid': raw_text1, 'subjectid': raw_text2, 'topicid': tid, 'conceptid': cid, 'start': '-1'
                    }
                    res4 = requests.get('https://rgvikramjeetapi.classx.co.in/get/livecourseclassbycoursesubtopconceptapiv3', params=par2, headers=hdr11).json()
                    try:
                        topicid = res4["data"]
                        for data in topicid:
                            tn = (data["download_link"])
                            tid = (data["Title"])
                            url = decode(tn)
                            videos_dict[tid] = url
                            mtext = f"{tid}:{url}\n"
                            open(f"{mm} - {course_title}.txt", "a", encoding="utf-8").write(mtext)
                        output_dict[t_name] = videos_dict
                    except requests.exceptions.RequestException as e:
                        await message.reply_text(f"An error occurred during the request: {e}")

    except requests.exceptions.RequestException as e:
        await message.reply_text(f"An error occurred during the request: {e}")


@app.on_message(filters.command("gentxt"))
async def filegen(_,message):
    txt = await gentxt(_,message)
    print(txt)
    
