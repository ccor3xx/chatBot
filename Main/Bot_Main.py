import asyncio
import datetime

from aiogram import Bot, Dispatcher, Router, types, F
from aiogram.filters import CommandStart
from aiogram.types import InlineKeyboardMarkup
from task.task1 import router, reply_kbd, gc, sh

from Config import BOT_TOKEN

bot = Bot(BOT_TOKEN)
dp = Dispatcher()
i=0
async def main():
    dp.include_router(router)
    await dp.start_polling(bot)

#Обработчик команды "старт"
@dp.message(CommandStart())
async def start(message: types.Message):
    keyboard = await reply_kbd()
    await message.answer(f"Добро пожаловать в тестового бота под ключ, {message.from_user.full_name}", reply_markup=keyboard)

#Обработчик текстовых сообщений с проверкой даты
@dp.message(F.text)
async def date(message: types.Message):
    msg = message.text
    global i
    try:
        date = datetime.datetime.strptime(msg, "%d.%m.%y")
        await message.answer(f"Дата верна")
        ws = sh.sheet1
        i += 1
        ws.update_cell(i, 2, date.strftime("%d.%m.%y"))

    except ValueError:
        await message.answer(f"Дата не верна")


if __name__ == '__main__':
    asyncio.run(main())
