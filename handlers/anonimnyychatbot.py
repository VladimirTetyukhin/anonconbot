import asyncio
from pyrogram import Client, filters, idle
from pyrogram.handlers import MessageHandler
from config import CHANNEL_ANONIMNYYCHATBOT_ID
from config import BOT_OWNER, api_id, api_hash
from create_bot import apps
import emoji
import regex

user_pic = ['','']

async def user_pic_default():
    user_pic = ['', '']

async def user_pic_is_repeat(client_pic, client_api_id):
    #print(client_pic)
    user_pic[client_api_id == api_id[0]] = client_pic
    return user_pic[0] == user_pic[1]

async def other_owner(client_api_id):
    return BOT_OWNER[client_api_id == api_id[0]]

async def send_text(client, message):
    if (message.text.startswith("Диалог остановлен") or
            message.text.startswith("Команда не найдена")):
        await client.send_message(
            chat_id=message.chat.id,
            text="/next"
        )
        await client.send_message(
            chat_id=await other_owner(client.api_id),
            text="/next"
        )
        await user_pic_default()
        return

    if message.text.startswith("🤖 Собеседник"):
        await client.send_message(
            chat_id=await other_owner(client.api_id),
            text="@{}".format(message.entities[0].user.username)
        )
        return

    if message.text.startswith("Нашёл кое-кого"):
        #print(message.text)
        if await user_pic_is_repeat(message.text, client.api_id):
            await client.send_message(
                chat_id=message.chat.id,
                text="/next"
            )
            await user_pic_default()
        return
  

    if (message.text.startswith("Пожалуйста, оцените") or
            message.text.startswith("🤖 Нельзя") or
            message.text.startswith("😾 Для") or
            message.text.startswith("Вы уже находитесь") or
            message.text.startswith("🤖 Вы собираетесь") or
            message.text.startswith("🤖 Данный") or
            message.text.startswith("Ищу собеседника") or
            message.text.startswith("Отправлять ссылки разрешено") or
            #message.text.startswith("Нашёл кое-кого") or
            message.text.startswith("Правила чата:") or
            message.text.startswith("Вам запрещено") or
            message.text.startswith("✅ Проверка")):
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
        message_id=message.id,
        reply_to_message_id = message.reply_to_message_id
    )

async def send_media_group(client, message):
    await client.copy_media_group(
        chat_id=await other_owner(client.api_id),
        from_chat_id=message.chat.id,
        message_id=message.id
    )

async def copy_media_group(client, message):
    await client.copy_media_group(
        chat_id=CHANNEL_ANONIMNYYCHATBOT_ID,
        from_chat_id=message.chat.id,
        message_id=message.id
    )

async def copy_all_except_media_group(client, message):
    await client.copy_message(
        chat_id=CHANNEL_ANONIMNYYCHATBOT_ID,
        from_chat_id=message.chat.id,
        message_id=message.id
    )



def register_handlers_anonimnyychatbot(app: Client):
    app.add_handler(MessageHandler(send_text, (filters.user(CHANNEL_ANONIMNYYCHATBOT_ID) & filters.chat(CHANNEL_ANONIMNYYCHATBOT_ID)) & filters.text))
    app.add_handler(MessageHandler(send_all_except_text_and_media_group, (filters.user(CHANNEL_ANONIMNYYCHATBOT_ID) & filters.chat(CHANNEL_ANONIMNYYCHATBOT_ID)) & ~filters.text & ~filters.media_group))
    app.add_handler(MessageHandler(send_media_group, (filters.user(CHANNEL_ANONIMNYYCHATBOT_ID) & filters.chat(CHANNEL_ANONIMNYYCHATBOT_ID)) & filters.media_group))
    app.add_handler(MessageHandler(copy_media_group, (filters.user(BOT_OWNER[0]) & filters.chat(BOT_OWNER[0]) | filters.user(BOT_OWNER[1]) & filters.chat(BOT_OWNER[1])) & filters.media_group))
    app.add_handler(MessageHandler(copy_all_except_media_group, (filters.user(BOT_OWNER[0]) & filters.chat(BOT_OWNER[0]) | filters.user(BOT_OWNER[1]) & filters.chat(BOT_OWNER[1])) & ~filters.media_group))
