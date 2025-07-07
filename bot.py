import telebot
import os
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from flask import Flask
import threading

from utils.supabase_parables import get_random_parable, add_parable, count_parables
from utils.supabase_users import save_user

TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID", 0))

bot = telebot.TeleBot(TOKEN)

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
            KeyboardButton("📝 Добавить мудрость"),
            KeyboardButton("➕ Добавить притчу"),
            KeyboardButton("📊 Кол-во притч")
        )

    bot.send_message(
        message.chat.id,
        "Добро пожаловать в *Точку тишины*. Выберите, что хотите:",
        parse_mode="Markdown",
        reply_markup=markup
    )

@bot.message_handler(func=lambda message: True)
def handle_buttons(message):
    text = message.text

    if text == "📖 Притча":
        bot.send_message(message.chat.id, get_random_parable())

    elif text == "➕ Добавить притчу" and message.from_user.id == ADMIN_ID:
        msg = bot.send_message(message.chat.id, "✍️ Напиши текст новой притчи:")
        bot.register_next_step_handler(msg, receive_parable)

    elif text == "📊 Кол-во притч" and message.from_user.id == ADMIN_ID:
        count = count_parables()
        bot.send_message(message.chat.id, f"📚 Всего притч в базе: {count}")

    else:
        bot.send_message(message.chat.id, "Нажми кнопку ниже или напиши '📖 Притча'.")

def receive_parable(message):
    text = message.text.strip()
    add_parable(text)
    bot.send_message(message.chat.id, "✅ Притча добавлена.")

app = Flask(__name__)
@app.route('/')
def home():
    return "I'm alive!"

def run_web():
    app.run(host="0.0.0.0", port=10000)

threading.Thread(target=run_web).start()
bot.polling()
