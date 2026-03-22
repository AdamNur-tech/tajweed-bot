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
            "letter_index": 0
        }
    return users[user_id]

# ===== AUDIO =====
def generate_audio(text, filename="voice.mp3"):
    tts = gTTS(text=text, lang="ar", slow=True)
    tts.save(filename)
    return filename

# ===== ГЛАВНОЕ МЕНЮ =====
def main_menu(chat_id, user_id):
    user = get_user(user_id)

    text = f"""
┏━━━━━━━━━━━━━━━━━━━━━━┓
        📖 TAJWEED PRO
┗━━━━━━━━━━━━━━━━━━━━━━┛

﷽
خيركم من تعلم القرآن وعلمه

━━━━━━━━━━━━━━━━━━━━━━

👤 Уровень: {user['level']}
⭐ XP: {user['xp']}

━━━━━━━━━━━━━━━━━━━━━━

🚀 Выбери действие:
"""

    markup = InlineKeyboardMarkup(row_width=2)

    markup.add(InlineKeyboardButton("▶️ Продолжить", callback_data="continue"))

    markup.add(
        InlineKeyboardButton("📚 Обучение", callback_data="learn"),
        InlineKeyboardButton("🧠 Практика", callback_data="practice")
    )

    markup.add(
        InlineKeyboardButton("🎯 Заучивание", callback_data="memorize"),
        InlineKeyboardButton("📊 Прогресс", callback_data="progress")
    )

    markup.add(
        InlineKeyboardButton("🤖 AI Учитель", callback_data="ai"),
        InlineKeyboardButton("🎤 Проверка чтения", callback_data="ai_check")
    )

    bot.send_message(chat_id, text, reply_markup=markup)

# ===== ОБУЧЕНИЕ =====
def learn_menu(chat_id, user_id):
    text = """
📚 ОБУЧЕНИЕ

Выбери модуль:

🔤 Алфавит
"""

    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("🔤 Алфавит", callback_data="alphabet"))
    markup.add(InlineKeyboardButton("⬅️ Назад", callback_data="back_main"))

    bot.send_message(chat_id, text, reply_markup=markup)

# ===== АЛФАВИТ =====
def alphabet_lesson(chat_id, user_id):
    user = get_user(user_id)
    letter = letters[user["letter_index"]]
    base = letter["base"]

    # харакаты
    fatha = base + "a"
    damma = base + "u"
    kasra = base + "i"

    text = f"""
🔤 {letter['letter']} — {letter['name']}

📖 Харакаты:

{letter['letter']}َ → {fatha}
{letter['letter']}ُ → {damma}
{letter['letter']}ِ → {kasra}

📌 Чтение:
{fatha} / {damma} / {kasra}

🎧 Нажми слушать
"""

    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(
        InlineKeyboardButton("🔊 Слушать", callback_data="sound_letter"),
        InlineKeyboardButton("➡️ Далее", callback_data="next_letter")
    )
    markup.add(InlineKeyboardButton("⬅️ Назад", callback_data="learn"))

    bot.send_message(chat_id, text, reply_markup=markup)

# ===== START =====
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(
        message.chat.id,
        "🚀 Запуск...",
        reply_markup=ReplyKeyboardRemove()
    )
    main_menu(message.chat.id, message.from_user.id)

# ===== CALLBACK =====
@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    user_id = call.from_user.id
    chat_id = call.message.chat.id
    data = call.data

    user = get_user(user_id)

    if data == "learn":
        learn_menu(chat_id, user_id)

    elif data == "alphabet":
        user["letter_index"] = 0
        alphabet_lesson(chat_id, user_id)

    elif data == "next_letter":
        user["letter_index"] += 1
        if user["letter_index"] < len(letters):
            alphabet_lesson(chat_id, user_id)
        else:
            bot.send_message(chat_id, "🎉 Алфавит завершён!")
            user["letter_index"] = 0

    elif data == "sound_letter":
        letter = letters[user["letter_index"]]["letter"]
        file = generate_audio(letter)
        bot.send_voice(chat_id, open(file, "rb"))

    elif data == "back_main":
        main_menu(chat_id, user_id)

    elif data == "continue":
        bot.send_message(chat_id, "🚀 Продолжение скоро будет")

    elif data == "practice":
        bot.send_message(chat_id, "🧠 Практика скоро будет")

    elif data == "memorize":
        bot.send_message(chat_id, "🎯 Заучивание скоро будет")

    elif data == "progress":
        bot.send_message(chat_id, "📊 Прогресс скоро будет")

    elif data == "ai":
        bot.send_message(chat_id, "🤖 Напиши свой вопрос")

    elif data == "ai_check":
        bot.send_message(chat_id, "🎤 Отправь голос")

# ===== RUN =====
print("🚀 Бот запущен")
bot.polling(none_stop=True)