import os
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardRemove
from gtts import gTTS

BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN)

users = {}

# ===== АЛФАВИТ (ПРАВИЛЬНЫЙ) =====
letters = [
    {"letter": "ا", "name": "Алиф", "sound": "a", "makhraj": "из горла (без контакта)"},
    {"letter": "ب", "name": "Ба", "sound": "ba", "makhraj": "губы"},
    {"letter": "ت", "name": "Та", "sound": "ta", "makhraj": "кончик языка + зубы"},
    {"letter": "ث", "name": "Са", "sound": "tha", "makhraj": "язык между зубами"},
    {"letter": "ج", "name": "Джим", "sound": "ja", "makhraj": "середина языка"},
    {"letter": "ح", "name": "Ха", "sound": "ḥa", "makhraj": "середина горла"},
    {"letter": "خ", "name": "Ха (глубокое)", "sound": "kha", "makhraj": "верх горла"},
    {"letter": "د", "name": "Даль", "sound": "da", "makhraj": "кончик языка"},
    {"letter": "ذ", "name": "Заль", "sound": "dha", "makhraj": "между зубами"},
    {"letter": "ر", "name": "Ра", "sound": "ra", "makhraj": "кончик языка"},
    {"letter": "ز", "name": "Зай", "sound": "za", "makhraj": "зубы"},
    {"letter": "س", "name": "Син", "sound": "sa", "makhraj": "зубы"},
    {"letter": "ش", "name": "Шин", "sound": "sha", "makhraj": "середина языка"},
    {"letter": "ص", "name": "Сад", "sound": "ṣa", "makhraj": "зубы (твердо)"},
    {"letter": "ض", "name": "Дад", "sound": "ḍa", "makhraj": "бок языка"},
    {"letter": "ط", "name": "Та (твердая)", "sound": "ṭa", "makhraj": "кончик языка (твердо)"},
    {"letter": "ظ", "name": "За (твердая)", "sound": "ẓa", "makhraj": "между зубами (твердо)"},
    {"letter": "ع", "name": "Айн", "sound": "ʿa", "makhraj": "глубина горла"},
    {"letter": "غ", "name": "Гайн", "sound": "gha", "makhraj": "верх горла"},
    {"letter": "ف", "name": "Фа", "sound": "fa", "makhraj": "губы + зубы"},
    {"letter": "ق", "name": "Каф (глубокая)", "sound": "qa", "makhraj": "глубина языка"},
    {"letter": "ك", "name": "Каф", "sound": "ka", "makhraj": "язык"},
    {"letter": "ل", "name": "Лям", "sound": "la", "makhraj": "язык"},
    {"letter": "م", "name": "Мим", "sound": "ma", "makhraj": "губы"},
    {"letter": "ن", "name": "Нун", "sound": "na", "makhraj": "язык + нос"},
    {"letter": "ه", "name": "Ха", "sound": "ha", "makhraj": "горло"},
    {"letter": "و", "name": "Вау", "sound": "wa", "makhraj": "губы"},
    {"letter": "ي", "name": "Я", "sound": "ya", "makhraj": "середина языка"},
]

# ===== USER =====
def get_user(user_id):
    if user_id not in users:
        users[user_id] = {
            "level": 0,
            "xp": 0,
            "step": 0,
            "lesson_msg": None
        }
    return users[user_id]

# ===== AUDIO =====
def generate_audio(text):
    tts = gTTS(text=text, lang="ar", slow=True)
    tts.save("voice.mp3")
    return "voice.mp3"

# ===== ПРОГРЕСС =====
def progress_bar(step):
    total = 4
    return "🟩" * step + "⬜" * (total - step)

# ===== МЕНЮ =====
def main_menu(chat_id, user_id):
    user = get_user(user_id)

    text = f"""
📖 TAJWEED PRO

خيركم من تعلم القرآن وعلمه

👤 Уровень: {user['level']+1}/{len(letters)}
⭐ XP: {user['xp']}

🚀 Начни обучение
"""

    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("▶️ Начать", callback_data="start"))

    bot.send_message(chat_id, text, reply_markup=markup)

# ===== УРОК =====
def lesson(chat_id, user_id, message_id=None):
    user = get_user(user_id)
    letter = letters[user["level"]]
    step = user["step"]
    bar = progress_bar(step)

    if step == 0:
        text = f"""
{bar}

🔤 БУКВА: {letter['letter']}

Название: {letter['name']}

📌 Чтение: {letter['sound']}
"""
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("Далее ➡️", callback_data="next"))

    elif step == 1:
        text = f"""
{bar}

🗣 ПРОИЗНОШЕНИЕ

Звук: {letter['sound']}

📍 Махрадж:
{letter['makhraj']}

❌ не искажай звук
"""
        markup = InlineKeyboardMarkup()
        markup.add(
            InlineKeyboardButton("🔊 Слушать", callback_data="sound"),
            InlineKeyboardButton("Далее ➡️", callback_data="next")
        )

    elif step == 2:
        text = f"""
{bar}

📖 ПРИМЕРЫ

{letter['letter']}َ  
{letter['letter']}ُ  
{letter['letter']}ِ  

👉 тренируй короткие звуки
"""
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("Далее ➡️", callback_data="next"))

    elif step == 3:
        correct = letter["sound"]

        text = f"""
{bar}

🎯 ТЕСТ

Как читается:

{letter['letter']}
"""
        markup = InlineKeyboardMarkup(row_width=2)
        markup.add(
            InlineKeyboardButton(correct, callback_data="correct"),
            InlineKeyboardButton("ba", callback_data="wrong"),
            InlineKeyboardButton("ta", callback_data="wrong"),
            InlineKeyboardButton("sa", callback_data="wrong"),
        )

    try:
        if message_id:
            bot.edit_message_text(text, chat_id, message_id, reply_markup=markup)
        else:
            msg = bot.send_message(chat_id, text, reply_markup=markup)
            return msg.message_id
    except:
        msg = bot.send_message(chat_id, text, reply_markup=markup)
        return msg.message_id

# ===== START =====
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "♻️ Загрузка...", reply_markup=ReplyKeyboardRemove())
    main_menu(message.chat.id, message.from_user.id)

# ===== CALLBACK =====
@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    user_id = call.from_user.id
    chat_id = call.message.chat.id
    data = call.data

    user = get_user(user_id)

    if data == "start":
        user["step"] = 0
        msg_id = lesson(chat_id, user_id)
        user["lesson_msg"] = msg_id

    elif data == "next":
        user["step"] += 1
        lesson(chat_id, user_id, user["lesson_msg"])

    elif data == "sound":
        letter = letters[user["level"]]
        file = generate_audio(letter["letter"])
        audio = open(file, "rb")
        bot.send_voice(chat_id, audio)

    elif data == "correct":
        user["xp"] += 10
        bot.answer_callback_query(call.id, "✅ Правильно!")

        user["level"] += 1
        user["step"] = 0

        if user["level"] >= len(letters):
            bot.send_message(chat_id, "🎉 Ты прошёл алфавит!")
        else:
            msg_id = lesson(chat_id, user_id)
            user["lesson_msg"] = msg_id

    elif data == "wrong":
        bot.answer_callback_query(call.id, "❌ Ошибка")

# ===== RUN =====
print("🚀 BOT STARTED")
bot.polling(none_stop=True)