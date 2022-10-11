from pyrogram import Client

CHANNEL_ANONRUBOT_ID=660309226 #anonrubot
CHANNEL_ANONIMNYYCHATBOT_ID=1434134055 #anonimnyychatbot
CHANNEL_CHATBOT_ID=825312679 #chatbot

APPS_NUMBER = 2
api_id = [,]
api_hash = ["", ""]
BOT_OWNER = [,]

apps = [Client("app_{}".format(i), api_id[i], api_hash[i]) for i in range(APPS_NUMBER)]