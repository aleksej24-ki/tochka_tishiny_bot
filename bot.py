import telebot import os from telebot.types import ReplyKeyboardMarkup, KeyboardButton from flask import Flask import threading

from utils.supabase_users import save_user from utils.supabase_parables import get_random_parable, add_parable from utils.wisdom import get_random_wisdom, load_wisdoms, add_wisdom

TOKEN = os.getenv("BOT_TOKEN") ADMIN_ID = int(os.getenv("ADMIN_ID", "708145081"))

bot = telebot.TeleBot(TOKEN)

Стартовая команда

@bot.message_handler(commands=['start']) def send_welcome(message): save_user(message.from_user)

markup = ReplyKeyboardMarkup(resize_keyboard=True)
markup.add(
    KeyboardButton("🧘 Получить истину"),
    KeyboardButton("📖 Притча")
)
if message.from_user.id == ADMIN_ID:
    markup.add(
        KeyboardButton("📜 Все мудрости"),
        KeyboardButton("📝 Добавить мудрость")
    )

bot.send_message(
    message.chat.id,
    "Добро пожаловать в *Точку тишины*. Выбери, что желаешь:",
    parse_mode="Markdown",
    reply_markup=markup
)

Добавление притчи

@bot.message_handler(commands=['add_parable']) def add_parable_command(message): if message.from_user.id != ADMIN_ID: return bot.reply_to(message, "🚫 Только админ может добавлять притчи.") msg = bot.send_message(message.chat.id, "✍️ Введи притчу") bot.register_next_step_handler(msg, save_parable_text)

def save_parable_text(message): add_parable(message.text.strip()) bot.send_message(message.chat.id, "✅ Притча сохранена")

Обработка кнопок

@bot.message_handler(func=lambda message: True) def handle_buttons(message): text = message.text

if text == "🧘 Получить истину":
    bot.send_message(message.chat.id, f"🔧 {get_random_wisdom()}")

elif text == "📜 Все мудрости":
    wisdoms = load_wisdoms()
    if len(wisdoms) < 15:
        text_block = "\n\n".join([f"{i+1}. {w}" for i, w in enumerate(wisdoms)])
        bot.send_message(message.chat.id, f"🧘 Все мудрости:\n\n{text_block}")
    else:
        with open("wisdoms_list.txt", "w", encoding="utf-8") as f:
            f.write("\n\n".join([f"{i+1}. {w}" for i, w in enumerate(wisdoms)]))
        with open("wisdoms_list.txt", "rb") as f:
            bot.send_document(message.chat.id, f)

elif text == "📝 Добавить мудрость":
    if message.from_user.id == ADMIN_ID:
        bot.send_message(message.chat.id, "✍️ Введи новую мудрость:")
        bot.register_next_step_handler(message, receive_wisdom)
    else:
        bot.send_message(message.chat.id, "🚫 Только админ может добавлять")

elif text == "📖 Притча":
    bot.send_message(message.chat.id, get_random_parable())

else:
    bot.send_message(message.chat.id, "Нажми кнопку ниже или напиши '🧘 Получить истину'.")

def receive_wisdom(message): new_text = message.text.strip() if add_wisdom(new_text): bot.send_message(message.chat.id, "📝 Мудрость добавлена!") else: bot.send_message(message.chat.id, "⚠️ Такая уже есть.")

Flask сервер

app = Flask(name)

@app.route('/') def home(): return "I'm alive!"

def run_web(): app.run(host="0.0.0.0", port=10000)

threading.Thread(target=run_web).start()

bot.polling(none_stop=True)

