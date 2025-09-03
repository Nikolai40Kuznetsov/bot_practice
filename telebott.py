import telebot
from id import name

TOKEN = name
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(Commands = ["start"])
def send_welcome(message):
    bot.reply_to(message, "Привет! Я простой бот на telebot")

@bot.message_handler(func=lambda message:True)
def echo_all(message):
    bot.reply_to(message, f"Ты написал {message.text}")

def main():
    bot.polling(none_stop=True)

if __name__ == "__main__":
    main()
    

