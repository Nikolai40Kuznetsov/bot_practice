import telebot
from telebot import types
# from id import name
import requests
import pandas as pd
import random

TOKEN = data
bot = telebot.TeleBot(TOKEN)

def tell_weather(message):
    url = "https://wttr.in/Minsk?format=j1"
    r = requests.get(url).json()
    forecast = {"Date": [], "Temp": [], "Weather": []}
    df = pd.DataFrame(forecast)
    for day in r["weather"]:
        date = day["date"]
        avgtemp = day["avgtempC"]
        desc = day["hourly"][4]["weatherDesc"][0]["value"]
        df.loc[len(df)] = [date, f"{avgtemp}*C", desc]
        bot.send_message(message, df)

def get_random_country(message):
    response = "https://restcountries.com/v3.1/all"
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
    bot.send_message(message, result)

def rewards_info(message):
    site = f"https://poisk.re/awards"
    awards = requests.get(site).json()
    man = random.choice(awards)
    bot.send_message(message, man)        
    
@bot.message_handler(content_types=['text'])
def handle_message(message):
    if message.text == "Старт":
        keyboard_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        info = types.KeyboardButton("Инфо")
        video = types.KeyboardButton("Видео")
        weather = types.KeyboardButton("Погода")
        country = types.KeyboardButton("Информация о случайной стране")
        hero = types.KeyboardButton("Случайный награждённый солдат")
        keyboard_markup.add(info, video, weather)    
        keyboard_markup.add(country)
        keyboard_markup.add(hero)    
        bot.send_message(message.chat.id, "Привет! Я простой бот на telebot", reply_markup=keyboard_markup)    
    elif message.text == "Инфо":
        bot.send_message(message.chat.id, "Ты нажал кнопку 'Инфо'")    
    elif message.text == "Погода":
        tell_weather(message.chat.id)   
    elif message.text == "Информация о случайной стране":
        get_random_country(message.chat.id)
    elif message.text == "Случайный награждённый солдат":
        rewards_info(message.chat.id)
        # bot.send_sticker(message, ':love:') 
    elif message.text == "Видео":
        bot.send_message(message.chat.id, "https://www.youtube.com/watch?v=m9wkjtT-j6o")    
    else:
        bot.send_message(message.chat.id, f"Вы написали \"{message.text}\", я не знаю такой команды")
        start_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        start_button = types.KeyboardButton("Старт")
        start_keyboard.add(start_button)
        bot.send_message(message.chat.id, "Нажмите кнопку 'Старт' чтобы начать", reply_markup=start_keyboard)   

def main():
    try:
        print("Бот запустился")
        bot.polling(none_stop=True)        
    except:
        print("Бот не запустился")
        
if __name__ == "__main__":
    main()
