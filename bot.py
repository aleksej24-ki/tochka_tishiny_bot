
import os
import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from flask import Flask, request
from utils.supabase_parables import get_random_parable
from utils.wisdom import get_random_wisdom

# Получение токена и URL из переменных окружения
BOT_TOKEN = os.getenv("TELEGRAM_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")  # Пример: https://your-app.onrender.com

bot = telebot.TeleBot(BOT_TOKEN)
app = Flask(__name__)

# Обработка команды /start
@bot.message_handler(commands=["start"])
def send_welcome(message):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(KeyboardButton("🧘 Получить истину"), KeyboardButton("📖 Притча"))
    bot.send_message(
        message.chat.id,
        "Добро пожаловать в *Точку тишины*. Выберите:",
        parse_mode="Markdown",
        reply_markup=markup
    )

# Кнопка — Получить истину
@bot.message_handler(func=lambda msg: msg.text == "🧘 Получить истину")
def send_wisdom(msg):
    text = get_random_wisdom()
    bot.send_message(msg.chat.id, f"🕯 {text}")

# Кнопка — Притча
@bot.message_handler(func=lambda msg: msg.text == "📖 Притча")
def send_parable(msg):
    text = get_random_parable()
    bot.send_message(msg.chat.id, f"📖 {text}")

# Webhook endpoint
@app.route(f"/{BOT_TOKEN}", methods=["POST"])
def webhook():
    update = telebot.types.Update.de_json(request.get_json())
    bot.process_new_updates([update])
    return "ok", 200

# Проверка доступности
@app.route("/", methods=["GET"])
def index():
    return "Бот работает!", 200

# Устанавливаем webhook при запуске сервера

if __name__ == "__main__":
    bot.remove_webhook()
    bot.set_webhook(url=f"{WEBHOOK_URL}/{TOKEN}")
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
