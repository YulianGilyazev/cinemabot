import aiohttp
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
import os


bot = Bot(token=os.environ['BOT_TOKEN'])
dp = Dispatcher(bot)


def parse_film_name(film_name: str) -> str:
    pass


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    await message.reply("Hi!\nI'm EchoBot!\nPowered by aiogram.")


@dp.message_handler()
async def echo(message: types.Message):
    await message.reply('ты лох')


if __name__ == '__main__':
    executor.start_polling(dp)
