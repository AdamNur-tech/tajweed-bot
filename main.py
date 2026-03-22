import os
import telebot
from telebot.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    ReplyKeyboardRemove
)

# ===== CONFIG =====
BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN)

users = {}

# ===== USER =====
def get_user(user_id):
    if user_id not in users:
        users[user_id] = {
            "level": "Новичок",
            "xp": 0,
            "streak": 0,
            "current": "Алфавит → Буква ا (Алиф)",
            "premium": False
        }
    return users[user_id]

# ===== ГЛАВНОЕ МЕНЮ =====
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

    markup.add(
        InlineKeyboardButton("▶️ Продолжить", callback_data="continue")
    )

    markup.add(
        InlineKeyboardButton("📚 Обучение", callback_data="learn"),
        InlineKeyboardButton("🧠 Практика", callback_data="practice")
    )

    markup.add(
        InlineKeyboardButton("🎯 Заучивание", callback_data="memorize"),
        InlineKeyboardButton("📊 Прогресс", callback_data="progress")
    )

    markup.add(
        InlineKeyboardButton("🤖 AI Учитель", callback_data="ai")
    )

    bot.send_message(chat_id, text, reply_markup=markup)

# ===== МЕНЮ ОБУЧЕНИЯ =====
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

    markup.add(
        InlineKeyboardButton("⬅️ Назад", callback_data="back_main")
    )

    bot.send_message(chat_id, text, reply_markup=markup)

# ===== START =====
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(
        message.chat.id,
        "♻️ Обновляем интерфейс...",
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

    if data == "continue":
        bot.send_message(chat_id, "🚀 Продолжаем обучение...")

    elif data == "learn":
        learn_menu(chat_id, user_id)

    elif data == "practice":
        bot.send_message(chat_id, "🧠 Практика скоро появится")

    elif data == "memorize":
        bot.send_message(chat_id, "🎯 Заучивание скоро появится")

    elif data == "progress":
        bot.send_message(chat_id, "📊 Прогресс скоро появится")

    elif data == "ai":
        bot.send_message(chat_id, "🤖 Напиши свой вопрос")

    elif data == "alphabet":
        alphabet_lesson(chat_id)

    elif data == "reading":
        bot.send_message(chat_id, "📖 Основы чтения скоро")

    elif data == "tajweed":
        bot.send_message(chat_id, "📚 Таджвид скоро")

    elif data == "quran":
        bot.send_message(chat_id, "📖 Коран скоро")

    elif data == "ai_check":
        if not user["premium"]:
            bot.send_message(chat_id, """
🎤 Проверка чтения (AI)

Этот раздел будет платным.

Скоро откроется.
""")
        else:
            bot.send_message(chat_id, "🎤 Начни читать...")

    elif data == "back_main":
        main_menu(chat_id, user_id)

# ===== УРОК АЛИФ =====
def alphabet_lesson(chat_id):
    text = """
┏━━━━━━━━━━━━━━━━━━━━━━┓
        🔤 УРОК: АЛИФ
┗━━━━━━━━━━━━━━━━━━━━━━┛

📌 Буква: ا

🗣 Произношение:
"А" — открытый звук

📖 Как читать:
ا = а

📍 Примеры:

اَ — а  
اُ — у  
اِ — и  

📘 Слово:
أَبَ — аба (отец)

━━━━━━━━━━━━━━━━━━━━━━

🎯 Попробуй:
Как читается "ا"?
"""

    markup = InlineKeyboardMarkup()
    markup.add(
        InlineKeyboardButton("А", callback_data="correct"),
        InlineKeyboardButton("Б", callback_data="wrong")
    )

    bot.send_message(chat_id, text, reply_markup=markup)

# ===== ОТВЕТЫ =====
@bot.callback_query_handler(func=lambda call: call.data in ["correct", "wrong"])
def answers(call):
    if call.data == "correct":
        bot.send_message(call.message.chat.id, "✅ Правильно!")
    else:
        bot.send_message(call.message.chat.id, "❌ Неправильно. Это звук 'А'")

# ===== ЗАПУСК =====
print("🚀 Бот запущен")
bot.polling(none_stop=True)