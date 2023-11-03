import asyncio
import json
from mongodb import client
from telebot.async_telebot import AsyncTeleBot
client.restore()
bot = AsyncTeleBot("5567350822:AAFvaj8rMvXF1BEelsjpzbgXy7gaoRq2LCc")


# Handle '/start' and '/help'
@bot.message_handler(commands=['help', 'start'])
async def send_welcome(message):
    await bot.reply_to(message, """Hi there, I am EchoBot.""")


# Handle all other messages with content_type 'text' (content_types defaults to ['text'])
@bot.message_handler(func=lambda message: True)
async def echo_message(message):
    print(message)
    text = message.text
    dct = json.loads(text)
    data = client.get_data_to_db(dct)
    dataset = json.dumps(data)

    await bot.send_message(message.chat.id, dataset)


asyncio.run(bot.polling())
