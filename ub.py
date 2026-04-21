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

client_ai = OpenAI(api_key="YOUR_OPENAI_KEY")

# ---------------- 24x7 TYPING PRANK ---------------- #

async def fake_typing():
    while True:
        try:
            async with client.action(TARGET_GROUP_ID, 'typing'):
                await asyncio.sleep(random.randint(6, 12))
        except Exception as e:
            print("Typing Error:", e)
            await asyncio.sleep(15)

# ---------------- BLOCK / UNBLOCK ---------------- #

@client.on(events.NewMessage(outgoing=True, pattern=r"\.block"))
async def block_user(event):
    if event.is_private:
        entity = await client.get_entity(event.chat_id)
        await client(BlockRequest(entity))
        await event.edit("Blocked.")

@client.on(events.NewMessage(outgoing=True, pattern=r"\.unblock"))
async def unblock_user(event):
    if event.is_private:
        await client(UnblockRequest(event.chat_id))
        await event.edit("User unblocked.")

# ---------------- AUTO WELCOME ---------------- #

@client.on(events.ChatAction())
async def welcome_new_member(event):
    if event.chat_id == TARGET_GROUP_ID:
        if event.user_joined or event.user_added or event.user_approved:
            user = await event.get_user()
            await client.send_message(
                TARGET_GROUP_ID,
                f"{user.first_name} ❤️\n𝗠𝗘𝗦𝗦𝗔𝗚𝗘 𝗠𝗘 𝗙𝗢𝗥 𝗙𝗨𝗡. 𝗠𝗨𝗔𝗔𝗔𝗛𝗛 💋"
            )

# ---------------- AUTO PRICE ---------------- #

@client.on(events.NewMessage(incoming=True))
async def auto_price(event):
    if event.is_private and not event.out:
        user_id = event.sender_id

        if user_id not in replied_users:
            replied_users.add(user_id)
            await asyncio.sleep(2)

            await event.respond("""🌸 NAVYA AVAILABLE 🌸
✅ 100% Trusted & Verified Model
━━━━━━━━━━━━━━━
💬 SEX CHAT
• 10 Minutes → ₹350
• 20 Minutes → ₹740
━━━━━━━━━━━━━━━
📞 VOICE CALL
• 5 Minutes → ₹220
• 10 Minutes → ₹450
• 18 Minutes → ₹890
━━━━━━━━━━━━━━━
🎥 VIDEO CALL
• 5 Minutes → ₹500
• 10 Minutes → ₹990
• 20 Minutes → ₹1900
""")


# ---------------- UTIL COMMANDS ---------------- #

@client.on(events.NewMessage(outgoing=True, pattern=r"\.ping"))
async def ping(event):
    start = time.time()
    msg = await event.edit("Pinging...")
    end = time.time()
    await msg.edit(f"PONG! {round((end-start)*1000)} ms")

@client.on(events.NewMessage(outgoing=True, pattern=r"\.id"))
async def get_id(event):
    await event.edit(f"CHAT ID: `{event.chat_id}`")

@client.on(events.NewMessage(outgoing=True, pattern=r"\.time"))
async def time_cmd(event):
    now = datetime.now().strftime("%H:%M:%S")
    await event.edit(f"TIME: {now}")

@client.on(events.NewMessage(outgoing=True, pattern=r"\.alive"))
async def alive(event):
    uptime = int(time.time() - start_time)
    await event.edit(f"⚡ Alive\nUptime: {uptime} sec")

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
