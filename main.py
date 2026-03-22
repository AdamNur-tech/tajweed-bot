import os, json
import telebot
from openai import OpenAI

bot = telebot.TeleBot(os.getenv("BOT_TOKEN"))
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

DATA_FILE = "db.json"

# --- БАЗА ---
def load():
    if not os.path.exists(DATA_FILE):
        return {}
    return json.load(open(DATA_FILE))

def save(data):
    json.dump(data, open(DATA_FILE, "w"))

users = load()

# --- КУРС ---
COURSE = [
{"level":1,"title":"Алфавит","lesson":"ا ب ت ث","test":"Как читается ب؟","answer":"ба"},
{"level":2,"title":"Харакаты","lesson":"بَ بِ بُ","test":"بِ это?","answer":"би"},
{"level":3,"title":"Сукун","lesson":"بْ","test":"Что это?","answer":"сукун"},
{"level":4,"title":"Нун сакина","lesson":"4 правила","test":"Сколько правил?","answer":"4"},
]

# --- ПОЛЬЗОВАТЕЛЬ ---
def get_user(uid):
    if str(uid) not in users:
        users[str(uid)] = {
            "level":1,
            "xp":0,
            "errors":[],
            "step":"menu"
        }
    return users[str(uid)]

# --- СТАРТ ---
@bot.message_handler(commands=['start'])
def start(m):
    user = get_user(m.from_user.id)
    save(users)

    bot.send_message(m.chat.id,
        "🎓 Медресе таджвида PRO\n\n"
        "Ты пройдёшь путь до уровня кари\n\n"
        "Напиши: урок")

# --- УРОК ---
@bot.message_handler(func=lambda m: m.text.lower()=="урок")
def lesson(m):
    user = get_user(m.from_user.id)
    lvl = user["level"]

    if lvl > len(COURSE):
        bot.send_message(m.chat.id,"🎉 Ты завершил курс")
        return

    lesson = COURSE[lvl-1]

    bot.send_message(m.chat.id,
        f"📚 {lesson['title']}\n\n{lesson['lesson']}\n\n"
        "Напиши: тест")

# --- ТЕСТ ---
@bot.message_handler(func=lambda m: m.text.lower()=="тест")
def test(m):
    user = get_user(m.from_user.id)
    lvl = user["level"]

    q = COURSE[lvl-1]["test"]
    user["step"] = "test"
    save(users)

    bot.send_message(m.chat.id,f"❓ {q}")

# --- ОТВЕТ ---
@bot.message_handler(func=lambda m: get_user(m.from_user.id)["step"]=="test")
def answer(m):
    user = get_user(m.from_user.id)
    lvl = user["level"]

    correct = COURSE[lvl-1]["answer"]

    if correct in m.text.lower():
        user["xp"] += 10
        user["level"] += 1
        bot.send_message(m.chat.id,"✅ Правильно! Уровень ↑")
    else:
        user["errors"].append({
            "level":lvl,
            "error":m.text
        })
        bot.send_message(m.chat.id,f"❌ Ошибка. Ответ: {correct}")

    user["step"]="menu"
    save(users)

# --- ИИ ОБУЧЕНИЕ ---
@bot.message_handler(func=lambda m: m.text.startswith("объясни"))
def ai(m):
    user = get_user(m.from_user.id)

    res = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role":"system","content":
             "Ты учитель таджвида. Объясняй как новичку."},
            {"role":"user","content":m.text}
        ]
    )

    bot.send_message(m.chat.id,res.choices[0].message.content)

# --- ГОЛОС ---
@bot.message_handler(content_types=['voice'])
def voice(m):
    bot.send_message(m.chat.id,"🎧 Анализ...")

    file = bot.get_file(m.voice.file_id)
    audio = bot.download_file(file.file_path)

    with open("v.ogg","wb") as f:
        f.write(audio)

    with open("v.ogg","rb") as f:
        t = client.audio.transcriptions.create(
            model="gpt-4o-mini-transcribe",
            file=f
        )

    res = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role":"system","content":"Проверь таджвид"},
            {"role":"user","content":t.text}
        ]
    )

    bot.send_message(m.chat.id,
        f"📖 {t.text}\n\n🧠 {res.choices[0].message.content}"
    )

print("PRO MADRASA STARTED 🚀")
bot.infinity_polling()