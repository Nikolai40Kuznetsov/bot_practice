import telebot
from telebot import types
from id import name
import requests
import pandas as pd

TOKEN = name
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(Commands = ["start"])
def send_welcome(message):
    keyboard_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    info = types.KeyboardButton("Инфо")
    stat = types.KeyboardButton("Статистика")
    video = types.KeyboardButton("Видео")
    keyboard_markup.add(info, stat, video)
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
        
@bot.message_handler(func=lambda message:True)
def send_video(message):
    if message.text == "Видео":
        bot.send_message(message, "@vid https://www.youtube.com/watch?v=m9wkjtT-j6o&pp=ygUJcmFpbmJsb29k")
        url = f"https://wttr.in/Minsk?format=j1"
        r = requests.get(url).json()
        forecast = {"Date": [], "Temp": [], "Weather": []}
        df = pd.DataFrame(forecast)
        for day in r["weather"]:
            date = day["date"]
            avgtemp = day["avgtempC"]
            desc = day["hourly"][4]["weatherDesc"][0]["value"]
            df.loc[len(df)] = [date, f"{avgtemp}*C", desc]
            bot.send_message(message, df)
        
def main():
    try:
        print("Бот запустился")
        bot.polling(none_stop=True)        
    except:
        print("Бот не запустился")
        

if __name__ == "__main__":
    main()
    

