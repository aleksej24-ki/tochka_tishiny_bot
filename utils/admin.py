from utils.db import get_all_users
from utils.wisdom import add_wisdom, load_wisdoms, search_wisdoms, delete_wisdom_by_index

def register_admin_commands(bot, ADMIN_ID):

    @bot.message_handler(commands=['add'])
    def add_command(message):
        if message.from_user.id != ADMIN_ID:
            bot.reply_to(message, "🚫 У тебя нет доступа.")
            return

        parts = message.text.split(' ', 1)
        if len(parts) < 2:
            bot.reply_to(message, "⚠️ Напиши текст после команды, например:
`/add Мудрость начинается с тишины.`", parse_mode="Markdown")
            return

        if add_wisdom(parts[1].strip()):
            bot.reply_to(message, "📝 Мудрость добавлена.")
        else:
            bot.reply_to(message, "⚠️ Такая мудрость уже есть.")

    @bot.message_handler(commands=['list'])
    def list_command(message):
        if message.from_user.id != ADMIN_ID:
            bot.reply_to(message, "🚫 У тебя нет доступа.")
            return

        wisdoms = load_wisdoms()
        text = "\n\n".join([f"{i+1}. {w}" for i, w in enumerate(wisdoms)])
        if len(text) < 4000:
            bot.reply_to(message, f"🧘 Все мудрости:\n\n{text}")
        else:
            with open("wisdom_list.txt", "w", encoding="utf-8") as f:
                f.write(text)
            with open("wisdom_list.txt", "rb") as f_send:
                bot.send_document(message.chat.id, f_send)

    @bot.message_handler(commands=['search'])
    def search_command(message):
        if message.from_user.id != ADMIN_ID:
            bot.reply_to(message, "🚫 У тебя нет доступа.")
            return

        parts = message.text.split(' ', 1)
        if len(parts) < 2:
            bot.reply_to(message, "⚠️ Напиши слово для поиска, например:
`/search тишина`", parse_mode="Markdown")
            return

        matches = search_wisdoms(parts[1].lower().strip())
        if matches:
            text = "\n\n".join(matches)
            if len(text) < 4000:
                bot.reply_to(message, f"🔍 Найдено:\n\n{text}")
            else:
                with open("search_results.txt", "w", encoding="utf-8") as f:
                    f.write(text)
                with open("search_results.txt", "rb") as f_send:
                    bot.send_document(message.chat.id, f_send)
        else:
            bot.reply_to(message, "😔 Ничего не найдено.")

    @bot.message_handler(commands=['delete'])
    def delete_command(message):
        if message.from_user.id != ADMIN_ID:
            bot.reply_to(message, "🚫 У тебя нет доступа.")
            return

        parts = message.text.split(' ', 1)
        if len(parts) < 2 or not parts[1].strip().isdigit():
            bot.reply_to(message, "⚠️ Укажи номер, например `/delete 3`", parse_mode="Markdown")
            return

        removed = delete_wisdom_by_index(int(parts[1]) - 1)
        if removed:
            bot.reply_to(message, f"🗑 Удалено:\n{removed}")
        else:
            bot.reply_to(message, "❌ Нет такого номера.")

    @bot.message_handler(commands=['users'])
    def users_command(message):
        if message.from_user.id != ADMIN_ID:
            bot.reply_to(message, "🚫 У тебя нет доступа.")
            return

        users = get_all_users()
        if not users:
            bot.reply_to(message, "📭 Нет пользователей.")
            return

        lines = [f"{u[2] or ''} {u[3] or ''} (@{u[1] or '—'})\nID: {u[0]}\n📅 {u[4]}" for u in users]
        text = "\n\n".join(lines)

        if len(text) < 4000:
            bot.reply_to(message, f"👥 Пользователи:\n\n{text}")
        else:
            with open("users_list.txt", "w", encoding="utf-8") as f:
                f.write(text)
            with open("users_list.txt", "rb") as f_send:
                bot.send_document(message.chat.id, f_send)
