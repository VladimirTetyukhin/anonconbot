import asyncio
from pyrogram import Client, filters, idle
from config import apps
from handlers import anonimnyychatbot, anonrubot, chatbot


for app in apps:
    anonimnyychatbot.register_handlers_anonimnyychatbot(app)
    #anonrubot.register_handlers_anonrubot(app)
    #chatbot.register_handlers_chatbot(app)

