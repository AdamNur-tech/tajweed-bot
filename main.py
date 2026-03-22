import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import os

BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = telebot.TeleBot(BOT_TOKEN)

# ===== БАЗА ПОЛЬЗОВАТЕЛЕЙ =====
users = {}

def get_user(user_id):
    if user_id not in users:
        users[user_id] = {
            "xp": 0,
            "level": "Новичок",
            "current": "Алфавит → Буква ب",
            "streak": 0,
            "premium": False
        }
    return users[user_id]


# ===== ГЛАВНОЕ МЕНЮ =====
def main_menu(chat_id, user_id):
    user = get_user(user_id)

    text = f"""
📖 Tajweed App

خيركم من تعلم القرآن وعلمه

“Лучший из вас — тот, кто изучает Коран и обучает ему”

✨ Начни путь к правильному чтению Корана

━━━━━━━━━━━━━━━━━━━━━━
👤 Уровень: {user['level']}
⭐ XP: {user['xp']}
🔥 Дней подряд: {user['streak']}

━━━━━━━━━━━━━━━━━━━━━━
📍 Сейчас:
{user['current']}
"""

    markup = InlineKeyboardMarkup(row_width=2)

    markup.add(
        InlineKeyboardButton("▶️ Продолжить", callback_data="continue")
    )

    markup.add(
        InlineKeyboardButton("📖 Обучение", callback_data="learn"),
        InlineKeyboardButton("🧠 Практика", callback_data="practice")
    )

    markup.add(
        InlineKeyboardButton("🎯 Заучивание", callback_data="memorize"),
        InlineKeyboardButton("📊 Прогресс", callback_data="progress")
    )

    markup.add(
        InlineKeyboardButton("🤖 AI Учитель", callback_data="ai")
    )

    bot.send_photo(
        chat_id,
        photo="https://images.unsplash.com/photo-1542816417-0983677f9b6b",
        caption=text,
        reply_markup=markup
    )


# ===== МЕНЮ ОБУЧЕНИЯ =====
def learn_menu(chat_id, user_id):
    text = """
📚 Обучение

Выбери модуль:
"""

    markup = InlineKeyboardMarkup(row_width=2)

    markup.add(
        InlineKeyboardButton("🔤 Алфавит", callback_data="alphabet"),
        InlineKeyboardButton("📘 Основы чтения", callback_data="reading")
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

    bot.send_photo(
        chat_id,
        photo="https://images.unsplash.com/photo-1584551246679-0daf3d275d0f",
        caption=text,
        reply_markup=markup
    )


# ===== START =====
@bot.message_handler(commands=['start'])
def start(message):
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

    elif data == "back_main":
        main_menu(chat_id, user_id)

    elif data == "practice":
        bot.send_message(chat_id, "🧠 Практика (в разработке)")

    elif data == "memorize":
        bot.send_message(chat_id, "🎯 Заучивание (в разработке)")

    elif data == "progress":
        bot.send_message(chat_id, "📊 Прогресс (в разработке)")

    elif data == "ai":
        bot.send_message(chat_id, "🤖 Напиши вопрос")

    elif data == "alphabet":
        bot.send_message(chat_id, "🔤 Алфавит (скоро начнем обучение)")

    elif data == "reading":
        bot.send_message(chat_id, "📘 Основы чтения (скоро)")

    elif data == "tajweed":
        bot.send_message(chat_id, "📚 Таджвид (скоро)")

    elif data == "quran":
        bot.send_message(chat_id, "📖 Коран (скоро)")

    elif data == "ai_check":
        if not user["premium"]:
            bot.send_message(chat_id, """
🎤 Проверка чтения (AI)

Этот раздел будет платным.

💡 Ты сможешь:
• читать голосом  
• получать исправления  
• учиться правильно  

Скоро доступ откроется
""")
        else:
            bot.send_message(chat_id, "🎤 Начни читать...")


# ===== ЗАПУСК =====
print("🚀 Бот запущен")
bot.polling(none_stop=True)
@bot.message_handler(func=lambda message: True)
def handle_all(message):
    if message.text == "/start":
        main_menu(message.chat.id, message.from_user.id)
    else:
        bot.send_message(message.chat.id, "Нажми /start")