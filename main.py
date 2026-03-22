import os
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from openai import OpenAI

bot = telebot.TeleBot(os.getenv("BOT_TOKEN"))
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

users = {}

LESSONS = {
1: "📚 Урок 1: Алиф Ба Та\nا ب ت\nПовтори",
2: "📚 Урок 2: Харакаты\nبَ بِ بُ",
3: "📚 Урок 3: Сукун\nبْ",
4: "📚 Урок 4: Нун сакина\n4 правила",
5: "📚 Урок 5: Мадд\n2 хараката",
}

QUIZ = {
1: ("Что это: ا ?", "алиф"),
2: ("بَ читается как?", "ба"),
3: ("Что значит сукун?", "нет гласной"),
4: ("Сколько правил нун?", "4"),
5: ("Сколько харакат мадд?", "2"),
}

# --- UI ---
def main_menu():
    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton("📚 Начать обучение", callback_data="learn"))
    kb.add(InlineKeyboardButton("🎤 Проверить чтение", callback_data="voice"))
    kb.add(InlineKeyboardButton("📊 Прогресс", callback_data="progress"))
    return kb

def next_btn():
    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton("➡️ Далее", callback_data="next"))
    return kb

def quiz_btn():
    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton("🧠 Пройти тест", callback_data="quiz"))
    return kb

# --- START ---
@bot.message_handler(commands=['start'])
def start(m):
    uid = m.from_user.id

    if uid not in users:
        users[uid] = {"level":1, "step":"menu"}

    bot.send_message(m.chat.id,
        "🎓 Медресе таджвида\n\n"
        "Ты пройдёшь путь до уровня кари 📖",
        reply_markup=main_menu())

# --- КНОПКИ ---
@bot.callback_query_handler(func=lambda call: True)
def handler(call):
    uid = call.from_user.id
    user = users[uid]

    # --- НАЧАТЬ ---
    if call.data == "learn":
        lvl = user["level"]
        bot.send_message(call.message.chat.id, LESSONS[lvl], reply_markup=quiz_btn())
        user["step"] = "lesson"

    # --- ТЕСТ ---
    elif call.data == "quiz":
        lvl = user["level"]
        q,_ = QUIZ[lvl]

        bot.send_message(call.message.chat.id, f"❓ {q}")
        user["step"] = "quiz"

    # --- ДАЛЕЕ ---
    elif call.data == "next":
        user["level"] += 1
        lvl = user["level"]

        if lvl in LESSONS:
            bot.send_message(call.message.chat.id, LESSONS[lvl], reply_markup=quiz_btn())
        else:
            bot.send_message(call.message.chat.id, "🎉 Ты прошёл курс!")

    # --- ПРОГРЕСС ---
    elif call.data == "progress":
        bot.send_message(call.message.chat.id,
            f"📊 Уровень: {user['level']}")

    # --- ГОЛОС ---
    elif call.data == "voice":
        bot.send_message(call.message.chat.id,
            "🎤 Отправь голосовое с чтением")

# --- ОТВЕТ НА ТЕСТ ---
@bot.message_handler(func=lambda m: users.get(m.from_user.id,{}).get("step")=="quiz")
def answer(m):
    uid = m.from_user.id
    user = users[uid]
    lvl = user["level"]

    _,correct = QUIZ[lvl]

    if correct in m.text.lower():
        bot.send_message(m.chat.id, "✅ Правильно!", reply_markup=next_btn())
    else:
        bot.send_message(m.chat.id, f"❌ Неправильно\nОтвет: {correct}")

    user["step"] = "menu"

# --- ГОЛОС ---
@bot.message_handler(content_types=['voice'])
def voice(m):
    bot.send_message(m.chat.id, "🎧 Анализ...")

    file = bot.get_file(m.voice.file_id)
    audio = bot.download_file(file.file_path)

    with open("voice.ogg","wb") as f:
        f.write(audio)

    with open("voice.ogg","rb") as f:
        t = client.audio.transcriptions.create(
            model="gpt-4o-mini-transcribe",
            file=f
        )

    res = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role":"system","content":"Проверь таджвид и укажи ошибки"},
            {"role":"user","content":t.text}
        ]
    )

    bot.send_message(m.chat.id,
        f"📖 {t.text}\n\n🧠 {res.choices[0].message.content}"
    )

print("APP BOT RUNNING 🚀")
bot.infinity_polling()