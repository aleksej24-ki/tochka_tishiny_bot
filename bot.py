import os
import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from flask import Flask, request
from utils.supabase_parables import get_random_parable
from utils.wisdom import get_random_wisdom

# Получение токена и URL из переменных окружения
BOT_TOKEN = os.getenv("TELEGRAM_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")  # Например: https://tochka-tishiny-bot.onrender.com

# Проверка переменных
if not BOT_TOKEN:
    raise Exception("❌ TELEGRAM_TOKEN не указан в переменных окружения!")
if not WEBHOOK_URL:
    raise Exception("❌ WEBHOOK_URL не указан в переменных окружения!")

bot = telebot.TeleBot(BOT_TOKEN)

app = Flask(__name__)

# Обработка команды /start
@bot.message_handler(commands=["start"])
def send_welcome(message):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(
        KeyboardButton("🧘 Получить истину"),
        KeyboardButton("📖 Притча")
    )
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
    print("🚀 Кнопка 'Притча' нажата")
    text = get_random_parable()
    print("📨 Отправка ответа пользователю")
    bot.send_message(msg.chat.id, f"📖 {text}")
    
# Webhook endpoint для Telegram
@app.route(f"/{BOT_TOKEN}", methods=["POST"])
def webhook():
    update = telebot.types.Update.de_json(request.get_json())
    bot.process_new_updates([update])
    return "ok", 200

# Проверка сервера (GET запрос)
@app.route("/", methods=["GET"])
def index():
    return "Бот работает!", 200

# Установка webhook при запуске
if __name__ == "__main__":
    bot.remove_webhook()
    bot.set_webhook(url=f"{WEBHOOK_URL}/{BOT_TOKEN}")
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
