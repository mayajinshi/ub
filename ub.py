import os
import time
import asyncio
import random
import logging
from threading import Thread
from flask import Flask
from telethon import TelegramClient, events
from telethon.sessions import StringSession
from telethon import events
from telethon.tl.functions.users import GetFullUserRequest
import re
# ================== KEEP ALIVE ================== #

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

# ================== LOGGING ================== #

logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s - %(message)s'
)

# ================== TELEGRAM CONFIG ================== #

api_id = 32135350
api_hash = "7c9832d6ef116e3d75ac843dbc1bbbad"
session = "1BVtsOIMBuzIfQb4ZqhUsR2N_sDI29Rjskwc3A88q87wUjhXq5YGDqYakC6OKEUdocAMClrgQw6yN4-Sz2XrVFNidsLa65UHSdRzeK9_3gkzE9zdUU58ovmUEFlcKQ_qnYu5m0njGMv6ccCIzNpse8nfsBiNw-1sE1I5xm_6Q6iXraLXG8Z0rMsQPBwtW9f2-YJxV6gzNEGQxY4Q1zEUTfT0dd9OsW8nimhEYKm81-1DnvTb1B6jh_VnN-ZCZ9pJWThY_oAJNCvV8Znls4bDQEv1daDiKTe99_iH1gClzY-vOlDOUkoPRR_3HdJ8rDMHaLJPLb-GV3HXZQCV5b8243NmC9STM3hY="

client = TelegramClient(StringSession(session), api_id, api_hash)

TARGET_GROUP_ID = -1003623091628
start_time = time.time()

# ================== AUTO TYPING ================== #

async def fake_typing():
    while True:
        try:
            async with client.action(TARGET_GROUP_ID, 'typing'):
                await asyncio.sleep(random.randint(6, 12))
        except Exception as e:
            logging.error(f"Typing error: {e}")
            await asyncio.sleep(10)

# ================== PRIVATE AUTO REPLY ================== #

GREETING_TEXT = '''🐣🦋 𝗦𝗘𝗥𝗩𝗜𝗖𝗘 𝗔𝗩𝗔𝗜𝗟𝗔𝗕𝗟𝗘 🐣🦋

🍒 𝗩𝗢𝗜𝗖𝗘 𝗖𝗔𝗟𝗟
5 MIN - 200 RS
10 MIN - 350 RS

🎀 𝗩𝗜𝗗𝗘𝗢 𝗖𝗔𝗟𝗟
5 MIN - 500 RS
10 MIN - 800 RS

🌟 𝗦𝗘𝗫 𝗖𝗛𝗔𝗧
5 MIN - 200 RS
10 MIN - 350 RS

💟 DEMO - 100 RS'''

@client.on(events.NewMessage(incoming=True))
async def private_auto_reply(event):
    try:
        if event.is_private and not event.out:
            text = event.raw_text.lower()
            if text in ["hi", "hello", "hey", "hii", "hy", "hyy"]:
                async with client.action(event.chat_id, 'typing'):
                    await asyncio.sleep(random.randint(2, 4))
                await event.reply(GREETING_TEXT)
    except Exception as e:
        logging.error(f"Auto reply error: {e}")

# ================== AUTO DELETE ================== #

@client.on(events.NewMessage(incoming=True))
async def auto_delete_group(event):
    if event.is_group:
        await asyncio.sleep(120)
        try:
            await event.delete()
        except:
            pass

# ================== BASIC COMMANDS ================== #



# Patterns to detect usernames/links in bio
BIO_PATTERNS = [
    r'@\w+',
    r'http[s]?://',
    r't\.me/',
    r'telegram\.me/',
    r'www\.'
]

@client.on(events.NewMessage())
async def bio_link_filter(event):
    try:
        sender = await event.get_sender()
        full = await client(GetFullUserRequest(sender.id))
        bio = full.full_user.about or ""

        # Check if bio contains username or link
        if any(re.search(pattern, bio, re.IGNORECASE) for pattern in BIO_PATTERNS):
            await event.delete()
            print(f"Deleted message from {sender.id} بسبب bio link/username")

    except Exception as e:
        print("Error:", e)
        

@client.on(events.NewMessage(outgoing=True, pattern=r"\.alive"))
async def alive(event):
    await event.edit("I'm alive my queen.. ❤️")

@client.on(events.NewMessage(outgoing=True, pattern=r"\.ping"))
async def ping(event):
    start = time.time()
    msg = await event.edit("Pinging...")
    end = time.time()
    ms = round((end - start) * 1000, 2)
    await msg.edit(f"🏓 Pong: {ms} ms")

@client.on(events.NewMessage(outgoing=True, pattern=r"\.uptime"))
async def uptime(event):
    seconds = int(time.time() - start_time)
    hrs = seconds // 3600
    mins = (seconds % 3600) // 60
    secs = seconds % 60
    await event.edit(f"⏳ Uptime: {hrs}h {mins}m {secs}s")

@client.on(events.NewMessage(outgoing=True, pattern=r"\.boost"))
async def boost(event):
    await event.edit("𝘽𝙊𝙊𝙎𝙏 𝙏𝙃𝙄𝙎 𝙂𝙍𝙊𝙐𝙋 💋\nt.me/wife_swapping_gf?boost ❤️")

@client.on(events.NewMessage(outgoing=True, pattern=r"\.boostshiv"))
async def boostshiv(event):
    await event.edit("𝘽𝙊𝙊𝙎𝙏 𝙏𝙃𝙄𝙎 𝘾𝙃𝘼𝙉𝙉𝙀𝙇 💋\nt.me/thnxshiv?boost ❤️")

# ================== FUN COMMANDS ================== #

@client.on(events.NewMessage(pattern=r"\.love"))
async def love(event):
    frames = ["🤍", "💛", "🧡", "❤️", "💖", "💞", "💕", "💘 I Love You 💘"]
    for f in frames:
        await event.edit(f)
        await asyncio.sleep(0.5)

@client.on(events.NewMessage(pattern=r"\.hack"))
async def hack(event):
    steps = [
        "Initializing hack...",
        "Connecting...",
        "Bypassing firewall...",
        "Injecting payload...",
        "Access Granted!",
        "💀 Target hacked!"
    ]
    for s in steps:
        await event.edit(s)
        await asyncio.sleep(1)

@client.on(events.NewMessage(pattern=r"\.type (.+)"))
async def type_cmd(event):
    text = event.pattern_match.group(1)
    await event.edit("")
    current = ""
    for char in text:
        current += char
        await event.edit(current)
        await asyncio.sleep(0.08)

@client.on(events.NewMessage(pattern=r"\.spam (\d+) (.+)"))
async def spam(event):
    count = int(event.pattern_match.group(1))
    text = event.pattern_match.group(2)

    if count > 20:
        return await event.edit("Spam limit is 20.")

    await event.delete()

    for _ in range(count):
        await event.respond(text)
        await asyncio.sleep(0.3)

# ================== QR PAYMENT ================== #

@client.on(events.NewMessage(outgoing=True, pattern=r"\.pay"))
async def pay(event):
    await client.send_file(
        event.chat_id,
        "qr.jpg",
        caption="scan and pay karo"
    )
    await event.delete()

# ================== HELP MENU ================== #

@client.on(events.NewMessage(outgoing=True, pattern=r"\.help"))
async def help_menu(event):
    await event.edit("""
⚡ USERBOT COMMANDS ⚡

.alive
.ping
.uptime
.boost
.boostshiv
.love
.hack
.type text
.spam count text
.pay
.help
""")

# ================== MAIN ================== #

async def main():
    await client.start()
    logging.info("Userbot running...")
    client.loop.create_task(fake_typing())
    await client.run_until_disconnected()

keep_alive()

with client:
    client.loop.run_until_complete(main())
