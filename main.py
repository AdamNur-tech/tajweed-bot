import os
import telebot
from openai import OpenAI

# --- КЛЮЧИ ---
BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

bot = telebot.TeleBot(BOT_TOKEN)
client = OpenAI(api_key=OPENAI_API_KEY)

# --- СТАРТ ---
@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message,
        "Ассаляму алейкум! 🤲\n\n"
        "Отправь голосовое сообщение с чтением Корана,\n"
        "и я проверю твой таджвид 📖")

# --- ОБРАБОТКА ГОЛОСА ---
@bot.message_handler(content_types=['voice'])
def handle_voice(message):
    try:
        bot.reply_to(message, "🎧 Анализирую чтение...")

        # скачать голос
        file_info = bot.get_file(message.voice.file_id)
        downloaded = bot.download_file(file_info.file_path)

        with open("voice.ogg", "wb") as f:
            f.write(downloaded)

        # распознавание
        with open("voice.ogg", "rb") as audio:
            transcription = client.audio.transcriptions.create(
                model="gpt-4o-mini-transcribe",
                file=audio
            )

        text = transcription.text

        # анализ таджвида
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content":
                 "Ты учитель таджвида. Проверь чтение Корана. "
                 "Найди ошибки, объясни их и дай советы."},
                {"role": "user", "content": text}
            ]
        )

        result = response.choices[0].message.content

        bot.reply_to(message,
            f"📖 Распознано:\n{text}\n\n"
            f"🧠 Анализ:\n{result}"
        )

    except Exception as e:
        bot.reply_to(message, f"❌ Ошибка: {e}")

# --- ОБЫЧНЫЕ СООБЩЕНИЯ ---
@bot.message_handler(func=lambda message: True)
def text_handler(message):
    bot.reply_to(message,
        "Отправь голосовое сообщение 🎤")

# --- ЗАПУСК ---
print("Бот запущен...")
bot.infinity_polling()