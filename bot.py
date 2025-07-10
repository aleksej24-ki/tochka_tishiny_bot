import os
import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from flask import Flask, request
from utils.supabase_parables import get_random_parable
from utils.wisdom import get_random_wisdom
from utils.wisdom_admin import add_wisdom, delete_wisdom, count_wisdoms


ADMIN_ID = 708145081  # <-- замени на свой Telegram ID

BOT_TOKEN = os.getenv("TELEGRAM_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")

bot = telebot.TeleBot(BOT_TOKEN)
app = Flask(__name__)

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

@bot.message_handler(commands=["add"])
def handle_add(message):
    if message.from_user.id != ADMIN_ID:
        return
    text = message.text[5:].strip()
    if not text:
        bot.reply_to(message, "❗ Укажи текст мудрости после команды.")
        return
    total = add_wisdom(text)
    bot.reply_to(message, f"✅ Мудрость добавлена. Всего: {total}")

@bot.message_handler(commands=["delete"])
def handle_delete(message):
    if message.from_user.id != ADMIN_ID:
        return
    try:
        index = int(message.text.split()[1])
        deleted = delete_wisdom(index)
        if deleted:
            bot.reply_to(message, f"🗑 Удалено: {deleted}")
        else:
            bot.reply_to(message, "❌ Неверный индекс.")
    except (IndexError, ValueError):
        bot.reply_to(message, "❗ Укажи индекс: `/delete 2`", parse_mode="Markdown")

@bot.message_handler(commands=["count"])
def handle_count(message):
    if message.from_user.id != ADMIN_ID:
        return
    total = count_wisdoms()
    bot.reply_to(message, f"📊 Всего мудростей: {total}")

@bot.message_handler(func=lambda msg: msg.text == "🧘 Получить истину")
def send_wisdom(msg):
    bot.send_message(msg.chat.id, f"🕯 {get_random_wisdom()}")

@bot.message_handler(func=lambda msg: msg.text == "📖 Притча")
def send_parable(msg):
    bot.send_message(msg.chat.id, f"📖 {get_random_parable()}")

@app.route(f"/{BOT_TOKEN}", methods=["POST"])
def webhook():
    update = telebot.types.Update.de_json(request.get_json())
    bot.process_new_updates([update])
    return "ok", 200

@app.route("/", methods=["GET"])
def index():
    return "Бот работает!", 200

if __name__ == "__main__":
    bot.remove_webhook()
    bot.set_webhook(url=f"{WEBHOOK_URL}/{BOT_TOKEN}")
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
