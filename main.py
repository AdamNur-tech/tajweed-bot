import telebot

TOKEN = "8616939480:AAHRjLO85dRGjLfuJGeO-2HHoEADUCr_ECQ"

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Ассаляму алейкум! 🤲\nДобро пожаловать в таджвид-бот!")

@bot.message_handler(func=lambda message: True)
def echo(message):
    bot.send_message(message.chat.id, "Я пока учусь 😊")

print("Бот запущен...")
bot.polling()
