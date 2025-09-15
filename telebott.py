import telebot
from telebot import types
import requests
import pandas as pd
import random
from datetime import datetime
import os

TOKEN = name
bot = telebot.TeleBot(TOKEN)

call_id = 0
LOG_FILE = "bot_logs.csv"

def log_to_file():
    if not os.path.exists(LOG_FILE):
        log_df = pd.DataFrame(columns=[
            'Unic_ID', 
            '@TG_nick', 
            'Motion', 
            'API', 
            'Date', 
            'Time', 
            'API_answer'
        ])
        log_df.to_csv(LOG_FILE, index=False, encoding='utf-8')

def write_log_to_file(log_entry):
    log_to_file()
    try:
        log_df = pd.read_csv(LOG_FILE, encoding='utf-8')
    except:
        log_df = pd.DataFrame(columns=[
            'Unic_ID', 
            '@TG_nick', 
            'Motion', 
            'API', 
            'Date', 
            'Time', 
            'API_answer'
        ])
    new_log_df = pd.DataFrame([log_entry])
    log_df = pd.concat([log_df, new_log_df], ignore_index=True)
    log_df.to_csv(LOG_FILE, index=False, encoding='utf-8')

def log_user_action(chat_id, motion_text, api_name="NONE", api_response="NONE"):
    global call_id
    try:
        chat_info = bot.get_chat(chat_id)
        username = chat_info.username if chat_info.username else "Неизвестно"
        first_name = chat_info.first_name if chat_info.first_name else "Неизвестно"
        last_name = chat_info.last_name if chat_info.last_name else ""
        user_info = f"@{username}" if username != "Неизвестно" else f"{first_name} {last_name}".strip()
    except:
        user_info = "Неизвестно"
    
    call_id += 1
    current_date = datetime.now().strftime("%Y-%m-%d")
    current_time = datetime.now().strftime("%H:%M:%S")
    
    log_entry = {
        'Unic_ID': call_id,
        '@TG_nick': user_info, 
        'Motion': motion_text, 
        'API': api_name, 
        'Date': current_date, 
        'Time': current_time, 
        'API_answer': api_response
    }
    
    write_log_to_file(log_entry)

def log_api_call(func):
    def wrapper(chat_id, *args, **kwargs):
        global call_id
        try:
            chat_info = bot.get_chat(chat_id)
            username = chat_info.username if chat_info.username else "Неизвестно"
            first_name = chat_info.first_name if chat_info.first_name else "Неизвестно"
            last_name = chat_info.last_name if chat_info.last_name else ""
            user_info = f"@{username}" if username != "Неизвестно" else f"{first_name} {last_name}".strip()
        except:
            user_info = "Неизвестно"
        call_id += 1
        api_name = func.__name__
        current_date = datetime.now().strftime("%Y-%m-%d")
        current_time = datetime.now().strftime("%H:%M:%S")
        
        result = func(chat_id, *args, **kwargs)
        api_response = "Успешно"
            
        log_entry = {
            'Unic_ID': call_id,
            '@TG_nick': user_info, 
            'Motion': api_name.replace('_', ' ').title(), 
            'API': api_name, 
            'Date': current_date, 
            'Time': current_time, 
            'API_answer': api_response
        }
        write_log_to_file(log_entry)
        return result
    return wrapper

@log_api_call
def tell_weather(chat_id):
    try:
        url = "https://wttr.in/Minsk?format=j1"
        r = requests.get(url).json()
        forecast = {"Date": [], "Temp": [], "Weather": []}
        df = pd.DataFrame(forecast)
        for day in r["weather"]:
            date = day["date"]
            avgtemp = day["avgtempC"]
            desc = day["hourly"][4]["weatherDesc"][0]["value"]
            df.loc[len(df)] = [date, f"{avgtemp}*C", desc]
        bot.send_message(chat_id, df.to_string(index=False))
        return "Данные о погоде получены"
    except Exception as e:
        bot.send_message(chat_id, f"Ошибка получения погоды: {str(e)}")
        raise e

@log_api_call
def get_random_country(chat_id): 
    try:
        i = random.randint(0, 5)
        if i == 0:
            response = "https://restcountries.com/v3.1/name/Russia"
        if i == 1:
            response = "https://restcountries.com/v3.1/name/Belarus"
        if i == 2:
            response = "https://restcountries.com/v3.1/name/England"
        if i == 3:
            response = "https://restcountries.com/v3.1/name/Spain"
        if i == 4:
            response = "https://restcountries.com/v3.1/name/Croatia"
        if i == 5:
            response = "https://restcountries.com/v3.1/name/Italy"
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
        bot.send_message(chat_id, result)
        return "Данные о стране получены"
    except Exception as e:
        bot.send_message(chat_id, f"Ошибка получения данных о стране: {str(e)}")
        raise e

@log_api_call
def metals_cost(chat_id):
    today = datetime.now().date()
    try:
        site = f"https://api.nbrb.by/bankingots/prices?startdate={today}&endDate={today}"
        response = requests.get(site)
        metals = response.json()
        if not metals:
            bot.send_message(chat_id, "На сегодня данных о драгметаллах нет")
            return "Нет данных на сегодня"
        result = "Цены на драгметаллы на сегодня:\n"
        for metal in metals:
            name = metal.get("MetalId", "Неизвестно")
            if name == 0:
                name = "Золото"
            if name == 1:
                name = "Серебро"
            if name == 2:
                name = "Платина"
            if name == 3:
                name = "Палладий"
            price = metal.get("Value", 0)
            result += f"{name}: {price} BYN\n"
            
        bot.send_message(chat_id, result)
        return "Данные о металлах получены"
    except Exception as e:
        bot.send_message(chat_id, f"Ошибка получения данных о цене драгметаллов: {str(e)}")
        raise e

@bot.message_handler(content_types=['text'])
def handle_message(message):
    if message.text == "Старт":
        log_user_action(message.chat.id, "Старт", "NONE", "NONE")
        keyboard_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        info = types.KeyboardButton("Инфо")
        video = types.KeyboardButton("Видео")
        weather = types.KeyboardButton("Погода")
        country = types.KeyboardButton("Информация о случайной стране")
        metals = types.KeyboardButton("Цены на драгметаллы")
        keyboard_markup.add(info, video, weather)    
        keyboard_markup.add(country)
        keyboard_markup.add(metals)    
        bot.send_message(message.chat.id, "Привет! Я простой бот на telebot", reply_markup=keyboard_markup)    
    elif message.text == "Инфо":
        log_user_action(message.chat.id, f"Инфо", "NONE", "NONE")
        bot.send_message(message.chat.id, "Ты нажал кнопку 'Инфо'")    
    elif message.text == "Погода":
        tell_weather(message.chat.id) 
    elif message.text == "Информация о случайной стране":
        get_random_country(message.chat.id)
    elif message.text == "Цены на драгметаллы":
        metals_cost(message.chat.id) 
    elif message.text == "Видео":
        log_user_action(message.chat.id, f"Запрос видео", "NONE", "NONE")
        bot.send_message(message.chat.id, "https://www.youtube.com/watch?v=m9wkjtT-j6o")    
    else:
        log_user_action(message.chat.id, f"Keyboard typing", "NONE", "NONE")
        start_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        start_button = types.KeyboardButton("Старт")
        start_keyboard.add(start_button)
        bot.send_message(message.chat.id, f"Вы написали \"{message.text}\", я не знаю такой команды", reply_markup=start_keyboard)

def main():
    try:
        log_to_file()
        print(f"Бот запустился. Логи будут сохраняться в файл: {LOG_FILE}")
        bot.polling(none_stop=True)        
    except Exception as e:
        print(f"Бот не запустился: {str(e)}")
        
if __name__ == "__main__":
    main()