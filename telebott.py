import telebot
from telebot import types
from id import name

TOKEN = name
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(Commands = ["start"])
def send_welcome(message):
    keyboard_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    info = types.KeyboardButton("Инфо")
    stat = types.KeyboardButton("Статистика")
    keyboard_markup.add(info, stat)
    bot.send_message(message, "Привет! Я простой бот на telebot")

@bot.message_handler(func=lambda message:True)
def echo_all(message):
    if message.text == "Инфо":
        bot.send_message(message, f"Ты нажал кнопку 'Инфо'")
    elif message.text == "Статистика":
        bot.send_message(message, f"Ты нажал кнопку 'Статистика'")
        # bot.send_sticker(message, ':love:')
    else:
        bot.send_message(message, f"Ты написал {message.text}")
        
def main():
    try:
        print("Бот запустился")
        bot.polling(none_stop=True)        
    except:
        print("Бот не запустился")
        

if __name__ == "__main__":
    main()
    

