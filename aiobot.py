import asyncio
from aiogram import Bot, types, Dispatcher
from aiogram.filters import Command
from id import name


TOKEN = name
bot = Bot(token = TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Привет! Я простой бот на aiogram")

@dp.message()
async def echo(message: types.Message):
    await message.answer(f"Ты написал {message.text}")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
    
