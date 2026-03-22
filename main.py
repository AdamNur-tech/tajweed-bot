import os
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardRemove
from gtts import gTTS

BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN)

users = {}

# ===== ПОЛНЫЙ АЛФАВИТ =====
letters = [
    {"letter": "ا", "name": "Алиф", "correct": "А"},
    {"letter": "ب", "name": "Ба", "correct": "Б"},
    {"letter": "ت", "name": "Та", "correct": "Т"},
    {"letter": "ث", "name": "Са", "correct": "С"},
    {"letter": "ج", "name": "Джим", "correct": "Д"},
    {"letter": "ح", "name": "Ха", "correct": "Х"},
    {"letter": "خ", "name": "Ха (глубокое)", "correct": "Х"},
    {"letter": "د", "name": "Даль", "correct": "Д"},
    {"letter": "ذ", "name": "Заль", "correct": "З"},
    {"letter": "ر", "name": "Ра", "correct": "Р"},
    {"letter": "ز", "name": "Зай", "correct": "З"},
    {"letter": "س", "name": "Син", "correct": "С"},
    {"letter": "ش", "name": "Шин", "correct": "Ш"},
    {"letter": "ص", "name": "Сад", "correct": "С"},
    {"letter": "ض", "name": "Дад", "correct": "Д"},
    {"letter": "ط", "name": "Та (твердая)", "correct": "Т"},
    {"letter": "ظ", "name": "За (твердая)", "correct": "З"},
    {"letter": "ع", "name": "Айн", "correct": "А"},
    {"letter": "غ", "name": "Гайн", "correct": "Г"},
    {"letter": "ف", "name": "Фа", "correct": "Ф"},
    {"letter": "ق", "name": "Каф", "correct": "К"},
    {"letter": "ك", "name": "Кяф", "correct": "К"},
    {"letter": "ل", "name": "Лям", "correct": "Л"},
    {"letter": "م", "name": "Мим", "correct": "М"},
    {"letter": "ن", "name": "Нун", "correct": "Н"},
    {"letter": "ه", "name": "Ха", "correct": "Х"},
    {"letter": "و", "name": "Вау", "correct": "У"},
    {"letter": "ي", "name": "Я", "correct": "И"},
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
    tts = gTTS(text=text, lang="ar")
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
        text = f"{bar}\n\n🔤 {letter['letter']}\n\n{letter['name']}"
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("Далее ➡️", callback_data="next"))

    elif step == 1:
        text = f"{bar}\n\n🗣 Произношение\n\nЗвук: {letter['correct']}"
        markup = InlineKeyboardMarkup()
        markup.add(
            InlineKeyboardButton("🔊 Слушать", callback_data="sound"),
            InlineKeyboardButton("Далее ➡️", callback_data="next")
        )

    elif step == 2:
        text = f"{bar}\n\n📖 Пример\n\n{letter['letter']}َ {letter['letter']}ُ {letter['letter']}ِ"
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("Далее ➡️", callback_data="next"))

    elif step == 3:
        text = f"{bar}\n\n🎯 Тест\n\nКак читается:\n\n{letter['letter']}"
        markup = InlineKeyboardMarkup(row_width=2)
        markup.add(
            InlineKeyboardButton("А", callback_data="A"),
            InlineKeyboardButton("Б", callback_data="B"),
            InlineKeyboardButton("Т", callback_data="T"),
            InlineKeyboardButton("С", callback_data="S"),
            InlineKeyboardButton("М", callback_data="M"),
        )

    if message_id:
        bot.edit_message_text(text, chat_id, message_id, reply_markup=markup)
    else:
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

    elif data in ["A","B","T","S","M"]:
        correct = letters[user["level"]]["correct"]

        if data == correct:
            user["xp"] += 10
            bot.answer_callback_query(call.id, "✅ Правильно!")

            user["level"] += 1
            user["step"] = 0

            if user["level"] >= len(letters):
                bot.send_message(chat_id, "🎉 Ты прошёл весь алфавит!")
            else:
                msg_id = lesson(chat_id, user_id)
                user["lesson_msg"] = msg_id
        else:
            bot.answer_callback_query(call.id, "❌ Ошибка")

# ===== RUN =====
print("🚀 BOT STARTED")
bot.polling(none_stop=True)