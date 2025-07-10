import json
import os

FILE_PATH = os.path.join(os.getcwd(), "wisdom.json")

def load_wisdoms():
    if not os.path.exists(FILE_PATH):
        return []
    with open(FILE_PATH, "r", encoding="utf-8") as file:
        return json.load(file)

def save_wisdoms(data):
    with open(FILE_PATH, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=2)

def add_wisdom(text):
    data = load_wisdoms()
    if text in data:
        return "⚠️ Такая мудрость уже существует."
    data.append(text)
    save_wisdoms(data)
    return "✅ Мудрость добавлена."

def delete_wisdom(index):
    data = load_wisdoms()
    try:
        removed = data.pop(index - 1)
        save_wisdoms(data)
        return f"🗑 Удалено: {removed}"
    except IndexError:
        return "❌ Неверный номер мудрости."

def count_wisdoms():
    return f"📊 Всего мудростей: {len(load_wisdoms())}"

def list_wisdoms():
    data = load_wisdoms()
    if not data:
        return "📭 Мудростей пока нет."
    result = ["📜 Список мудростей:"]
    for i, item in enumerate(data, 1):
        result.append(f"{i}. {item}")
    return "\n".join(result)
