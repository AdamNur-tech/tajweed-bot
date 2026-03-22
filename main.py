import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import os

BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = telebot.TeleBot(BOT_TOKEN)

# ===== ХРАНЕНИЕ ПОЛЬЗОВАТЕЛЕЙ =====
users = {}

def get_user(user_id):
    if user_id not in users:
        users[user_id] = {
            "xp": 0,
            "level": "Новичок",
            "current": "Алфавит → Буква ب",
            "streak": 0
        }
    return users[user_id]


# ===== ГЛАВНОЕ МЕНЮ =====
def main_menu(chat_id, user_id):
    user = get_user(user_id)

    text = f"""
╔══════════════════════╗
        📖 Tajweed App
╚══════════════════════╝

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

━━━━━━━━━━━━━━━━━━━━━━
🚀 Продолжить обучение
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

    bot.send_message(chat_id, text, reply_markup=markup)


# ===== START =====
@bot.message_handler(commands=['start'])
def start(message):
    main_menu(message.chat.id, message.from_user.id)


# ===== ОБРАБОТКА КНОПОК =====
@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    user_id = call.from_user.id
    chat_id = call.message.chat.id
    data = call.data

    if data == "continue":
        bot.send_message(chat_id, "🚀 Продолжаем обучение...")

    elif data == "learn":
        bot.send_message(chat_id, "📖 Раздел обучения (скоро добавим модули)")

    elif data == "practice":
        bot.send_message(chat_id, "🧠 Практика (в разработке)")

    elif data == "memorize":
        bot.send_message(chat_id, "🎯 Заучивание Корана (в разработке)")

    elif data == "progress":
        bot.send_message(chat_id, "📊 Твой прогресс (в разработке)")

    elif data == "ai":
        bot.send_message(chat_id, "🤖 Напиши вопрос")


# ===== ЗАПУСК =====
print("🚀 Бот запущен")
bot.polling(none_stop=True)