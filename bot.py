from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
import os
import src.parser as parser
from src.messages import greeting_message, help_message


from aiogram.types import (
    ReplyKeyboardRemove,
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)

button_help = KeyboardButton("/help -- помощь")
button_random = KeyboardButton("/random -- случайный фильм")
button_trending = KeyboardButton("/trending -- помощь")


greet_kb = ReplyKeyboardMarkup()
greet_kb.add(button_help)
greet_kb.add(button_random)
greet_kb.add(button_trending)


bot = Bot(token=os.environ["BOT_TOKEN"])
dp = Dispatcher(bot)


@dp.message_handler(commands=["start"])
async def send_welcome(message: types.Message):
    await message.answer(greeting_message)


@dp.message_handler(commands=["random"])
async def send_welcome(message: types.Message):
    film_id = parser.get_random_film()
    film = await parser.get_film_by_id(film_id)
    answer = await parser.get_film_full(film)
    await message.answer(answer)


@dp.message_handler(commands=["help"])
async def send_welcome(message: types.Message):
    await message.answer(help_message, reply_markup=greet_kb)


@dp.message_handler(commands=["trending"])
async def send_welcome(message: types.Message):
    res = await parser.get_trending()
    answer = await parser.get_films_list(res)
    await message.answer(answer)


@dp.message_handler(regexp=r"/id*")
async def send_film_by_id(message: types.Message):
    film = await parser.get_film_by_id(message.text[3:])
    answer = await parser.get_film_full(film)
    photo = await parser.get_film_poster(film)
    if photo is not None:
        await message.answer_photo(photo, caption=answer)
    else:
        await message.answer(answer)


@dp.message_handler()
async def query(message: types.Message):
    films = await parser.get_films_by_text(message.text)
    answer = await parser.get_films_list(films)
    await message.answer(answer)


if __name__ == "__main__":
    parser.read_ids()
    executor.start_polling(dp)
