import asyncio
from pyrogram import Client, filters, idle

from create_bot import apps

for app in apps:
    app.start()

idle()

for app in apps:
    app.stop()