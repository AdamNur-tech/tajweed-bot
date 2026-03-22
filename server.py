# server.py
import os, sqlite3, json
from flask import Flask, request, jsonify, send_from_directory
import telebot
from openai import OpenAI

BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
BASE_URL = os.getenv("BASE_URL")  # например: https://your-app.up.railway.app

app = Flask(__name__, static_folder="web", static_url_path="/")
bot = telebot.TeleBot(BOT_TOKEN) if BOT_TOKEN else None
client = OpenAI(api_key=OPENAI_API_KEY) if OPENAI_API_KEY else None

# ---------- DB ----------
conn = sqlite3.connect("db.sqlite", check_same_thread=False)
cur = conn.cursor()
cur.execute("""
CREATE TABLE IF NOT EXISTS users(
  id INTEGER PRIMARY KEY,
  level INTEGER,
  xp INTEGER,
  step INTEGER,
  errors TEXT
)
""")
conn.commit()

def get_user(uid:int):
    cur.execute("SELECT id,level,xp,step,errors FROM users WHERE id=?", (uid,))
    row = cur.fetchone()
    if not row:
        cur.execute("INSERT INTO users VALUES(?,?,?,?,?)", (uid,1,0,0,"[]"))
        conn.commit()
        return {"id":uid,"level":1,"xp":0,"step":0,"errors":[]}
    return {"id":row[0],"level":row[1],"xp":row[2],"step":row[3],"errors":json.loads(row[4] or "[]")}

def save_user(u:dict):
    cur.execute("UPDATE users SET level=?,xp=?,step=?,errors=? WHERE id=?",
                (u["level"],u["xp"],u["step"],json.dumps(u["errors"]),u["id"]))
    conn.commit()

# ---------- COURSE (ядро + можно расширять) ----------
COURSE = [
# L1 Alphabet
{"level":1,"type":"lesson","title":"Алиф","content":"ا — звук А"},
{"level":1,"type":"lesson","title":"Ба","content":"ب — Б; بَ БА, بِ БИ, بُ БУ"},
{"level":1,"type":"quiz","q":"Как читается بِ ?","opts":["БА","БИ","БУ"],"a":1},

# L2 Harakat
{"level":2,"type":"lesson","title":"Харакаты","content":"َ = А, ِ = И, ُ = У"},
{"level":2,"type":"quiz","q":"Как читается بَ ?","opts":["БА","БИ","БУ"],"a":0},

# L3 Words
{"level":3,"type":"lesson","title":"Слова","content":"بَتَ = бата"},
{"level":3,"type":"quiz","q":"Как читается بُ ?","opts":["БУ","БИ","БА"],"a":0},

# L4 Tajweed
{"level":4,"type":"lesson","title":"Нун сакина","content":"Изхар, Идгам, Ихфа, Икляб"},
{"level":4,"type":"quiz","q":"مِن بَعْدِ — какое правило?","opts":["Ихфа","Икляб","Изхар"],"a":1},

# L5 Madd
{"level":5,"type":"lesson","title":"Мадд","content":"2, 4, 6 харакат"},
{"level":5,"type":"quiz","q":"Сколько харакат у мадд табии?","opts":["2","4","6"],"a":0},
]

def level_items(level:int):
    return [x for x in COURSE if x["level"]==level]

def next_item(u):
    items = level_items(u["level"])
    if u["step"] >= len(items):
        u["level"] += 1
        u["step"] = 0
        save_user(u)
        items = level_items(u["level"])
    if not items:
        return None
    return items[u["step"]]

# ---------- API ----------
@app.get("/")
def root():
    return send_from_directory("web", "index.html")

@app.get("/api/state")
def api_state():
    uid = int(request.args.get("uid","0"))
    u = get_user(uid)
    item = next_item(u)
    return jsonify({"user":u, "item":item})

@app.post("/api/next")
def api_next():
    data = request.json
    u = get_user(int(data["uid"]))
    u["step"] += 1
    save_user(u)
    return jsonify({"ok":True})

@app.post("/api/answer")
def api_answer():
    data = request.json
    u = get_user(int(data["uid"]))
    item = next_item(u)
    correct = False
    if item and item["type"]=="quiz":
        if int(data["i"]) == int(item["a"]):
            correct = True
            u["xp"] += 10
        else:
            u["errors"].append(item.get("q","unknown"))
        u["step"] += 1
        # level up
        if u["xp"] >= 100:
            u["level"] += 1
            u["xp"] = 0
    save_user(u)
    return jsonify({"correct":correct, "user":u})

@app.post("/api/ai_explain")
def api_ai_explain():
    data = request.json
    text = data.get("text","")
    if not client:
        return jsonify({"answer":"AI не настроен"})
    res = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role":"system","content":"Ты учитель таджвида. Объясни просто и по шагам."},
            {"role":"user","content":text}
        ]
    )
    return jsonify({"answer":res.choices[0].message.content})

# ---------- TELEGRAM (голос + webhook) ----------
if bot:
    @bot.message_handler(commands=['start'])
    def tg_start(m):
        link = f"{BASE_URL}/?uid={m.from_user.id}"
        bot.send_message(m.chat.id,
            f"🕌 Tajweed AI PRO\n\nОткрой приложение:\n{link}\n\n"
            "🎤 Отправь голос — проверю таджвид")

    @bot.message_handler(content_types=['voice'])
    def tg_voice(m):
        bot.send_message(m.chat.id, "🎧 Анализ...")
        f = bot.get_file(m.voice.file_id)
        audio = bot.download_file(f.file_path)
        with open("v.ogg","wb") as o:
            o.write(audio)

        # STT
        with open("v.ogg","rb") as inp:
            t = client.audio.transcriptions.create(
                model="gpt-4o-mini-transcribe",
                file=inp
            )
        text = t.text

        # Analysis
        res = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role":"system","content":
                 "Ты строгий учитель таджвида: 1) ошибки 2) как исправить 3) совет."},
                {"role":"user","content":text}
            ]
        )
        bot.send_message(m.chat.id, f"📖 {text}\n\n🧠 {res.choices[0].message.content}")

    @app.post("/webhook")
    def webhook():
        json_str = request.get_data().decode('UTF-8')
        update = telebot.types.Update.de_json(json_str)
        bot.process_new_updates([update])
        return "OK", 200

    @app.get("/set_webhook")
    def set_webhook():
        if not BASE_URL:
            return "BASE_URL not set", 400
        bot.remove_webhook()
        bot.set_webhook(url=f"{BASE_URL}/webhook")
        return "Webhook set"

# ---------- RUN ----------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 8080)))