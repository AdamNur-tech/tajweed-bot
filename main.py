import os
import telebot
from telebot.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    ReplyKeyboardRemove
)
from gtts import gTTS

# ===== CONFIG =====
BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN)

users = {}

# ===== АЛФАВИТ =====
letters = [
    {"letter": "ا", "name": "Алиф", "base": ""},
    {"letter": "ب", "name": "Ба", "base": "b"},
    {"letter": "ت", "name": "Та", "base": "t"},
    {"letter": "ث", "name": "Са", "base": "th"},
    {"letter": "ج", "name": "Джим", "base": "j"},
    {"letter": "ح", "name": "Ха", "base": "ḥ"},
    {"letter": "خ", "name": "Ха (глуб.)", "base": "kh"},
    {"letter": "د", "name": "Даль", "base": "d"},
    {"letter": "ذ", "name": "Заль", "base": "dh"},
    {"letter": "ر", "name": "Ра", "base": "r"},
    {"letter": "ز", "name": "Зай", "base": "z"},
    {"letter": "س", "name": "Син", "base": "s"},
    {"letter": "ش", "name": "Шин", "base": "sh"},
    {"letter": "ص", "name": "Сад", "base": "ṣ"},
    {"letter": "ض", "name": "Дад", "base": "ḍ"},
    {"letter": "ط", "name": "Та (тв.)", "base": "ṭ"},
    {"letter": "ظ", "name": "За (тв.)", "base": "ẓ"},
    {"letter": "ع", "name": "Айн", "base": "ʿ"},
    {"letter": "غ", "name": "Гайн", "base": "gh"},
    {"letter": "ف", "name": "Фа", "base": "f"},
    {"letter": "ق", "name": "Каф (глуб.)", "base": "q"},
    {"letter": "ك", "name": "Каф", "base": "k"},
    {"letter": "ل", "name": "Лям", "base": "l"},
    {"letter": "م", "name": "Мим", "base": "m"},
    {"letter": "ن", "name": "Нун", "base": "n"},
    {"letter": "ه", "name": "Ха", "base": "h"},
    {"letter": "و", "name": "Вау", "base": "w"},
    {"letter": "ي", "name": "Я", "base": "y"},
]

# ===== USER =====
def get_user(user_id):
    if user_id not in users:
        users[user_id] = {
            "level": "Новичок",
            "xp": 0,
            "streak": 0,
            "current": "Алфавит",
            "premium": False,
            "step": 0,
            "letter_index": 0
        }
    return users[user_id]

# ===== AUDIO =====
def generate_audio(text, filename="voice.mp3"):
    tts = gTTS(text=text, lang="ar")
    tts.save(filename)
    return filename

# ===== ГЛАВНОЕ МЕНЮ =====
def main_menu(chat_id, user_id):
    user = get_user(user_id)

    text = f"""
📖 TAJWEED PRO

👤 Уровень: {user['level']}
⭐ XP: {user['xp']}

🚀 Выбери действие:
"""

    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(InlineKeyboardButton("▶️ Продолжить", callback_data="continue"))
    markup.add(
        InlineKeyboardButton("📚 Обучение", callback_data="learn"),
        InlineKeyboardButton("🧠 Практика", callback_data="practice")
    )

    bot.send_message(chat_id, text, reply_markup=markup)

# ===== ОБУЧЕНИЕ =====
def learn_menu(chat_id, user_id):
    text = "📚 Обучение\n\n🔤 Алфавит"
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("🔤 Алфавит", callback_data="alphabet"))
    markup.add(InlineKeyboardButton("⬅️ Назад", callback_data="back_main"))
    bot.send_message(chat_id, text, reply_markup=markup)

# ===== УРОК =====
def alphabet_lesson(chat_id, user_id):
    user = get_user(user_id)
    step = user["step"]
    letter_data = letters[user["letter_index"]]

    letter = letter_data["letter"]
    name = letter_data["name"]
    base = letter_data["base"]

    fatha = base + "a"
    damma = base + "u"
    kasra = base + "i"

    if step == 0:
        text = f"""
🔤 ШАГ 1

Буква: {letter}
Название: {name}
"""

    elif step == 1:
        text = f"""
🗣 ШАГ 2

Звук: {fatha}
"""

    elif step == 2:
        text = f"""
📖 ШАГ 3

{letter}َ → {fatha}
{letter}ُ → {damma}
{letter}ِ → {kasra}

{fatha} / {damma} / {kasra}
"""

    elif step == 3:
        text = f"""
🎯 ШАГ 4

Как читается:

{letter}
"""

    markup = InlineKeyboardMarkup()

    if step == 1:
        markup.add(InlineKeyboardButton("🔊 Слушать", callback_data="sound"))

    if step < 3:
        markup.add(InlineKeyboardButton("➡️ Далее", callback_data="next"))
    else:
        markup.add(
            InlineKeyboardButton(fatha, callback_data="correct"),
            InlineKeyboardButton("ошибка", callback_data="wrong")
        )

    bot.send_message(chat_id, text, reply_markup=markup)

# ===== CALLBACK =====
@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    user = get_user(call.from_user.id)
    chat_id = call.message.chat.id

    if call.data == "learn":
        learn_menu(chat_id, call.from_user.id)

    elif call.data == "alphabet":
        user["step"] = 0
        user["letter_index"] = 0
        alphabet_lesson(chat_id, call.from_user.id)

    elif call.data == "next":
        user["step"] += 1
        if user["step"] > 3:
            user["step"] = 0
            user["letter_index"] += 1
        alphabet_lesson(chat_id, call.from_user.id)

    elif call.data == "sound":
        letter = letters[user["letter_index"]]["letter"]
        bot.send_voice(chat_id, open(generate_audio(letter), "rb"))

    elif call.data == "correct":
        bot.send_message(chat_id, "✅ Правильно")
        user["step"] = 0
        user["letter_index"] += 1
        alphabet_lesson(chat_id, call.from_user.id)

    elif call.data == "wrong":
        bot.send_message(chat_id, "❌ Ошибка")
        alphabet_lesson(chat_id, call.from_user.id)

# ===== START =====
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "🚀 Запуск...", reply_markup=ReplyKeyboardRemove())
    main_menu(message.chat.id, message.from_user.id)

# ===== RUN =====
print("🚀 Бот запущен")
bot.polling(none_stop=True)