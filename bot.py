import aiohttp
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
import emoji
import os
import asyncio
import parser


help_mesage = '--'
greeting_message = ('Тебя приветствует ФильмБот! \n'
                    'Напиши название фильма или выбери что ты хочешь сделать\n'
                    '\\trending -- популярные сейчас\n'
                    '\\genres -- список жанров\n'
                    '\\help -- помощь')


bot = Bot(token=os.environ['BOT_TOKEN'])
dp = Dispatcher(bot)


def parse_film_name(film_name: str) -> str:
    return 'film_name'


def get_random_film() -> str:
    return '--'


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.answer(greeting_message)


@dp.message_handler(commands=['random'])
async def send_welcome(message: types.Message):
    random_film = '\n'.join(('Вот что я нашел', get_random_film()))
    await message.answer(random_film)


@dp.message_handler(commands=['help'])
async def send_welcome(message: types.Message):
    await message.answer(help_mesage)


@dp.message_handler(commands=['trending'])
async def send_welcome(message: types.Message):
    res = await parser.get_trending()
    answer = await parser.get_films_list(res)
    await message.answer(answer)

#
# @dp.message_handler(regexp=r"i/*")
# async def get_by_id(message: types.Message):
#     p = Parser()
#     p.parse_id(int(message.text[2:]))
#     print(message.text[2:])
#     response, photo = p.output, p.photo
#     await bot.send_photo(message.from_user.id, photo)
#
# @dp.message_handler()
# async def query(message: types.Message):
#     p = Parser()
#     film_name = p.parse_query(message.text)
#     await message.answer(film_name)
#

if __name__ == '__main__':
    executor.start_polling(dp)
