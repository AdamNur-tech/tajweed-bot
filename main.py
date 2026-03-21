import os
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from openai import OpenAI

BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

bot = telebot.TeleBot(BOT_TOKEN)
client = OpenAI(api_key=OPENAI_API_KEY)

users = {}

FREE_LIMIT = 3

# --- УРОКИ ---
LESSONS = {
    1: "📚 Нун сакина:\n\nИзхар, Идгам, Ихфа, Икляб",
    2: "📚 Мадд:\n\nУдлинение звука",
    3: "📚 Калькаля:\n\nОтражение звука",
}

# --- ВОПРОСЫ ---
QUIZ = {
    1: ("Сколько правил у нун сакина?", "4"),
    2: ("Минимальный мадд?", "2"),
}

# --- МЕНЮ ---
def menu():
    m = InlineKeyboardMarkup()
    m.add(
        InlineKeyboardButton("📚 Урок", callback_data="lesson"),
        InlineKeyboardButton("🧠 Тест", callback_data="quiz")
    )
    m.add(
        InlineKeyboardButton("🎤 Проверка", callback_data="voice"),
        InlineKeyboardButton("📊 Прогресс", callback_data="profile")
    )
    return m

# --- СТАРТ ---
@bot.message_handler(commands=['start'])
def start(m):
    uid = m.from_user.id

    if uid not in users:
        users[uid] = {
            "level": 1,
            "xp": 0,
            "used": 0,
            "paid": False
        }

    bot.send_message(
        m.chat.id,
        "🎓 Медресе таджвида\n\n"
        "Учись, сдавай экзамены и повышай уровень 📚",
        reply_markup=menu()
    )

# --- CALLBACK ---
@bot.callback_query_handler(func=lambda c: True)
def cb(c):
    uid = c.from_user.id
    user = users[uid]

    if c.data == "lesson":
        lvl = user["level"]
        bot.edit_message_text(
            LESSONS.get(lvl, "📚 Продвинутый уровень"),
            c.message.chat.id,
            c.message.message_id,
            reply_markup=menu()
        )

    elif c.data == "quiz":
        q, _ = QUIZ.get(user["level"], ("Нет вопросов", ""))
        bot.edit_message_text(
            f"❓ {q}",
            c.message.chat.id,
            c.message.message_id
        )
        users[uid]["step"] = "quiz"

    elif c.data == "profile":
        bot.edit_message_text(
            f"📊 Уровень: {user['level']}\nXP: {user['xp']}",
            c.message.chat.id,
            c.message.message_id,
            reply_markup=menu()
        )

    elif c.data == "voice":
        bot.send_message(c.message.chat.id, "🎤 Отправь голос")

# --- ОТВЕТ НА ТЕСТ ---
@bot.message_handler(func=lambda m: users.get(m.from_user.id, {}).get("step") == "quiz")
def quiz_answer(m):
    uid = m.from_user.id
    user = users[uid]

    _, correct = QUIZ.get(user["level"], ("", ""))

    if correct in m.text:
        user["xp"] += 10
        user["level"] += 1
        bot.send_message(m.chat.id, "✅ Верно! Уровень повышен 🔥")
    else:
        bot.send_message(m.chat.id, f"❌ Ошибка. Ответ: {correct}")

    user["step"] = None

# --- ГОЛОС ---
@bot.message_handler(content_types=['voice'])
def voice(m):
    uid = m.from_user.id
    user = users[uid]

    if not user["paid"] and user["used"] >= FREE_LIMIT:
        bot.send_message(m.chat.id, "❌ Лимит. Напиши /buy")
        return

    user["used"] += 1

    bot.send_message(m.chat.id, "🎧 Проверяю...")

    file = bot.get_file(m.voice.file_id)
    audio = bot.download_file(file.file_path)

    with open("voice.ogg", "wb") as f:
        f.write(audio)

    with open("voice.ogg", "rb") as f:
        t = client.audio.transcriptions.create(
            model="gpt-4o-mini-transcribe",
            file=f
        )

    text = t.text

    res = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Коротко найди ошибки таджвида"},
            {"role": "user", "content": text}
        ]
    )

    bot.send_message(m.chat.id,
        f"📖 {text}\n\n🧠 {res.choices[0].message.content}"
    )

# --- ПОКУПКА ---
@bot.message_handler(commands=['buy'])
def buy(m):
    bot.send_message(m.chat.id,
        "💰 Доступ 5€\nНапиши @your_username")

# --- ЗАПУСК ---
print("МЕДРЕСЕ БОТ ЗАПУЩЕН 🚀")
bot.infinity_polling()