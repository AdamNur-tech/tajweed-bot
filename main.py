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
    {"letter": "ا", "name": "Алиф", "base": "", "makhraj": "горло (без преграды)"},
    {"letter": "ب", "name": "Ба", "base": "b", "makhraj": "губы"},
    {"letter": "ت", "name": "Та", "base": "t", "makhraj": "кончик языка + зубы"},
    {"letter": "ث", "name": "Са", "base": "th", "makhraj": "между зубами"},
    {"letter": "ج", "name": "Джим", "base": "j", "makhraj": "середина языка"},
    {"letter": "ح", "name": "Ха", "base": "ḥ", "makhraj": "середина горла"},
    {"letter": "خ", "name": "Ха (глуб.)", "base": "kh", "makhraj": "верх горла"},
    {"letter": "د", "name": "Даль", "base": "d", "makhraj": "кончик языка"},
    {"letter": "ذ", "name": "Заль", "base": "dh", "makhraj": "между зубами"},
    {"letter": "ر", "name": "Ра", "base": "r", "makhraj": "кончик языка"},
    {"letter": "ز", "name": "Зай", "base": "z", "makhraj": "зубы"},
    {"letter": "س", "name": "Син", "base": "s", "makhraj": "зубы"},
    {"letter": "ش", "name": "Шин", "base": "sh", "makhraj": "середина языка"},
    {"letter": "ص", "name": "Сад", "base": "ṣ", "makhraj": "зубы (твердо)"},
    {"letter": "ض", "name": "Дад", "base": "ḍ", "makhraj": "бок языка"},
    {"letter": "ط", "name": "Та (тв.)", "base": "ṭ", "makhraj": "кончик языка (твердо)"},
    {"letter": "ظ", "name": "За (тв.)", "base": "ẓ", "makhraj": "между зубами (твердо)"},
    {"letter": "ع", "name": "Айн", "base": "ʿ", "makhraj": "глубина горла"},
    {"letter": "غ", "name": "Гайн", "base": "gh", "makhraj": "верх горла"},
    {"letter": "ف", "name": "Фа", "base": "f", "makhraj": "губы + зубы"},
    {"letter": "ق", "name": "Каф (глуб.)", "base": "q", "makhraj": "глубина языка"},
    {"letter": "ك", "name": "Каф", "base": "k", "makhraj": "язык"},
    {"letter": "ل", "name": "Лям", "base": "l", "makhraj": "язык"},
    {"letter": "م", "name": "Мим", "base": "m", "makhraj": "губы"},
    {"letter": "ن", "name": "Нун", "base": "n", "makhraj": "язык + нос"},
    {"letter": "ه", "name": "Ха", "base": "h", "makhraj": "горло"},
    {"letter": "و", "name": "Вау", "base": "w", "makhraj": "губы"},
    {"letter": "ي", "name": "Я", "base": "y", "makhraj": "середина языка"},
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
    markup.add(InlineKeyboardButton("📚 Обучение", callback_data="learn"))
    bot.send_message(chat_id, text, reply_markup=markup)

# ===== ОБУЧЕНИЕ =====
def learn_menu(chat_id):
    text = """
📚 ОБУЧЕНИЕ

🔤 Алфавит
"""
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("🔤 Алфавит", callback_data="alphabet"))
    markup.add(InlineKeyboardButton("⬅️ Назад", callback_data="back_main"))
    bot.send_message(chat_id, text, reply_markup=markup)

# ===== УРОК =====
def alphabet_lesson(chat_id, user_id):
    user = get_user(user_id)
    letter = letters[user["letter_index"]]
    base = letter["base"]

    fatha = base + "a"
    damma = base + "u"
    kasra = base + "i"

    text = f"""
🔤 {letter['letter']} — {letter['name']}

📍 Махрадж:
{letter['makhraj']}

📖 Харакаты:

{letter['letter']}َ → {fatha}
{letter['letter']}ُ → {damma}
{letter['letter']}ِ → {kasra}

📚 Слоги:

{fatha} / {damma} / {kasra}

🎧 Слушай и повторяй
"""

    markup = InlineKeyboardMarkup()
    markup.add(
        InlineKeyboardButton("🔊 Слушать", callback_data="sound"),
        InlineKeyboardButton("➡️ Далее", callback_data="next")
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
        learn_menu(chat_id)

    elif data == "alphabet":
        user["letter_index"] = 0
        alphabet_lesson(chat_id, user_id)

    elif data == "next":
        user["letter_index"] += 1
        if user["letter_index"] < len(letters):
            alphabet_lesson(chat_id, user_id)
        else:
            bot.send_message(chat_id, "🎉 Алфавит завершён!")
            user["letter_index"] = 0

    elif data == "sound":
        letter = letters[user["letter_index"]]["letter"]
        file = generate_audio(letter)
        audio = open(file, "rb")
        bot.send_voice(chat_id, audio)

    elif data == "back_main":
        main_menu(chat_id, user_id)

# ===== RUN =====
print("🚀 Бот запущен")
bot.polling(none_stop=True)