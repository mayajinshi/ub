import os
import asyncio
import random
import time
from datetime import datetime
from threading import Thread
from flask import Flask

from telethon import TelegramClient, events
from telethon.sessions import StringSession
from telethon.tl.functions.contacts import BlockRequest, UnblockRequest
from openai import OpenAI

from telethon.tl.types import MessageEntityMentionName


# ---------------- KEEP ALIVE ---------------- #

app = Flask('')

@app.route('/')
def home():
    return "adubot is alive"

def run():
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run)
    t.start()

# ---------------- TELEGRAM LOGIN ---------------- #

api_id = 20900277
api_hash = "6a3d761f9be590be4259404f34a1f81e"
session = "1BVtsOIMBu7Q_vOVo2DYgBWAwR2eSAgKw-nNjkbHOcQPAMmd1uzcmKZJkMGbd91Tggo65p9uvTsqdXnWg7jru1hUSYEBQx7JEGGT702FBTvupvSVjsXZRqA5vimYDGxcnYIsckWMSq4cwWU3c03aS_H9ijWO-qha2aEh3t6XH65APZcLiw6lADeyW73YYyEJU7BKSsMaBNd7s1lVHMFcV3kM_KjqoFEd8Lda2BVmchxDHleETTiEg6_A2Xe9o9aWium8FHikm5q9EcvYwQcjH_Psf1X9_aOPVqfO4Dwb0FWjiX89PzoKtkQS2Ujm_DwxM31nTPRpOWQURGL4CEI4ZrvhW1pkTjag="

client = TelegramClient(StringSession(session), api_id, api_hash)

# ---------------- SETTINGS ---------------- #

TARGET_GROUP_ID = -1003623091628
replied_users = set()
start_time = time.time()

# ---------------- 24x7 TYPING PRANK ---------------- #

async def fake_typing():
    while True:
        try:
            async with client.action(TARGET_GROUP_ID, 'typing'):
                await asyncio.sleep(random.randint(6, 12))
        except Exception as e:
            print("Typing Error:", e)
            await asyncio.sleep(15)

# ---------------- AUTO WELCOME ---------------- 

@client.on(events.NewMessage(outgoing=True, pattern=r"\.all"))
async def mention_all(event):
    chat = await event.get_chat()
    users = []

    async for user in client.iter_participants(chat):
        if not user.bot:
            users.append(f"[{user.first_name}](tg://user?id={user.id})")

    message = ""
    for user in users:
        if len(message) + len(user) + 1 > 4000:
            await event.respond(message, parse_mode="md")
            message = ""
        message += user + " "

    if message:
        await event.respond(message, parse_mode="md")

    await event.delete()
    
# ---------------- AUTO PRICE ---------------- #

@client.on(events.NewMessage(incoming=True))
async def auto_price(event):
    if event.is_private and not event.out:
        user_id = event.sender_id

        if user_id not in replied_users:
            replied_users.add(user_id)
            await asyncio.sleep(2)

            await event.respond(""" Hi Babe! Are you here for paid cam show or normal chat?

            Please leave your reply and wait for my response.
""")
# ----------


PRICE_TEXT = """
Scan the QR or Tap on the link to pay.

     tinyurl.com/gfnavya 

Send screenshot after payment.
"""

QR_IMAGE = "qr.jpg"  

@client.on(events.NewMessage(outgoing=True, pattern=r"\.qr"))
async def send_price_list(event):
    await client.send_file(
        event.chat_id,
        QR_IMAGE,
        caption=PRICE_TEXT
    )
    await event.delete()

#------

@client.on(events.NewMessage(outgoing=True, pattern=r"\.fl"))
async def price_list(event):
    text = """
    🐣🦋 𝗡𝗔𝗩𝗬𝗔 𝗔𝗩𝗔𝗜𝗟𝗔𝗕𝗟𝗘 🐣🦋

       🍒  𝗩𝗢𝗜𝗖𝗘 𝗖𝗔𝗟𝗟  🍒

🍒𝟱 𝗠𝗜𝗡𝗨𝗧𝗘𝗦 - 100 𝗥𝗦 💦
🍒𝟭𝟬 𝗠𝗜𝗡𝗨𝗧𝗘𝗦 - 250 𝗥𝗦 💦

       🎀 𝗩𝗜𝗗𝗘𝗢 𝗖𝗔𝗟𝗟 💘

🍒𝟱 𝗠𝗜𝗡𝗨𝗧𝗘𝗦 - 3𝟬𝟬 𝗥𝗦  💦
🍒𝟭𝟬 𝗠𝗜𝗡𝗨𝗧𝗘𝗦 - 6𝟬𝟬 𝗥𝗦 💦

       🌟 𝗦𝗘𝗫 𝗖𝗛𝗔𝗧 👄

🍒𝟱 𝗠𝗜𝗡𝗨𝗧𝗘𝗦 - 1𝟬𝟬 𝗥𝗦 💦
🍒𝟭𝟬 𝗠𝗜𝗡𝗨𝗧𝗘𝗦 - 200 𝗥𝗦 💦

       🎀 𝗦𝗣𝗘𝗖𝗜𝗔𝗟 𝗦𝗛𝗢𝗪 💘

🍒 𝗦𝗔𝗥𝗘𝗘 𝗦𝗛𝗢𝗪 - 𝟭𝟮𝟬𝟬 𝗥𝗦 💦
🍒 𝗦𝗤𝗨𝗜𝗥𝗧 𝗦𝗛𝗢𝗪 - 𝟭𝟭𝟬𝟬 𝗥𝗦 💦

💟𝗗𝗘𝗠𝗢 - 𝟭𝟬𝟬 𝗥𝗦💟
"""
    await event.edit(text)
    

@client.on(events.ChatAction(chats=TARGET_GROUP_ID))
async def welcome_new_user(event):
    if event.users:
        users = await event.get_users()

        for user in users:
            await asyncio.sleep(2)

            message = f" {user.first_name} DM ME FOR FUN BABY 💋"

            entity = MessageEntityMentionName(
                offset=8,
                length=len(user.first_name),
                user_id=user.id
            )

            await client.send_message(
                GROUP_ID,
                message,
                formatting_entities=[entity]
            )
#-----

@client.on(events.NewMessage(outgoing=True, pattern=r"\.dm"))
async def price_list(event):
    text = """
DM @niximia to buy Telegram/WhatsApp accounts.
"""
    await event.edit(text)


@client.on(events.NewMessage(outgoing=True, pattern=r"\.rl"))
async def price_list(event):
    text = """
    🐣🦋 𝗡𝗔𝗩𝗬𝗔 𝗔𝗩𝗔𝗜𝗟𝗔𝗕𝗟𝗘 🐣🦋

       🍒  𝗩𝗢𝗜𝗖𝗘 𝗖𝗔𝗟𝗟  🍒

🍒𝟱 𝗠𝗜𝗡𝗨𝗧𝗘𝗦 - 𝟮𝟬𝟬 𝗥𝗦 💦
🍒𝟭𝟬 𝗠𝗜𝗡𝗨𝗧𝗘𝗦 - 𝟯𝟱𝟬 𝗥𝗦 💦

       🎀 𝗩𝗜𝗗𝗘𝗢 𝗖𝗔𝗟𝗟 💘

🍒𝟱 𝗠𝗜𝗡𝗨𝗧𝗘𝗦 - 𝟱𝟬𝟬 𝗥𝗦  💦
🍒𝟭𝟬 𝗠𝗜𝗡𝗨𝗧𝗘𝗦 - 𝟴𝟬𝟬 𝗥𝗦 💦

       🌟 𝗦𝗘𝗫 𝗖𝗛𝗔𝗧 👄

🍒𝟱 𝗠𝗜𝗡𝗨𝗧𝗘𝗦 - 𝟮𝟬𝟬 𝗥𝗦 💦
🍒𝟭𝟬 𝗠𝗜𝗡𝗨𝗧𝗘𝗦 - 𝟯𝟱𝟬 𝗥𝗦 💦

       🎀 𝗦𝗣𝗘𝗖𝗜𝗔𝗟 𝗦𝗛𝗢𝗪 💘

🍒 𝗦𝗔𝗥𝗘𝗘 𝗦𝗛𝗢𝗪 - 𝟭𝟮𝟬𝟬 𝗥𝗦 💦
🍒 𝗦𝗤𝗨𝗜𝗥𝗧 𝗦𝗛𝗢𝗪 - 𝟭𝟭𝟬𝟬 𝗥𝗦 💦

💟𝗗𝗘𝗠𝗢 - 𝟭𝟬𝟬 𝗥𝗦💟
"""
    await event.edit(text)



PROOF_LINK = "@proofsxnavya"

@client.on(events.NewMessage(incoming=True))
async def auto_proof_reply(event):
    if event.is_private:
        msg = event.raw_text.lower()

        proof_keywords = ["proof", "send proof", "proof?"]

        if any(word in msg for word in proof_keywords):
            await event.reply(f"Here is the proof:\n{PROOF_LINK}")


#-------
@client.on(events.NewMessage(outgoing=True, pattern=r"\.alive"))
async def alive(event):
    uptime = int(time.time() - start_time)
    await event.edit(f"💋 BaZiGaR mAiN bAzIgAr!\nUptime: {uptime} sec")

@client.on(events.NewMessage(outgoing=True, pattern=r"\.spam"))
async def spam(event):
    args = event.raw_text.split(maxsplit=2)
    count = int(args[1])
    text = args[2]

    await event.delete()
    for _ in range(count):
        await client.send_message(event.chat_id, text)

# ---------------- MAIN ---------------- #

async def main():
    await client.start()
    print("Userbot running...")

    client.loop.create_task(fake_typing())

    await client.run_until_disconnected()

keep_alive()

with client:
    client.loop.run_until_complete(main())
