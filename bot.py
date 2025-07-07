import telebot
import os
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from flask import Flask
import threading

from utils.parables_pg import create_table, add_parable, get_random_parable, get_parables_count

TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)
ADMIN_ID = 708145081

create_table()

@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(
        KeyboardButton("🧘 Получить истину"),
        KeyboardButton("📖 Притча")
    )
    if message.from_user.id == ADMIN_ID:
        markup.add(KeyboardButton("📜 Все мудрости"))
        markup.add(KeyboardButton("📝 Добавить притчу"))
    bot.send_message(message.chat.id, "Добро пожаловать в *Точку тишины*.", parse_mode="Markdown", reply_markup=markup)

@bot.message_handler(commands=['count_parables'])
def count_parables(message):
    if message.from_user.id != ADMIN_ID:
        return
    count = get_parables_count()
    bot.send_message(message.chat.id, f"📖 В базе {count} притч.")

@bot.message_handler(func=lambda message: True)
def handle_buttons(message):
    text = message.text
    if text == "📖 Притча":
        bot.send_message(message.chat.id, get_random_parable())
    elif text == "📝 Добавить притчу" and message.from_user.id == ADMIN_ID:
        msg = bot.send_message(message.chat.id, "✍️ Введи новую притчу:")
        bot.register_next_step_handler(msg, receive_parable)
    else:
        bot.send_message(message.chat.id, "Выберите команду с клавиатуры.")

def receive_parable(message):
    add_parable(message.text.strip())
    bot.send_message(message.chat.id, "✅ Притча добавлена!")

app = Flask(__name__)
@app.route('/')
def home():
    return "I'm alive!"
def run_web():
    app.run(host="0.0.0.0", port=10000)
threading.Thread(target=run_web).start()
bot.polling()