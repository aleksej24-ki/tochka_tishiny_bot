import telebot
import random
import json
import os
import sqlite3
from datetime import datetime
from flask import Flask
import threading
ADMIN_ID = 708145081

# 🔑 Токен из переменной окружения
TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)

# 📚 Загрузка цитат
with open("wisdoms.json", "r", encoding="utf-8") as f:
    wisdoms = json.load(f)

# 🗃️ Инициализация базы данных
def init_db():
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username TEXT,
            first_name TEXT,
            last_name TEXT,
            date_joined TEXT
        )
    ''')
    conn.commit()
    conn.close()

init_db()

# 📩 Обработка команды /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id = message.from_user.id
    username = message.from_user.username
    first_name = message.from_user.first_name
    last_name = message.from_user.last_name
    date_joined = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute('''
        INSERT OR IGNORE INTO users (id, username, first_name, last_name, date_joined)
        VALUES (?, ?, ?, ?, ?)
    ''', (user_id, username, first_name, last_name, date_joined))
    conn.commit()
    conn.close()

    bot.send_message(
        message.chat.id,
        "Добро пожаловать в *Точку тишины*.\nНажми или напиши '🧘 Получить истину'.",
        parse_mode="Markdown"
    )

@bot.message_handler(commands=['add'])
def add_wisdom(message):
    if message.from_user.id != ADMIN_ID:
        bot.reply_to(message, "🚫 У тебя нет доступа к этой команде.")
        return

    parts = message.text.split(' ', 1)
    if len(parts) < 2:
        bot.reply_to(message, "⚠️ Напиши текст после команды, например:\n`/add Мудрость начинается с тишины.`", parse_mode="Markdown")
        return

    new_wisdom = parts[1].strip()

    # Загрузим существующие мудрости
    with open("wisdoms.json", "r", encoding="utf-8") as f:
        wisdoms = json.load(f)

    # Проверим на наличие дубликата (без учёта регистра и пробелов)
    if any(new_wisdom.lower().strip() == w.lower().strip() for w in wisdoms):
        bot.reply_to(message, "⚠️ Такая мудрость уже есть в списке.")
        return

    # Добавим и сохраним
    wisdoms.append(new_wisdom)

    with open("wisdoms.json", "w", encoding="utf-8") as f:
        json.dump(wisdoms, f, ensure_ascii=False, indent=2)

    bot.reply_to(message, "📝 Мудрость добавлена.")

# 🧘 Получение истины
@bot.message_handler(func=lambda message: True)
def send_wisdom(message):
    if "истину" in message.text.lower():
        quote = random.choice(wisdoms)
        bot.send_message(message.chat.id, f"🕯 {quote}")
    elif message.text == "/stats":
        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM users")
        count = cursor.fetchone()[0]
        conn.close()
        bot.send_message(message.chat.id, f"📊 Всего пользователей: {count}")
    else:
        bot.send_message(message.chat.id, "Напиши '🧘 Получить истину', чтобы услышать мудрость.")

# 🌐 Flask-сервер для Render + UptimeRobot
app = Flask(__name__)

@app.route('/')
def home():
    return "I'm alive!"

def run_web():
    app.run(host="0.0.0.0", port=10000)

threading.Thread(target=run_web).start()

# 🚀 Запуск бота
bot.polling()
