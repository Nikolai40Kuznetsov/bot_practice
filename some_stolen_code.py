import requests
import telebot
from telebot.types import ReplyKeyboardMarkup
from datetime import datetime
import random
from id import name

BOT_TOKEN = name

bot = telebot.TeleBot(BOT_TOKEN)

keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
keyboard.row('🌤️ Погода в Минске на неделю')
keyboard.row('💰 Курсы валют')
keyboard.row('🌎 Случайная страна', '📊 Криптовалюты')
keyboard.row('❓ Помощь')

def get_weather_minsk():
    """Получение прогноза погоды в Минске на 7 дней через Open-Meteo API"""
    try:
        url = "https://api.open-meteo.com/v1/forecast"
        params = {
            'latitude': 53.9045,
            'longitude': 27.5615,
            'daily': 'temperature_2m_max,temperature_2m_min,weathercode,precipitation_probability',
            'timezone': 'Europe/Minsk',
            'forecast_days': 7
        }
        
        response = requests.get(url, params=params)
        data = response.json()
        
        if 'daily' not in data:
            return "❌ Ошибка получения данных о погоде"
        
        daily = data['daily']
        result = "🌤️ Погода в Минске на неделю:\n\n"
        
        weather_codes = {
            0: "☀️ Ясно",
            1: "🌤️ Преимущественно ясно",
            2: "⛅ Переменная облачность",
            3: "☁️ Пасмурно",
            45: "🌫️ Туман",
            48: "🌫️ Инейный туман",
            51: "🌧️ Легкая морось",
            53: "🌧️ Умеренная морось",
            55: "🌧️ Сильная морось",
            61: "🌧️ Небольшой дождь",
            63: "🌧️ Умеренный дождь",
            65: "🌧️ Сильный дождь",
            80: "🌧️ Ливень",
            81: "🌧️ Сильный ливень",
            82: "🌧️ Очень сильный ливень",
            95: "⛈️ Гроза",
            96: "⛈️ Гроза с градом",
            99: "⛈️ Сильная гроза с градом"
        }
        
        for i in range(7):
            date = datetime.fromisoformat(daily['time'][i]).strftime('%d.%m.%Y')
            temp_max = daily['temperature_2m_max'][i]
            temp_min = daily['temperature_2m_min'][i]
            weather_code = daily['weathercode'][i]
            precip_prob = daily['precipitation_probability'][i]
            
            weather_desc = weather_codes.get(weather_code, "❓ Неизвестная погода")
            
            result += f"📅 {date}:\n"
            result += f"   🌡️ {temp_min:.0f}°C - {temp_max:.0f}°C\n"
            result += f"   {weather_desc}\n"
            result += f"   💧 Вероятность осадков: {precip_prob}%\n\n"
        
        return result
    
    except Exception as e:
        return f"❌ Ошибка получения данных о погоде: {str(e)}"

def get_exchange_rates():
    """Получение курсов валют"""
    try:
        url = "https://api.exchangerate.host/latest"
        params = {
            'base': 'BYN',
            'symbols': 'USD,EUR,RUB,PLN,UAH'
        }
        
        response = requests.get(url, params=params)
        data = response.json()
        
        if not data['success']:
            return "❌ Ошибка получения курсов валют"
        
        rates = data['rates']
        result = "💰 Курсы валют к BYN:\n\n"
        
        currency_symbols = {
            'USD': '🇺🇸 Доллар США',
            'EUR': '🇪🇺 Евро',
            'RUB': '🇷🇺 Российский рубль',
            'PLN': '🇵🇱 Польский злотый',
            'UAH': '🇺🇦 Украинская гривна'
        }
        
        for currency, symbol in currency_symbols.items():
            if currency in rates:
                rate = 1 / rates[currency] 
                result += f"{symbol}:\n"
                result += f"   💰 1 {currency} = {rate:.3f} BYN\n\n"
        
        return result
    
    except Exception as e:
        return f"❌ Ошибка получения курсов валют: {str(e)}"

def get_random_country():
    """Получение информации о случайной стране"""
    try:
        response = requests.get("https://restcountries.com/v3.1/all")
        countries = response.json()
        
        country = random.choice(countries)
        
        result = "🌎 Случайная страна:\n\n"
        result += f"🇺🇳 {country.get('name', {}).get('common', 'Неизвестно')}\n"
        result += f"🏙️ Столица: {', '.join(country.get('capital', ['Неизвестно']))}\n"
        result += f"👥 Население: {country.get('population', 0):,}\n"
        result += f"📏 Площадь: {country.get('area', 0):,} км²\n"
        result += f"🗺️ Регион: {country.get('region', 'Неизвестно')}\n"
        
        if country.get('languages'):
            languages = list(country['languages'].values())
            result += f"🗣️ Языки: {', '.join(languages[:3])}\n"
        
        return result
    
    except Exception as e:
        return f"❌ Ошибка получения информации о стране: {str(e)}"

def get_crypto_prices():
    """Получение курсов основных криптовалют"""
    try:
        url = "https://api.coingecko.com/api/v3/simple/price"
        params = {
            'ids': 'bitcoin,ethereum,binancecoin,cardano,solana',
            'vs_currencies': 'usd',
            'include_24hr_change': 'true'
        }
        
        response = requests.get(url, params=params)
        data = response.json()
        
        result = "📊 Курсы криптовалют:\n\n"
        
        crypto_names = {
            'bitcoin': '₿ Bitcoin',
            'ethereum': 'Ξ Ethereum',
            'binancecoin': 'BNB Binance Coin',
            'cardano': 'ADA Cardano',
            'solana': 'SOL Solana'
        }
        
        for crypto_id, info in data.items():
            if crypto_id in crypto_names:
                price = info['usd']
                change = info['usd_24h_change']
                change_icon = '📈' if change > 0 else '📉'
                
                result += f"{crypto_names[crypto_id]}:\n"
                result += f"   💰 ${price:,.2f}\n"
                result += f"   {change_icon} {change:+.1f}% (24ч)\n\n"
        
        return result
    
    except Exception as e:
        return f"❌ Ошибка получения курсов криптовалют: {str(e)}"

@bot.message_handler(commands=['start'])
def send_welcome(message):
    """Обработчик команды /start"""
    bot.send_message(
        message.chat.id,
        f"👋 Привет, {message.from_user.first_name}!\n"
        "Выберите один из доступных вариантов:",
        reply_markup=keyboard
    )

@bot.message_handler(commands=['help'])
def send_help(message):
    """Обработчик команды /help"""
    help_text = """
🤖 Доступные команды:
/start - начать работу
/help - показать справку

📊 Доступные опции:
🌤️ Погода в Минске на неделю - точный прогноз погоды
💰 Курсы валют - курсы USD, EUR, RUB, PLN, UAH
🌎 Случайная страна - информация о случайной стране
📊 Криптовалюты - курсы основных криптовалют
"""
    bot.send_message(message.chat.id, help_text)

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    """Обработка текстовых сообщений"""
    text = message.text
    
    if text == "🌤️ Погода в Минске на неделю":
        weather_info = get_weather_minsk()
        bot.send_message(message.chat.id, weather_info)
    
    elif text == "💰 Курсы валют":
        exchange_info = get_exchange_rates()
        bot.send_message(message.chat.id, exchange_info)
    
    elif text == "🌎 Случайная страна":
        country_info = get_random_country()
        bot.send_message(message.chat.id, country_info)
    
    elif text == "📊 Криптовалюты":
        crypto_info = get_crypto_prices()
        bot.send_message(message.chat.id, crypto_info)
    
    elif text == "❓ Помощь":
        send_help(message)
    
    else:
        bot.send_message(
            message.chat.id,
            "Я не понимаю эту команду. Используйте кнопки ниже или /help для справки.",
            reply_markup=keyboard
        )

if __name__ == "__main__":
    print("Бот запущен...")
    print("Для остановки нажмите Ctrl+C")
    bot.infinity_polling()