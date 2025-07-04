import telebot
import random
import json

# 🔑 Вставь сюда свой токен от BotFather
TOKEN = '7754034337:AAELgRgAFFKv2lm0v3YvCuoy_vP7vj4tqeE'
bot = telebot.TeleBot(TOKEN)

# 📚 Загрузка мудростей из файла JSON
with open("wisdoms.json", "r", encoding="utf-8") as f:
    wisdoms = json.load(f)

# 📩 Команда /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(
    message.chat.id,
    "Добро пожаловать в *Точку тишины*.\nНажми или напиши '🧘 Получить истину'.",
    parse_mode="Markdown"
    )

# 💬 Обработка текстовых сообщений
@bot.message_handler(func=lambda message: True)
def send_wisdom(message):
    if "истину" in message.text.lower():
        quote = random.choice(wisdoms)
        bot.send_message(message.chat.id, f"🕯 {quote}")
    else:
        bot.send_message(message.chat.id, "Напиши '🧘 Получить истину', чтобы услышать мудрость.")

# 🚀 Запуск бота
bot.polling()
