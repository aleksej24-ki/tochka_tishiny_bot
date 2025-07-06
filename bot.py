import telebot
import os
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from flask import Flask
import threading

from utils.db import init_db, save_user
from utils.wisdom import get_random_wisdom, load_wisdoms, add_wisdom

TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)

ADMIN_ID = 708145081

init_db()

@bot.message_handler(commands=['start'])
def send_welcome(message):
    save_user(message.from_user)

    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(
        KeyboardButton("🧘 Получить истину"),
        KeyboardButton("📜 Все мудрости")
    )
    if message.from_user.id == ADMIN_ID:
        markup.add(KeyboardButton("📝 Добавить мудрость"))

    bot.send_message(
        message.chat.id,
        "Добро пожаловать в *Точку тишины*. Выберите, что хотите:",
        parse_mode="Markdown",
        reply_markup=markup
    )

@bot.message_handler(func=lambda message: True)
def handle_buttons(message):
    text = message.text

    if text == "🧘 Получить истину":
        bot.send_message(message.chat.id, f"🕯 {get_random_wisdom()}")

    elif text == "📜 Все мудрости":
        wisdoms = load_wisdoms()
        if len(wisdoms) < 15:
            full = "\n\n".join([f"{i+1}. {w}" for i, w in enumerate(wisdoms)])
            bot.send_message(message.chat.id, f"🧘 Все мудрости:\n\n{full}")
        else:
            with open("wisdoms_list.txt", "w", encoding="utf-8") as f:
                f.write("\n\n".join([f"{i+1}. {w}" for i, w in enumerate(wisdoms)]))
            with open("wisdoms_list.txt", "rb") as f_send:
                bot.send_document(message.chat.id, f_send)

    elif text == "📝 Добавить мудрость":
        if message.from_user.id == ADMIN_ID:
            bot.send_message(message.chat.id, "✍️ Напиши текст новой мудрости:")
            bot.register_next_step_handler(message, receive_wisdom)
        else:
            bot.send_message(message.chat.id, "🚫 Только админ может добавлять.")

    else:
        bot.send_message(message.chat.id, "Нажми кнопку ниже или напиши '🧘 Получить истину'.")

def receive_wisdom(message):
    new_text = message.text.strip()
    if add_wisdom(new_text):
        bot.send_message(message.chat.id, "📝 Мудрость добавлена!")
    else:
        bot.send_message(message.chat.id, "⚠️ Такая мудрость уже существует.")

# Flask-сервер
app = Flask(__name__)
@app.route('/')
def home():
    return "I'm alive!"
def run_web():
    app.run(host="0.0.0.0", port=10000)
threading.Thread(target=run_web).start()

bot.polling()
