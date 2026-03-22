import os, json
import telebot
from openai import OpenAI

bot = telebot.TeleBot(os.getenv("BOT_TOKEN"))
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

DB = "db.json"

def load():
    if not os.path.exists(DB):
        return {}
    return json.load(open(DB))

def save(data):
    json.dump(data, open(DB, "w"))

users = load()

def get_user(uid):
    if str(uid) not in users:
        users[str(uid)] = {
            "level": 1,
            "stage": "alphabet",
            "errors": [],
            "history": [],
            "mode": "learn"
        }
    return users[str(uid)]

# --- СТАРТ ---
@bot.message_handler(commands=['start'])
def start(m):
    user = get_user(m.from_user.id)
    save(users)

    bot.send_message(m.chat.id,
        "🕌 AI Медресе Таджвида\n\n"
        "Я научу тебя с нуля до уровня قارئ\n\n"
        "Команды:\n"
        "📚 урок\n"
        "🧠 вопрос\n"
        "🎤 практика\n"
        "📊 прогресс\n"
    )

# --- УРОК ---
@bot.message_handler(func=lambda m: m.text.lower() == "урок")
def lesson(m):
    user = get_user(m.from_user.id)

    res = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role":"system",
                "content":
                "Ты лучший учитель таджвида.\n"
                "Обучай по шагам:\n"
                "1. Объяснение\n"
                "2. Примеры\n"
                "3. Задание\n"
                "4. Вопрос\n"
            },
            {
                "role":"user",
                "content":
                f"Уровень: {user['level']}\n"
                f"Этап: {user['stage']}\n"
                f"Ошибки: {user['errors']}\n"
                "Дай следующий урок"
            }
        ]
    )

    bot.send_message(m.chat.id, res.choices[0].message.content)

# --- ВОПРОС ---
@bot.message_handler(func=lambda m: m.text.lower().startswith("вопрос"))
def question(m):
    user = get_user(m.from_user.id)

    res = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role":"system",
                "content":
                "Ты учитель таджвида. Отвечай просто и понятно."
            },
            {"role":"user","content":m.text}
        ]
    )

    bot.send_message(m.chat.id, res.choices[0].message.content)

# --- ПРАКТИКА ТЕКСТ ---
@bot.message_handler(func=lambda m: m.text.lower().startswith("ответ"))
def answer(m):
    user = get_user(m.from_user.id)

    res = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role":"system",
                "content":
                "Ты учитель таджвида.\n"
                "Проверь ответ ученика:\n"
                "- правильно или нет\n"
                "- объясни ошибку\n"
            },
            {"role":"user","content":m.text}
        ]
    )

    bot.send_message(m.chat.id, res.choices[0].message.content)

# --- ГОЛОС ---
@bot.message_handler(content_types=['voice'])
def voice(m):
    bot.send_message(m.chat.id, "🎧 Слушаю чтение...")

    file = bot.get_file(m.voice.file_id)
    audio = bot.download_file(file.file_path)

    with open("voice.ogg","wb") as f:
        f.write(audio)

    with open("voice.ogg","rb") as f:
        t = client.audio.transcriptions.create(
            model="gpt-4o-mini-transcribe",
            file=f
        )

    text = t.text

    res = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role":"system",
                "content":
                "Ты строгий учитель таджвида.\n"
                "Разбери чтение:\n"
                "- ошибки\n"
                "- как исправить\n"
                "- правильное чтение\n"
            },
            {"role":"user","content":text}
        ]
    )

    bot.send_message(m.chat.id,
        f"📖 Ты прочитал:\n{text}\n\n🧠 Разбор:\n{res.choices[0].message.content}"
    )

# --- ПРОГРЕСС ---
@bot.message_handler(func=lambda m: m.text.lower() == "прогресс")
def progress(m):
    user = get_user(m.from_user.id)

    bot.send_message(m.chat.id,
        f"📊 Уровень: {user['level']}\n"
        f"Ошибки: {len(user['errors'])}"
    )

print("FINAL AI MADRASA 🚀")
bot.infinity_polling()