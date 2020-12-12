from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
import os
import src.parser as parser
from src.messages import greeting_message, help_message, empty_result_message, no_film


from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)


bot = Bot(token=os.environ["BOT_TOKEN"])
dp = Dispatcher(bot)


@dp.message_handler(commands=["start"])
async def send_welcome(message: types.Message):
    inline_kb_full = InlineKeyboardMarkup(row_width=2)
    inline_kb_full.add(InlineKeyboardButton("Случайный фильм", callback_data="random"))
    inline_kb_full.add(
        InlineKeyboardButton("Популярно сейчас", callback_data="trending")
    )
    await message.answer(greeting_message, reply_markup=inline_kb_full)

@dp.message_handler(commands=["help"])
async def send_welcome(message: types.Message):
    inline_kb_full = InlineKeyboardMarkup(row_width=2)
    inline_kb_full.add(InlineKeyboardButton("Случайный фильм", callback_data="random"))
    inline_kb_full.add(
        InlineKeyboardButton("Популярно сейчас", callback_data="trending")
    )
    await message.answer(help_message, reply_markup=inline_kb_full)


@dp.callback_query_handler(lambda c: c.data == "random")
async def process_callback_random(callback_query: types.CallbackQuery):
    film_id = parser.get_random_film()
    film = await parser.get_film_by_id(film_id)
    answer, tmdb, ivi, netflix = await parser.get_film_full(film)
    photo = await parser.get_film_poster(film)
    inline_kb_full = InlineKeyboardMarkup(row_width=2)
    if ivi is not None:
        inline_kb_full.add(InlineKeyboardButton("IVI", url=ivi))
    if netflix is not None:
        inline_kb_full.add(InlineKeyboardButton("Netflix", url=netflix))
    if tmdb is not None:
        inline_kb_full.add(InlineKeyboardButton("TMDB", url=tmdb))
    if photo is not None:
        await bot.send_photo(
            callback_query.from_user.id,
            photo,
            caption=answer,
            reply_markup=inline_kb_full,
        )
    else:
        await bot.send_message(
            callback_query.from_user.id, answer, reply_markup=inline_kb_full
        )


@dp.callback_query_handler(lambda c: c.data == "trending")
async def process_callback_trending(callback_query: types.CallbackQuery):
    res = await parser.get_trending()
    answer = await parser.get_films_list(res)
    await bot.send_message(callback_query.from_user.id, answer)


@dp.message_handler(commands=["random"])
async def send_welcome(message: types.Message):
    film_id = parser.get_random_film()
    film = await parser.get_film_by_id(film_id)
    if film is None:
        await message.answer(no_film)
        return
    answer, tmdb, ivi, netflix = await parser.get_film_full(film)
    photo = await parser.get_film_poster(film)
    inline_kb_full = InlineKeyboardMarkup(row_width=2)
    if ivi is not None:
        inline_kb_full.add(InlineKeyboardButton("IVI", url=ivi))
    if netflix is not None:
        inline_kb_full.add(InlineKeyboardButton("Netflix", url=netflix))
    if tmdb is not None:
        inline_kb_full.add(InlineKeyboardButton("TMDB", url=tmdb))
    if photo is not None:
        await message.answer_photo(photo, caption=answer, reply_markup=inline_kb_full)
    else:
        await message.answer(answer, reply_markup=inline_kb_full)


@dp.message_handler(commands=["trending"])
async def send_welcome(message: types.Message):
    res = await parser.get_trending()
    answer = await parser.get_films_list(res)
    await message.answer(answer)


@dp.message_handler(regexp=r"/id*")
async def send_film_by_id(message: types.Message):
    film = await parser.get_film_by_id(message.text[3:])
    if film is None:
        await message.answer(no_film)
        return
    answer, tmdb, ivi, netflix = await parser.get_film_full(film)
    photo = await parser.get_film_poster(film)
    inline_kb_full = InlineKeyboardMarkup(row_width=2)
    if ivi is not None:
        inline_kb_full.add(InlineKeyboardButton("IVI", url=ivi))
    if netflix is not None:
        inline_kb_full.add(InlineKeyboardButton("Netflix", url=netflix))
    if tmdb is not None:
        inline_kb_full.add(InlineKeyboardButton("TMDB", url=tmdb))
    if photo is not None:
        await message.answer_photo(photo, caption=answer, reply_markup=inline_kb_full)
    else:
        await message.answer(answer, reply_markup=inline_kb_full)


@dp.message_handler()
async def query(message: types.Message):
    films = await parser.get_films_by_text(message.text)
    if films is None:
        await message.answer(empty_result_message)
        return
    answer = await parser.get_films_list(films)
    if answer is None or answer == "":
        await message.answer(empty_result_message)
        return
    await message.answer(answer)


if __name__ == "__main__":
    parser.read_ids()
    executor.start_polling(dp)
