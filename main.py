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
    {"l":"ء","name":"Hamza","base":"ʾ","makhraj":"Гортань. Резкий звук — короткое прерывание воздуха."},

    {"l":"ا","name":"Alif","base":"","makhraj":"Глубокое горло. Воздух выходит свободно без преграды."},
    {"l":"ب","name":"Ba","base":"b","makhraj":"Обе губы полностью смыкаются, затем резко открываются."},
    {"l":"ت","name":"Ta","base":"t","makhraj":"Кончик языка касается верхних зубов."},
    {"l":"ث","name":"Tha","base":"th","makhraj":"Кончик языка выходит между зубами."},
    {"l":"ج","name":"Jim","base":"j","makhraj":"Средняя часть языка касается нёба."},
    {"l":"ح","name":"Ḥa","base":"ḥ","makhraj":"Средняя часть горла, звук без вибрации."},
    {"l":"خ","name":"Kh","base":"kh","makhraj":"Верхняя часть горла, с хрипом."},
    {"l":"د","name":"Dal","base":"d","makhraj":"Кончик языка касается верхних зубов."},
    {"l":"ذ","name":"Dhal","base":"dh","makhraj":"Кончик языка между зубами, мягко."},
    {"l":"ر","name":"Ra","base":"r","makhraj":"Кончик языка слегка вибрирует."},
    {"l":"ز","name":"Zay","base":"z","makhraj":"Кончик языка у зубов, звук звонкий."},
    {"l":"س","name":"Sin","base":"s","makhraj":"Кончик языка у зубов, шипящий звук."},
    {"l":"ش","name":"Shin","base":"sh","makhraj":"Средняя часть языка поднимается к нёбу."},
    {"l":"ص","name":"Ṣad","base":"ṣ","makhraj":"Кончик языка у зубов, но звук твёрдый и глубокий."},
    {"l":"ض","name":"Ḍad","base":"ḍ","makhraj":"Бок языка прижимается к верхним коренным зубам."},
    {"l":"ط","name":"Ṭa","base":"ṭ","makhraj":"Кончик языка, звук твёрдый, язык приподнят."},
    {"l":"ظ","name":"Ẓa","base":"ẓ","makhraj":"Кончик языка между зубами, звук твёрдый."},
    {"l":"ع","name":"ʿAyn","base":"ʿ","makhraj":"Середина горла, сжатый звук."},
    {"l":"غ","name":"Ghayn","base":"gh","makhraj":"Верх горла, с вибрацией."},
    {"l":"ف","name":"Fa","base":"f","makhraj":"Верхние зубы касаются нижней губы."},
    {"l":"ق","name":"Qaf","base":"q","makhraj":"Задняя часть языка касается мягкого нёба."},
    {"l":"ك","name":"Kaf","base":"k","makhraj":"Зад языка ближе к середине нёба."},
    {"l":"ل","name":"Lam","base":"l","makhraj":"Кончик языка у верхних зубов."},
    {"l":"م","name":"Mim","base":"m","makhraj":"Губы смыкаются, звук через нос."},
    {"l":"ن","name":"Nun","base":"n","makhraj":"Кончик языка + звук через нос."},
    {"l":"ه","name":"Ha","base":"h","makhraj":"Гортань, лёгкий выдох."},
    {"l":"و","name":"Waw","base":"w","makhraj":"Губы округляются."},
    {"l":"ي","name":"Ya","base":"y","makhraj":"Средняя часть языка поднимается."},
]

# ===== ФОРМЫ БУКВ =====
def forms_lesson(chat_id):
    text = """
🔡 ФОРМЫ БУКВ

ا — не соединяется справа
ب بـ ـبـ ـب
ت تـ ـتـ ـت
ث ثـ ـثـ ـث
ج جـ ـجـ ـج
ح حـ ـحـ ـح
خ خـ ـخـ ـخ
د — не соединяется справа
ذ — не соединяется справа
ر — не соединяется справа
ز — не соединяется справа
س سـ ـсـ ـс
ش شـ ـشـ ـش
ص صـ ـصـ ـص
ض ضـ ـضـ ـض
ط طـ ـطـ ـط
ظ ظـ ـظـ ـظ
ع عـ ـعـ ـع
غ غـ ـغـ ـغ
ف فـ ـفـ ـف
ق قـ ـقـ ـق
ك كـ ـكـ ـك
ل لـ ـلـ ـل
م مـ ـمـ ـم
ن نـ ـنـ ـن
ه هـ ـهـ ـه
و — не соединяется справа
ي يـ ـيـ ـي

📌 ا د ذ ر ز و не соединяются справа
"""

    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("⬅️ Назад", callback_data="learn"))

    bot.send_message(chat_id, text, reply_markup=markup)

# ===== USER =====
def get_user(user_id):
    if user_id not in users:
        users[user_id] = {
            "level":"Новичок",
            "xp":0,
            "streak":0,
            "current":"Алфавит",
            "step":0,
            "letter_index":0
        }
    return users[user_id]

# ===== AUDIO =====
def generate_audio(text):
    file = "voice.mp3"
    gTTS(text=text, lang="ar", slow=True).save(file)
    return file

# ===== МЕНЮ (НЕ ТРОГАЕМ) =====
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

# ===== ОБУЧЕНИЕ (ИСПРАВЛЕНО) =====
def learn_menu(chat_id, user_id):
    markup = InlineKeyboardMarkup()

    markup.add(InlineKeyboardButton("🔤 Алфавит", callback_data="alphabet"))
    markup.add(InlineKeyboardButton("🔡 Формы букв", callback_data="forms"))

    markup.add(InlineKeyboardButton("⬅️ Назад", callback_data="back_main"))

    bot.send_message(chat_id, "📚 ОБУЧЕНИЕ", reply_markup=markup)

# ===== УРОК =====
def alphabet_lesson(chat_id, user_id):
    user = get_user(user_id)
    step = user["step"]
    data = letters[user["letter_index"]]

    l = data["l"]
    base = data["base"]

    fatha = base + "a"
    damma = base + "u"
    kasra = base + "i"

    if step == 0:
        text = f"""
🔤 {l} — {data['name']}

📍 Махрадж:
{data['makhraj']}

📖 Харакаты:
{l}َ → {fatha}
{l}ُ → {damma}
{l}ِ → {kasra}

🎧 Слушай и повторяй
"""

        markup = InlineKeyboardMarkup()
        markup.add(
            InlineKeyboardButton("🔊 Буква", callback_data="sound"),
            InlineKeyboardButton("🔊 Харакаты", callback_data="sound_harakat")
        )
        markup.add(
            InlineKeyboardButton("➡️ К тесту", callback_data="to_test")
        )

    else:
        text = f"""
🎯 ТЕСТ

Как читается:

{l}َ
"""

        markup = InlineKeyboardMarkup(row_width=2)
        markup.add(
            InlineKeyboardButton(fatha, callback_data="correct"),
            InlineKeyboardButton(damma, callback_data="wrong"),
            InlineKeyboardButton(kasra, callback_data="wrong"),
            InlineKeyboardButton("aaa", callback_data="wrong")
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

    elif call.data == "forms":
    with open("images/arabic_letters_table_fixed.png", "rb") as photo:
        bot.send_photo(
            chat_id,
            photo,
            caption="🔄 Видоизменение букв"
        )
 

    elif call.data == "to_test":
        user["step"] = 1
        alphabet_lesson(chat_id, call.from_user.id)

    elif call.data == "sound":
        l = letters[user["letter_index"]]["l"]
        bot.send_voice(chat_id, open(generate_audio(l), "rb"))

    elif call.data == "sound_harakat":
        l = letters[user["letter_index"]]["l"]
        text = f"{l}َ {l}ُ {l}ِ"
        bot.send_voice(chat_id, open(generate_audio(text), "rb"))

    elif call.data == "correct":
        bot.send_message(chat_id, "✅ Правильно")
        user["step"] = 0
        user["letter_index"] += 1
        alphabet_lesson(chat_id, call.from_user.id)

    elif call.data == "wrong":
        bot.send_message(chat_id, "❌ Ошибка")

    elif call.data == "back_main":
        main_menu(chat_id, call.from_user.id)

# ===== START =====
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "🚀 Запуск...", reply_markup=ReplyKeyboardRemove())
    main_menu(message.chat.id, message.from_user.id)

print("🚀 Бот запущен")
def learn_menu(chat_id, user_id):
    markup = InlineKeyboardMarkup(row_width=2)

    markup.add(
        InlineKeyboardButton("🔤 Алфавит", callback_data="alphabet"),
        InlineKeyboardButton("🔄 Видоизменение", callback_data="forms")
    )

    markup.add(
        InlineKeyboardButton("🔗 Соединение", callback_data="connect"),
        InlineKeyboardButton("📜 Правила таджвида", callback_data="tajweed")
    )

    markup.add(
        InlineKeyboardButton("📖 Виды чтения", callback_data="reading"),
        InlineKeyboardButton("🎧 Практика чтения", callback_data="practice_read")
    )

    markup.add(InlineKeyboardButton("⬅️ Назад", callback_data="back_main"))

    bot.send_message(chat_id, "📚 ОБУЧЕНИЕ", reply_markup=markup)
@bot.callback_query_handler(func=lambda call: call.data == "connect")
def connect_module(call):
    bot.send_message(call.message.chat.id, "🔗 Соединение букв скоро будет")

@bot.callback_query_handler(func=lambda call: call.data == "tajweed")
def tajweed_module(call):
    bot.send_message(call.message.chat.id, "📜 Правила таджвида скоро будут")

@bot.callback_query_handler(func=lambda call: call.data == "reading")
def reading_module(call):
    bot.send_message(call.message.chat.id, "📖 Виды чтения скоро будут")

@bot.callback_query_handler(func=lambda call: call.data == "practice_read")
def practice_module(call):
    bot.send_message(call.message.chat.id, "🎧 Практика чтения скоро будет")
@bot.callback_query_handler(func=lambda call: call.data == "forms")
def override_forms(call):
    with open("images/arabic_letters_table_fixed.png", "rb") as photo:
        bot.send_photo(call.message.chat.id, photo)
bot.polling(none_stop=True)