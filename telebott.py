import telebot
from telebot import types
from id import name
import threading
import time
import schedule

# 5739163615 мой id 

TOKEN = name
bot = telebot.TeleBot(TOKEN)
tg_id = 5739163615

@bot.message_handler(func=lambda message: True)
def send_message(message):
    bot.send_message(message.chat.id, 'Будь здоров, воин')
    schedule.every().day.at("10:05").do(send_message)
    schedule.every().day.at("18:50").do(send_message)
    schedule.every().day.at("22:20").do(send_message)            
         
    
@bot.message_handler(commands=["start"])
def send_welcome(message):
    keyboard_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    info = types.KeyboardButton("Инфо")
    stat = types.KeyboardButton("Статистика")
    video = types.KeyboardButton("Видео")
    keyboard_markup.add(info, stat, video)
    bot.send_message(message.chat.id, "Привет! Я простой бот на telebot", reply_markup=keyboard_markup)

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    if message.text == "Инфо":
        bot.send_message(message.chat.id, "Ты нажал кнопку 'Инфо'")
    elif message.text == "Статистика":
        bot.send_message(message.chat.id, "Ты нажал кнопку 'Статистика'")
        # bot.send_sticker(message.chat.id, 'STICKER_ID')  
    elif message.text == "Видео":
        bot.send_message(message.chat.id, "https://www.youtube.com/watch?v=m9wkjtT-j6o&pp=ygUJcmFpbmJsb29k")
    else:
        bot.send_message(message.chat.id, f"Ты написал: {message.text}")

def main():
    try:
        print("Бот запустился")
        bot.polling(none_stop=True)      
    except Exception as e:
        print(f"Бот не запустился: {e}")
        

if __name__ == "__main__":
    main()