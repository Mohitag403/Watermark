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

# Constants
API_URL = "https://neetkakajeeapi.classx.co.in/"
AUTH_KEY = "appxapi"
ENCRYPTION_KEY = "638udh3829162018"
IV = "fedcba9876543210"

async def decrypt_data(encoded_data, key, iv):
    decoded_data = b64decode(encoded_data)
    cipher = AES.new(key.encode("utf8"), AES.MODE_CBC, iv.encode("utf8"))
    decrypted_data = unpad(cipher.decrypt(decoded_data), AES.block_size)
    return decrypted_data.decode('utf-8')

async def send_message_and_listen(message, text):
    editable = await message.reply_text(text)
    input_msg = await app.listen(editable.chat.id)
    raw_text = input_msg.text
    await input_msg.delete(True)
    return raw_text, editable

@app.on_message(filters.command(["nkj"]) & filters.user(SUDO_USERS))
async def neetkaka_login(_, message):
    try:
        # Step 1: User Login
        raw_text, editable = await send_message_and_listen(message, "Send ID & Password like this: ID*Password")
        info = {"email": raw_text.split("*")[0], "password": raw_text.split("*")[1]}
        scraper = cloudscraper.create_scraper()
        res = scraper.post(API_URL + "post/userLogin", data=info, headers=get_headers()).content
        output = json.loads(res)
        userid, token = output["data"]["userid"], output["data"]["token"]

        # Step 2: Get Batches
        await editable.edit("**Login Successful**")
        hdr1 = get_headers(userid, token)
        res1 = requests.get(API_URL + f"get/mycourseweb?userid={userid}", headers=hdr1)
        b_data = res1.json()['data']
        batch_details = get_batch_details(b_data)
        await editable.edit(f'{"**You have these batches :-"}\n\n{batch_details}')

        # Step 3: Get Subject IDs
        batch_id, editable = await send_message_and_listen(message, "**Now send the Batch ID to Download**")
        subjID_data = get_subject_ids(batch_id, hdr1)
        await editable.edit(subjID_data)

        # Step 4: Get Topic IDs
        subj_id, editable = await send_message_and_listen(message, "**Enter the Subject Id shown above**")
        topic_data = get_topic_data(batch_id, subj_id, hdr1)
        await editable.edit(topic_data)

        # Step 5: Download Topics
        topic_ids, editable = await send_message_and_listen(message, "**Now send the Topic IDs to Download**\n"
                                                                     "Send like this 1&2&3&4 or copy-paste/edit below IDs")
        resolution, editable = await send_message_and_listen(message, "**Now send the Resolution**")
        download_topics(userid, token, batch_id, subj_id, topic_ids, resolution)

        await message.reply_text("Done")

    except Exception as e:
        await message.reply_text(f"An error occurred: {str(e)}")

# Helper functions

async def get_headers(userid=None, token=None):
    return {
        "Host": "neetkakajeeapi.classx.co.in",
        "Client-Service": "Appx",
        "Auth-Key": AUTH_KEY,
        "User-Id": userid,
        "Authorization": token
    }

async def get_batch_details(b_data):
    cool = ""
    FFF = "BATCH-ID - BATCH NAME - INSTRUCTOR"
    for data in b_data:
        aa = f"**`{data['id']}`      - `{data['course_name']}`**\n\n"
        if len(f'{cool}{aa}') > 4096:
            cool = ""
        cool += aa
    return f'{"**You have these batches :-"}\n\n{FFF}\n\n{cool}'

async def get_subject_ids(batch_id, hdr1):
    res = requests.get(API_URL + f"get/allsubjectfrmlivecourseclass?courseid={batch_id}", headers=hdr1).content
    output0 = json.loads(res)
    subjID = output0["data"]
    cool = ""
    for sub in subjID:
        subjid, subjname = sub["subjectid"], sub["subject_name"]
        aa = f"`{subjid}` - `{subjname}`\n\n"
        cool += aa
    return cool

async def get_topic_data(batch_id, subj_id, hdr1):
    res = requests.get(API_URL + f"get/alltopicfrmlivecourseclass?courseid={batch_id}&subjectid={subj_id}", headers=hdr1)
    b_data2 = res.json()['data']
    lol = ""
    BBB = f"{'**TOPIC-ID    - TOPIC     - VIDEOS**'}\n"
    for data in b_data2:
        t_name, tid = data["topic_name"], data["topicid"]
        zz = len(tid)
        hh = f'`{tid}`     - **{t_name} - ({zz})**\n'
        lol += hh
    return f"Batch details of **{t_name}** are:\n\n{BBB}\n\n{lol}"

async def download_topics(userid, token, batch_id, subj_id, topic_ids, resolution):
    try:
        xv = topic_ids.split('&')
        for t in xv:
            hdr11 = get_headers(userid, token)
            res = requests.get(API_URL + f"get/livecourseclassbycoursesubtopconceptapiv3?topicid={t}&start=-1&courseid={batch_id}&subjectid={subj_id}", headers=hdr11).json()
            topicid = res["data"]

            for data in topicid:
                tids, plinks = data["Title"], [data["pdf_link"]]
                vs = await decrypt_data(plinks[0].split(':')[0], ENCRYPTION_KEY, IV)

                dlinks = [link['path'] for link in data['download_links'] if link['quality'] == f"{resolution}p"]
                cool2 = await decrypt_data(dlinks[0].split(':')[0], ENCRYPTION_KEY, IV)

                mm = "NEET Kaka JEE"
                with open(f'{mm}.txt', 'a') as f:
                    f.write(f"{tids} : {cool2}\n {vs}")
                await app.send_document(int(message.chat.id), f"{mm}.txt")
                file_path = f"{mm}.txt"
                os.remove(file_path)
    except Exception as e:
        await message.reply_text(str(e))
