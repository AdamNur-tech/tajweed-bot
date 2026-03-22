import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import os
from openai import OpenAI
import random

BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

bot = telebot.TeleBot(BOT_TOKEN)
client = OpenAI(api_key=OPENAI_API_KEY)

# ===== USERS DB =====
users = {}

def get_user(user_id):
    if user_id not in users:
        users[user_id] = {
            "xp": 0,
            "level": "Beginner",
            "mode": "menu",
            "mistakes": [],
            "current_module": "nun"
        }
    return users[user_id]

# ===== MODULES =====
modules = {
    "nun": {
        "name": "Нун и правила",
        "questions": [
            {
                "text": "مِن بَعْدِ",
                "correct": "Икляб",
                "options": ["Ихфа", "Икляб", "Идгам"]
            },
            {
                "text": "مِنْ شَرِّ",
                "correct": "Ихфа",
                "options": ["Ихфа", "Изхар", "Идгам"]
            }
        ]
    }
}

# ===== LEVEL SYSTEM =====
def update_level(user):
    if user["xp"] > 100:
        user["level"] = "Intermediate"
    if user["xp"] > 300:
        user["level"] = "Advanced"

# ===== MENU =====
def main_menu(chat_id):
    markup = InlineKeyboardMarkup()
    markup.add(
        InlineKeyboardButton("📚 Учиться", callback_data="learn"),
        InlineKeyboardButton("🎯 Практика", callback_data="practice")
    )
    markup.add(
        InlineKeyboardButton("🤖 AI Учитель", callback_data="ai")
    )
    bot.send_message(chat_id, "Выбери:", reply_markup=markup)

# ===== QUESTION =====
def send_question(chat_id, user):
    module = modules[user["current_module"]]
    q = random.choice(module["questions"])

    markup = InlineKeyboardMarkup()

    for opt in q["options"]:
        markup.add(
            InlineKeyboardButton(opt, callback_data=f"ans|{opt}|{q['correct']}")
        )

    bot.send_message(chat_id, f"{q['text']}\n\nЧто это?", reply_markup=markup)

# ===== AI =====
def ai_teacher(text):
    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "system", "content": """
Ты эксперт по таджвиду.
Учишь как преподаватель:
- через ощущения
- исправляешь ошибки
- даёшь практику
"""},

            {"role": "user", "content": text}
        ]
    )
    return response.choices[0].message.content

# ===== VOICE =====
def speech_to_text(file):
    return client.audio.transcriptions.create(
        model="gpt-4o-mini-transcribe",
        file=open(file, "rb")
    ).text

# ===== CALLBACK =====
@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    user = get_user(call.from_user.id)

    if call.data == "learn":
        send_question(call.message.chat.id, user)

    elif call.data.startswith("ans"):
        _, user_ans, correct = call.data.split("|")

        if user_ans == correct:
            user["xp"] += 10
            update_level(user)
            bot.send_message(call.message.chat.id, f"✅ XP: {user['xp']} | Уровень: {user['level']}")
        else:
            user["mistakes"].append(correct)
            bot.send_message(call.message.chat.id, f"❌ Ошибка. Правильно: {correct}")

        send_question(call.message.chat.id, user)

    elif call.data == "ai":
        user["mode"] = "ai"
        bot.send_message(call.message.chat.id, "Задай вопрос или отправь голос")

# ===== TEXT =====
@bot.message_handler(content_types=['text'])
def handle_text(message):
    user = get_user(message.from_user.id)

    if user["mode"] == "ai":
        answer = ai_teacher(message.text)
        bot.send_message(message.chat.id, answer)

# ===== VOICE =====
@bot.message_handler(content_types=['voice'])
def handle_voice(message):
    user = get_user(message.from_user.id)

    file_info = bot.get_file(message.voice.file_id)
    downloaded_file = bot.download_file(file_info.file_path)

    with open("voice.ogg", "wb") as f:
        f.write(downloaded_file)

    text = speech_to_text("voice.ogg")

    bot.send_message(message.chat.id, f"Ты сказал:\n{text}")

    answer = ai_teacher(f"Проверь таджвид: {text}")
    bot.send_message(message.chat.id, answer)

# ===== START =====
@bot.message_handler(commands=['start'])
def start(message):
    main_menu(message.chat.id)

bot.polling()