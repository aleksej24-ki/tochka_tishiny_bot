import telebot
import os
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from flask import Flask
import threading
from dotenv import load_dotenv

from utils.db import init_db, save_user
from utils.parables import (
    create_parables_table,
    add_parable,
    get_random_parable,
    get_parables_count,
)

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)

ADMIN_ID = 708145081

init_db()
create_parables_table()

@bot.message_handler(commands=['start'])
def send_welcome(message):
    save_user(message.from_user)

    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(
        KeyboardButton("🧘 Получить истину"),
        KeyboardButton("📖 Притча")
    )
    if message.from_user.id == ADMIN_ID:
        markup.add(
            KeyboardButton("📜 Все мудрости"),
            KeyboardButton("📝 Добавить притчу"),
            KeyboardButton("✉️ Сколько притч")
        )

    bot.send_message(
        message.chat.id,
        "Добро пожаловать в *Точку тишины*.\nВыберите, что хотите:",
        parse_mode="Markdown",
        reply_markup=markup
    )

@bot.message_handler(func=lambda m: m.text == "📝 Добавить притчу")
def handle_add_parable(message):
    if message.from_user.id != ADMIN_ID:
        bot.send_message(message.chat.id, "❌ Только админ может это.")
        return
    msg = bot.send_message(message.chat.id, "✍️ Введи новую притчу:")
    bot.register_next_step_handler(msg, save_parable_text)

def save_parable_text(message):
    add_parable(message.text.strip())
    bot.send_message(message.chat.id, "✅ Притча сохранена!")

@bot.message_handler(func=lambda m: m.text == "✉️ Сколько притч")
def handle_count(message):
    if message.from_user.id == ADMIN_ID:
        count = get_parables_count()
        bot.send_message(message.chat.id, f"📖 В базе: {count} притч.")

@bot.message_handler(func=lambda message: True)
def handle_buttons(message):
    text = message.text
    if text == "🧘 Получить истину":
        bot.send_message(message.chat.id, "🕯 Истина тиха... скоро появится.")
    elif text == "📖 Притча":
        bot.send_message(message.chat.id, get_random_parable())
    else:
        bot.send_message(message.chat.id, "Нажми кнопку снизу.")

app = Flask(__name__)
@app.route('/')
def home():
    return "I'm alive!"

def run_web():
    app.run(host="0.0.0.0", port=10000)

threading.Thread(target=run_web).start()
bot.polling(non_stop=True)
