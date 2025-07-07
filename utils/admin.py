from telebot.types import KeyboardButton

ADMIN_ID = 708145081

def is_admin(user_id):
    return user_id == ADMIN_ID

def admin_buttons():
    return [
        KeyboardButton("📜 Все мудрости"),
        KeyboardButton("📝 Добавить мудрость"),
        KeyboardButton("📖 Притча"),
        KeyboardButton("➕ Добавить притчу"),
        KeyboardButton("📊 Всего притч")
    ]
