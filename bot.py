import telebot
import os
from utils.db import init_db, save_user
from utils.admin import register_admin_commands
from flask import Flask
import threading

TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)

ADMIN_ID = 708145081

init_db()
register_admin_commands(bot, ADMIN_ID)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    save_user(message.from_user)
    bot.send_message(
        message.chat.id,
        "Добро пожаловать в *Точку тишины*.
Нажми или напиши '🧘 Получить истину'.",
        parse_mode="Markdown"
    )

@bot.message_handler(func=lambda message: True)
def echo_wisdom(message):
    if "истину" in message.text.lower():
        from utils.wisdom import get_random_wisdom
        bot.send_message(message.chat.id, f"🕯 {get_random_wisdom()}")
    else:
        bot.send_message(message.chat.id, "Напиши '🧘 Получить истину', чтобы услышать мудрость.")

# Flask-сервер для Render
app = Flask(__name__)
@app.route('/')
def home():
    return "I'm alive!"
def run_web():
    app.run(host="0.0.0.0", port=10000)
threading.Thread(target=run_web).start()

bot.polling()
