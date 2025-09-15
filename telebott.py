import telebot
from telebot import types
from id import name
import requests
import pandas as pd
import random

TOKEN = name
bot = telebot.TeleBot(TOKEN)

def tell_weather(message):
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

def get_random_country():
    response = f"https://restcountries.com/v3.1/all"
    countries = requests.get(response).json()     
    country = random.choice(countries)        
    result = "Случайная страна:\n\n"
    result += f"🇺🇳 {country.get('name', {}).get('common', 'Неизвестно')}\n"
    result += f"Столица: {', '.join(country.get('capital', ['Неизвестно']))}\n"
    result += f"Население: {country.get('population', 0):,}\n"
    result += f"Площадь: {country.get('area', 0):,} км²\n"
    result += f"Регион: {country.get('region', 'Неизвестно')}\n"
    if country.get('languages'):
        languages = list(country['languages'].values())
        result += f"Языки: {', '.join(languages[:3])}\n"
    return result

@bot.message_handler(Commands = ["start"])
def send_welcome(message):
    keyboard_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    info = types.KeyboardButton("Инфо")
    video = types.KeyboardButton("Видео")
    weather = types.KeyboardButton("Погода")
    country = types.KeyboardButton("Информация о случайной стране")
    keyboard_markup.add(info, video, weather)
    keyboard_markup.add(country)
    bot.send_message(message, "Привет! Я простой бот на telebot")

@bot.message_handler(func=lambda message:True)
def echo_all(message):
    if message.text == "Инфо":
        bot.send_message(message, f"Ты нажал кнопку 'Инфо'")
    elif message.text == "Погода":
        tell_weather()
    elif message.text == "Информация о случайной стране":
        get_random_country()
        # bot.send_sticker(message, ':love:')
    else:
        bot.send_message(message, f"Ты написал {message.text}")
        
@bot.message_handler(func=lambda message:True)
def send_video(message):
    if message.text == "Видео":
        bot.send_message(message, "@vid https://www.youtube.com/watch?v=m9wkjtT-j6o&pp=ygUJcmFpbmJsb29k")

def main():
    try:
        print("Бот запустился")
        bot.polling(none_stop=True)        
    except:
        print("Бот не запустился")
        
if __name__ == "__main__":
    main()