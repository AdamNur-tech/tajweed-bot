import os
import telebot
from flask import Flask, request
from openai import OpenAI

# --- CONFIG ---
BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
BASE_URL = os.getenv("BASE_URL")

bot = telebot.TeleBot(BOT_TOKEN)
app = Flask(__name__)
client = OpenAI(api_key=OPENAI_API_KEY)

users = {}

# --- USER ---
def get_user(user_id):
    if user_id not in users:
        users[user_id] = {
            "level": 1,
            "errors": [],
            "lesson": 0
        }
    return users[user_id]

# --- УРОКИ ---
LESSONS = [
    {"title": "Алиф", "text": "ا", "desc": "Алиф читается как 'А'"},
    {"title": "Ба", "text": "ب", "desc": "Ба читается как 'Б'"},
    {"title": "Та", "text": "ت", "desc": "Та читается как 'Т'"},
    {"title": "Са", "text": "ث", "desc": "Са — межзубный звук"},
]

# --- СТАРТ ---
@bot.message_handler(commands=["start"])
def start(m):
    bot.send_message(m.chat.id,
        "📚 AI Медресе таджвида\n\n"
        "Команды:\n"
        "📖 урок\n"
        "🧠 тест\n"
        "🎤 практика\n"
        "📊 прогресс"
    )

# --- УРОК ---
@bot.message_handler(func=lambda m: m.text.lower() == "урок")
def lesson(m):
    user = get_user(m.from_user.id)
    l = LESSONS[user["lesson"] % len(LESSONS)]

    bot.send_message(m.chat.id,
        f"📖 Урок {user['lesson']+1}\n\n"
        f"{l['title']}: {l['text']}\n\n"
        f"{l['desc']}"
    )

    user["lesson"] += 1

# --- ТЕСТ ---
@bot.message_handler(func=lambda m: m.text.lower() == "тест")
def test(m):
    user = get_user(m.from_user.id)
    l = LESSONS[(user["lesson"]-1) % len(LESSONS)]

    bot.send_message(m.chat.id,
        f"❓ Как читается:\n\n{l['text']}"
    )

    user["test"] = l["title"].lower()

@bot.message_handler(func=lambda m: True)
def answer(m):
    user = get_user(m.from_user.id)

    if "test" in user:
        if m.text.lower() == user["test"]:
            bot.send_message(m.chat.id, "✅ Правильно!")
            user["level"] += 1
        else:
            bot.send_message(m.chat.id, "❌ Ошибка")
            user["errors"].append(m.text)

        del user["test"]

# --- ПРОГРЕСС ---
@bot.message_handler(func=lambda m: m.text.lower() == "прогресс")
def progress(m):
    user = get_user(m.from_user.id)

    bot.send_message(m.chat.id,
        f"📊 Уровень: {user['level']}\n"
        f"Ошибки: {len(user['errors'])}"
    )

# --- ГОЛОС ---
@bot.message_handler(content_types=["voice"])
def voice(m):
    bot.send_message(m.chat.id, "🎤 Анализирую...")

    res = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{
            "role": "user",
            "content": "Оцени чтение Корана и дай таджвид ошибки"
        }]
    )

    bot.send_message(m.chat.id,
        f"🧠 Разбор:\n{res.choices[0].message.content}"
    )

# --- WEBHOOK ---
@app.route(f"/{BOT_TOKEN}", methods=["POST"])
def webhook():
    json_str = request.get_data().decode("UTF-8")
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return "ok"

# --- SET WEBHOOK ---
@app.route("/set_webhook")
def set_webhook():
    bot.remove_webhook()
    bot.set_webhook(url=f"{BASE_URL}/{BOT_TOKEN}")
    return "Webhook set"

# --- RUN ---
PORT = int(os.environ.get("PORT", 8080))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT)