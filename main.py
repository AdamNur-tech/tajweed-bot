import os
import telebot
from telebot.types import ReplyKeyboardMarkup
from openai import OpenAI

BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

bot = telebot.TeleBot(BOT_TOKEN)
client = OpenAI(api_key=OPENAI_API_KEY)

users = {}

FREE_LIMIT = 3

# --- УРОКИ ПО УРОВНЯМ ---
LESSONS = {
1: "📚 Алиф Ба Та:\nا ب ت\nПовтори вслух",
2: "📚 Все буквы:\nا ب ت ث ج ح خ د ...",
3: "📚 Формы букв:\nب بـ ـبـ ـب",
4: "📚 Фатха:\nبَ = БА",
5: "📚 Касра:\nبِ = БИ",
6: "📚 Дамма:\nبُ = БУ",
7: "📚 Сукун:\nبْ",
8: "📚 Танвин:\nً ٍ ٌ",
9: "📚 Чтение:\nبَتَ = БАТА",
10: "📚 Нун сакина:\n4 правила",
11: "📚 Мим сакина:\n3 правила",
12: "📚 Мадд:\n2 хараката",
13: "📚 Калькаля:\nق ط ب ج د",
14: "📚 Толстые буквы:\nص ض ط ظ",
15: "📚 Ра и Лям",
16: "📚 Вакф (остановка)",
17: "📚 Ошибки таджвида"
}

# --- ТЕСТЫ ---
QUIZ = {
1: ("Какая буква это: ا ?", "алиф"),
4: ("Как читается بَ ?", "ба"),
10: ("Сколько правил у нун сакина?", "4"),
12: ("Сколько харакат у мадда?", "2"),
}

# --- МЕНЮ ---
def menu():
    m = ReplyKeyboardMarkup(resize_keyboard=True)
    m.add("📚 Урок", "🧠 Тест")
    m.add("🎤 Практика", "📊 Прогресс")
    return m

# --- СТАРТ ---
@bot.message_handler(commands=['start'])
def start(m):
    uid = m.from_user.id

    if uid not in users:
        users[uid] = {
            "level": 1,
            "xp": 0,
            "step": None,
            "used": 0
        }

    bot.send_message(m.chat.id,
        "🎓 Медресе таджвида\n\n"
        "Ты начинаешь с нуля и дойдёшь до уровня кари 📖\n\n"
        "Выбери:",
        reply_markup=menu())

# --- УРОК ---
@bot.message_handler(func=lambda m: m.text == "📚 Урок")
def lesson(m):
    user = users[m.chat.id]
    lvl = user["level"]

    bot.send_message(m.chat.id, LESSONS.get(lvl, "🎓 Ты прошёл курс!"))

# --- ТЕСТ ---
@bot.message_handler(func=lambda m: m.text == "🧠 Тест")
def quiz(m):
    user = users[m.chat.id]
    lvl = user["level"]

    if lvl not in QUIZ:
        bot.send_message(m.chat.id, "📚 Сначала изучи урок")
        return

    q, _ = QUIZ[lvl]
    users[m.chat.id]["step"] = "quiz"

    bot.send_message(m.chat.id, f"❓ {q}")

@bot.message_handler(func=lambda m: users.get(m.chat.id, {}).get("step") == "quiz")
def answer(m):
    user = users[m.chat.id]
    lvl = user["level"]

    _, correct = QUIZ.get(lvl, ("", ""))

    if correct in m.text.lower():
        user["xp"] += 10
        user["level"] += 1
        bot.send_message(m.chat.id, "✅ Верно! Уровень повышен 🔥")
    else:
        bot.send_message(m.chat.id, f"❌ Неправильно. Ответ: {correct}")

    user["step"] = None

# --- ГОЛОС ---
@bot.message_handler(content_types=['voice'])
def voice(m):
    uid = m.from_user.id
    user = users[uid]

    if user["used"] >= FREE_LIMIT:
        bot.send_message(m.chat.id, "❌ Лимит. Напиши /buy")
        return

    user["used"] += 1

    bot.send_message(m.chat.id, "🎧 Проверяю чтение...")

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
            {"role":"system","content":
             "Ты учитель таджвида. Найди ошибки и дай совет"},
            {"role":"user","content":text}
        ]
    )

    bot.send_message(m.chat.id,
        f"📖 {text}\n\n🧠 {res.choices[0].message.content}"
    )

# --- ПРОГРЕСС ---
@bot.message_handler(func=lambda m: m.text == "📊 Прогресс")
def progress(m):
    user = users[m.chat.id]

    bot.send_message(m.chat.id,
        f"📊 Уровень: {user['level']}\nXP: {user['xp']}")

# --- ПОКУПКА ---
@bot.message_handler(commands=['buy'])
def buy(m):
    bot.send_message(m.chat.id,
        "💰 Доступ без лимита — 5€\nНапиши @your_username")

# --- ЗАПУСК ---
print("БОТ МЕДРЕСЕ ЗАПУЩЕН 🚀")
bot.infinity_polling()