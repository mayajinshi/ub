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
from telethon.tl.types import MessageEntityMentionName

# ---------------- WEB SERVER ---------------- #

app = Flask(__name__)

@app.route('/')
def home():
    return "adubot is alive"

def run_web():
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    Thread(target=run_web).start()

# ---------------- TELEGRAM CONFIG ---------------- #

api_id = 32135350
api_hash = '7c9832d6ef116e3d75ac843dbc1bbbad'
session = "1BVtsOIMBuzIfQb4ZqhUsR2N_sDI29Rjskwc3A88q87wUjhXq5YGDqYakC6OKEUdocAMClrgQw6yN4-Sz2XrVFNidsLa65UHSdRzeK9_3gkzE9zdUU58ovmUEFlcKQ_qnYu5m0njGMv6ccCIzNpse8nfsBiNw-1sE1I5xm_6Q6iXraLXG8Z0rMsQPBwtW9f2-YJxV6gzNEGQxY4Q1zEUTfT0dd9OsW8nimhEYKm81-1DnvTb1B6jh_VnN-ZCZ9pJWThY_oAJNCvV8Znls4bDQEv1daDiKTe99_iH1gClzY-vOlDOUkoPRR_3HdJ8rDMHaLJPLb-GV3HXZQCV5b8243NmC9STM3hY="

client = TelegramClient(StringSession(session), api_id, api_hash)

TARGET_GROUP_ID = -1003623091628
GROUP_LINK = "@WIFE_SWAPPING_GF"

replied_users = set()
start_time = time.time()

quotes = ["Hi", "Hii", "Addd Mee", "Heloo", "Nice"]

# ---------------- BACKGROUND TASKS ---------------- #

async def fake_typing():
    while True:
        try:
            async with client.action(TARGET_GROUP_ID, 'typing'):
                await asyncio.sleep(random.randint(6, 12))
        except Exception as e:
            print("Typing Error:", e)
            await asyncio.sleep(15)

async def send_quotes():
    while True:
        dialogs = await client.get_dialogs()
        for dialog in dialogs:
            if dialog.is_group:
                try:
                    await client.send_message(dialog.id, random.choice(quotes))
                    await asyncio.sleep(7)
                except Exception:
                    pass
        await asyncio.sleep(300)

# ---------------- PRIVATE AUTO REPLY ---------------- #

@client.on(events.NewMessage(incoming=True))
async def private_auto_reply(event):
    if event.is_private and not event.out:
        user_id = event.sender_id
        msg = event.raw_text.lower()

        # first auto reply
        if user_id not in replied_users:
            replied_users.add(user_id)

            await asyncio.sleep(2)

            await event.respond(
                f"🌸 NAVYA AVAILABLE 🌸\n\n"
                f"Please join our group:\n{GROUP_LINK}\n\n"
                f"After joining, message me again 💋"
            )

# ---------------- KEYWORD REPLY ---------------- #

@client.on(events.NewMessage(incoming=True, pattern=r'(?i)^demo$'))
async def demo_reply(event):
    if event.is_private:
        await event.reply("demo paid hai babe.. 100rs only")

# ---------------- GROUP WELCOME ---------------- #

@client.on(events.ChatAction(chats=TARGET_GROUP_ID))
async def welcome_new_user(event):
    if event.user_joined or event.user_added:
        users = await event.get_users()

        for user in users:
            name = user.first_name or "User"
            message = f"Hello {name}, DM ME FOR FUN BABY 💋"

            entity = MessageEntityMentionName(
                offset=6,
                length=len(name),
                user_id=user.id
            )

            await client.send_message(
                TARGET_GROUP_ID,
                message,
                formatting_entities=[entity]
            )

# ---------------- COMMANDS ---------------- #

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
    await event.edit(f"CURRENT TIME: {now}")

@client.on(events.NewMessage(outgoing=True, pattern=r"\.alive"))
async def alive(event):
    uptime = int(time.time() - start_time)
    await event.edit(f"⚡ Alive\nUptime: {uptime} sec")

@client.on(events.NewMessage(outgoing=True, pattern=r"\.block"))
async def block_user(event):
    if event.is_private:
        await client(BlockRequest(event.chat_id))
        await event.edit("Blocked.")

@client.on(events.NewMessage(outgoing=True, pattern=r"\.unblock"))
async def unblock_user(event):
    if event.is_private:
        await client(UnblockRequest(event.chat_id))
        await event.edit("Unblocked.")

@client.on(events.NewMessage(outgoing=True, pattern=r"\.spam"))
async def spam(event):
    args = event.raw_text.split(maxsplit=2)
    if len(args) < 3:
        return await event.edit("Usage: .spam count text")

    count = int(args[1])
    text = args[2]

    await event.delete()

    for _ in range(count):
        await client.send_message(event.chat_id, text)

@client.on(events.NewMessage(outgoing=True, pattern=r"\.rl"))
async def price_list(event):
    text = """
🌸 NAVYA AVAILABLE 🌸
💬 SEX CHAT
• 10 min → ₹350
• 20 min → ₹740

📞 VOICE CALL
• 5 min → ₹220
• 10 min → ₹450

🎥 VIDEO CALL
• 5 min → ₹500
• 10 min → ₹990

Send payment screenshot after payment.
"""
    await event.edit(text)

@client.on(events.NewMessage(chats=TARGET_GROUP_ID))
async def auto_delete_group_messages(event):
    try:
        await asyncio.sleep(120)
        await event.delete()
    except Exception as e:
        print("Auto-delete error:", e)
        
# ---------------- MAIN ---------------- #

async def main():
    await client.start()
    print("Userbot running...")

    asyncio.create_task(fake_typing())
    asyncio.create_task(send_quotes())

    await client.run_until_disconnected()

keep_alive()
asyncio.run(main())
