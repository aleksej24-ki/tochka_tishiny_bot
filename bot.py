import telebot
import random
import json
import os
from flask import Flask
import threading

TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)

with open("wisdoms.json", "r", encoding="utf-8") as f:
    wisdoms = json.load(f)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(
        message.chat.id,
        "Добро пожаловать в *Точку тишины*.\nНажми или напиши '🧘 Получить истину'.",
        parse_mode="Markdown"
    )

@bot.message_handler(func=lambda message: True)
def send_wisdom(message):
    if "истину" in message.text.lower():
        quote = random.choice(wisdoms)
        bot.send_message(message.chat.id, f"🕯 {quote}")
    else:
        bot.send_message(message.chat.id, "Напиши '🧘 Получить истину', чтобы услышать мудрость.")

# 🧵 HTTP-сервер для Render
app = Flask(__name__)

@app.route('/')
def home():
    return "I'm alive!"

def run_web():
    app.run(host="0.0.0.0", port=10000)

threading.Thread(target=run_web).start()

# 🚀 Запуск бота
bot.polling()
