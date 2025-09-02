from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
import id

TOKEN = id.name
bot = Bot(TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands = ['start', 'help'])
async def send_welcome(msg: types.Message):
    await msg.reply_to_message(f"Привет {msg.from_user.first_name}")

if __name__ == "__main__":
    dp.start_polling()
