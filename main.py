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
    {"letter": "ا", "name": "Алиф", "base": "", "makhraj": "глубокое горло"},
    {"letter": "ب", "name": "Ба", "base": "b", "makhraj": "губы"},
    {"letter": "ت", "name": "Та", "base": "t", "makhraj": "кончик языка"},
    {"letter": "ث", "name": "Са", "base": "th", "makhraj": "между зубами"},
    {"letter": "ج", "name": "Джим", "base": "j", "makhraj": "середина языка"},
    {"letter": "ح", "name": "Ха", "base": "ḥ", "makhraj": "середина горла"},
    {"letter": "خ", "name": "Ха (глуб.)", "base": "kh", "makhraj": "верх горла"},
    {"letter": "د", "name": "Даль", "base": "d", "makhraj": "кончик языка"},
    {"letter": "ذ", "name": "Заль", "base": "dh", "makhraj": "между зубами"},
    {"letter": "ر", "name": "Ра", "base": "r", "makhraj": "кончик языка"},
    {"letter": "ز", "name": "Зай", "base": "z", "makhraj": "перед языка"},
    {"letter": "س", "name": "Син", "base": "s", "makhraj": "перед языка"},
    {"letter": "ش", "name": "Шин", "base": "sh", "makhraj": "середина языка"},
    {"letter": "ص", "name": "Сад", "base": "ṣ", "makhraj": "твёрдый язык"},
    {"letter": "ض", "name": "Дад", "base": "ḍ", "makhraj": "бок языка"},
    {"letter": "ط", "name": "Та (тв.)", "base": "ṭ", "makhraj": "твёрдый кончик"},
    {"letter": "ظ", "name": "За", "base": "ẓ", "makhraj": "между зубами"},
    {"letter": "ع", "name": "Айн", "base": "ʿ", "makhraj": "глубокое горло"},
    {"letter": "غ", "name": "Гайн", "base": "gh", "makhraj": "верх горла"},
    {"letter": "ف", "name": "Фа", "base": "f", "makhraj": "губа+зубы"},
    {"letter": "ق", "name": "Каф", "base": "q", "makhraj": "зад языка"},
    {"letter": "ك", "name": "Каф", "base": "k", "makhraj": "зад языка"},
    {"letter": "ل", "name": "Лям", "base": "l", "makhraj": "кончик языка"},
    {"letter": "م", "name": "Мим", "base": "m", "makhraj": "губы"},
    {"letter": "ن", "name": "Нун", "base": "n", "makhraj": "нос+язык"},
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
            "current": "Алфавит → Буква ا (Алиф)",
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

# ===== ГЛАВНОЕ МЕНЮ (НЕ ТРОГАЛ) =====
def main_menu(chat_id, user_id):
    user = get_user(user_id)

    text = f"""
┏━━━━━━━━━━━━━━━━━━━━━━┓
        📖 TAJWEED PRO
┗━━━━━━━━━━━━━━━━━━━━━━┛

﷽
خيركم من تعلم القرآن وعلمه

«Лучший из вас — тот,
кто изучает Коран и обучает ему»

━━━━━━━━━━━━━━━━━━━━━━

✨ Начни путь к правильному чтению Корана

━━━━━━━━━━━━━━━━━━━━━━

👤 Уровень: {user['level']}
⭐ XP: {user['xp']}
🔥 Серия: {user['streak']} дней

━━━━━━━━━━━━━━━━━━━━━━

📍 Текущий урок:
🔤 {user['current']}

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
    markup.add(InlineKeyboardButton("🤖 AI Учитель", callback_data="ai"))

    bot.send_message(chat_id, text, reply_markup=markup)

# ===== МЕНЮ ОБУЧЕНИЯ (НЕ ТРОГАЛ) =====
def learn_menu(chat_id, user_id):
    text = """
┏━━━━━━━━━━━━━━━━━━━━━━┓
        📚 ОБУЧЕНИЕ
┗━━━━━━━━━━━━━━━━━━━━━━┛

Выбери модуль:

🔤 Алфавит — буквы и звуки  
📖 Основы — чтение слов  
📚 Таджвид — правила  
📖 Коран — практика  

━━━━━━━━━━━━━━━━━━━━━━
"""

    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(
        InlineKeyboardButton("🔤 Алфавит", callback_data="alphabet"),
        InlineKeyboardButton("📖 Основы", callback_data="reading")
    )
    markup.add(
        InlineKeyboardButton("📚 Таджвид", callback_data="tajweed"),
        InlineKeyboardButton("📖 Коран", callback_data="quran")
    )
    markup.add(
        InlineKeyboardButton("🎤 Проверка чтения (AI)", callback_data="ai_check")
    )
    markup.add(InlineKeyboardButton("⬅️ Назад", callback_data="back_main"))

    bot.send_message(chat_id, text, reply_markup=markup)

# ===== АЛФАВИТ =====
def alphabet_lesson(chat_id, user_id):
    user = get_user(user_id)
    step = user["step"]
    data = letters[user["letter_index"]]

    l = data["letter"]
    base = data["base"]

    fatha = base + "a"
    damma = base + "u"
    kasra = base + "i"

    if step == 0:
        text = f"🔤 {l}\n{data['name']}"

    elif step == 1:
        text = f"🗣 Звук: {fatha}"

    elif step == 2:
        text = f"📍 Махрадж:\n{data['makhraj']}"

    elif step == 3:
        text = f"""
📖 Харакаты:

{l}َ → {fatha}
{l}ُ → {damma}
{l}ِ → {kasra}
"""

    elif step == 4:
        text = f"🎯 Как читается:\n{l}"

    markup = InlineKeyboardMarkup()

    if step == 1:
        markup.add(InlineKeyboardButton("🔊 Слушать", callback_data="sound"))

    if step < 4:
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
        if user["step"] > 4:
            user["step"] = 0
            user["letter_index"] += 1
        alphabet_lesson(chat_id, call.from_user.id)

    elif call.data == "sound":
        l = letters[user["letter_index"]]["letter"]
        bot.send_voice(chat_id, open(generate_audio(l), "rb"))

    elif call.data == "correct":
        bot.send_message(chat_id, "✅ Правильно")
        user["step"] = 0
        user["letter_index"] += 1
        alphabet_lesson(chat_id, call.from_user.id)

    elif call.data == "wrong":
        bot.send_message(chat_id, "❌ Ошибка")
        alphabet_lesson(chat_id, call.from_user.id)

    elif call.data == "back_main":
        main_menu(chat_id, call.from_user.id)

# ===== START =====
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "🚀 Запуск...", reply_markup=ReplyKeyboardRemove())
    main_menu(message.chat.id, message.from_user.id)

print("🚀 Бот запущен")
bot.polling(none_stop=True)