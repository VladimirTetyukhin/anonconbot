import asyncio
from pyrogram import Client, filters, idle
from pyrogram.handlers import MessageHandler
from config import CHANNEL_CHATBOT_ID
from config import BOT_OWNER, api_id, api_hash
from create_bot import apps

async def other_owner(client_api_id):
    return BOT_OWNER[client_api_id == api_id[0]]

async def send_text(client, message):
    if (message.text.startswith("You stopped the dialog 🙄") or
            message.text.startswith("Your partner has stopped the") or
            message.text.startswith("Type /search to find")):
        await client.send_message(
            chat_id=message.chat.id,
            text="/next"
        )
        await client.send_message(
            chat_id=await other_owner(client.api_id),
            text="/next"
        )
        return

    if message.text.startswith("🤖 Собеседник"):
        await client.send_message(
            chat_id=await other_owner(client.api_id),
            text="@{}".format(message.entities[0].user.username)
        )
        return

    if (message.text.startswith("If you wish, leave your") or
            message.text.startswith("Looking for a partner") or
            message.text.startswith("Partner found 🐵") or
            message.text.startswith("You stopped the dialog. Searching") or
            message.text.startswith("You are in the dialog right now") or
            message.text.startswith("Choose a reason for report")):
        return
    
    await client.copy_message(
        chat_id=await other_owner(client.api_id),
        from_chat_id=message.chat.id,
        message_id=message.id
    )

async def send_all_except_text_and_media_group(client, message):
    if message.photo and message.caption and message.caption.startswith("🤖 Чтобы"):
        return
    await client.copy_message(
        chat_id=await other_owner(client.api_id),
        from_chat_id=message.chat.id,
        message_id=message.id
    )

async def send_media_group(client, message):
    await client.copy_media_group(
        chat_id=await other_owner(client.api_id),
        from_chat_id=message.chat.id,
        message_id=message.id
    )

async def copy_media_group(client, message):
    await client.copy_media_group(
        chat_id=CHANNEL_CHATBOT_ID,
        from_chat_id=message.chat.id,
        message_id=message.id
    )

async def copy_all_except_media_group(client, message):
    await client.copy_message(
        chat_id=CHANNEL_CHATBOT_ID,
        from_chat_id=message.chat.id,
        message_id=message.id
    )



def register_handlers_chatbot(app: Client):
    app.add_handler(MessageHandler(send_text, (filters.user(CHANNEL_CHATBOT_ID) & filters.chat(CHANNEL_CHATBOT_ID)) & filters.text))
    app.add_handler(MessageHandler(send_all_except_text_and_media_group, (filters.user(CHANNEL_CHATBOT_ID) & filters.chat(CHANNEL_CHATBOT_ID)) & ~filters.text & ~filters.media_group))
    app.add_handler(MessageHandler(send_media_group, (filters.user(CHANNEL_CHATBOT_ID) & filters.chat(CHANNEL_CHATBOT_ID)) & filters.media_group))
    app.add_handler(MessageHandler(copy_media_group, (filters.user(BOT_OWNER[0]) & filters.chat(BOT_OWNER[0]) | filters.user(BOT_OWNER[1]) & filters.chat(BOT_OWNER[1])) & filters.media_group))
    app.add_handler(MessageHandler(copy_all_except_media_group, (filters.user(BOT_OWNER[0]) & filters.chat(BOT_OWNER[0]) | filters.user(BOT_OWNER[1]) & filters.chat(BOT_OWNER[1])) & ~filters.media_group))
