from datetime import datetime
import json
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from config import bot_token
from rate import parse
from weather import main

bot = Bot(token=bot_token, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)

btnConverter = KeyboardButton('Поулчить курс валют')
btnWeather = KeyboardButton('Получить прогноз погоды')
menu = ReplyKeyboardMarkup(resize_keyboard=True).add(btnConverter, btnWeather)

@dp.message_handler(commands='start')
async def start(message):
    await message.reply("It's our bot special for Hackathon)")

# converter
@dp.message_handler(commands='get_convert')
async def get_converter(message):
    parse()
    with open('/home/atai/Desktop/Bootcamp/week11/sneakers/TgBot/rate.json') as file:
        rate = json.load(file)
    
    await message.answer(f'<b>{datetime.now().date()}</b>')
    for k, v in rate.items():
        conv = f'{k}: {v}'
        await message.answer(conv)

# weather
@dp.message_handler(commands='get_weather')
async def get_weather(message):
    main()
    with open('/home/atai/Desktop/Bootcamp/week11/sneakers/TgBot/weather.json') as file:
        weather = json.load(file)

    await message.answer(f'<b>{datetime.now().date()}</b>')
    await message.answer(weather)

if __name__ == '__main__':
    executor.start_polling(dp)
