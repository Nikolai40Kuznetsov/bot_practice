import asyncio
from aiogram import Bot, types, Dispatcher
from aiogram.filters import Command
from id import name

TOKEN = name
bot = Bot(token = TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def send_welcome(message: types.Message):
    keyboard_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    info = types.KeyboardButton("Инфо")
    stat = types.KeyboardButton("Статистика")
    keyboard_markup.add(info, stat)
    await message.answer("Привет! Я простой бот на aiogram")    

@dp.message()
async def echo(message: types.Sticker):
    if message.text == "Инфо":
        await message.answer(message, f"Ты нажал кнопку 'Инфо'")
    elif message.text == "Статистика":
        await message.answer(message, f"Ты нажал кнопку 'Статистика'")
        # bot.send_sticker(message, ':love:')
    else:
        await message.answer(f"Ты написал {message.text}")
        await message.answer(message, f"ID твоего стикера: {message.sticker.file_id}", parse_mode="Markdown")

async def main():
    try:
        print("Бот запустился")
        await dp.start_polling(bot)
    except:
        print("Бот не запустился") 


if __name__ == "__main__":
    asyncio.run(main())