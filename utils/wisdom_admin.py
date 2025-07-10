import json
import os

FILE_PATH = os.path.join(os.getcwd(), "wisdom.json")

print("🗂 Абсолютный путь к wisdom.json:", FILE_PATH)

def load_wisdoms():
    try:
        print("🟡 Путь к файлу:", FILE_PATH)
        with open(FILE_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
            print("📘 Загружено мудростей:", len(data))
            return data
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print("❌ Ошибка при загрузке мудростей:", str(e))
        return []

def save_wisdoms(data):
    with open(FILE_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def add_wisdom(text):
    data = load_wisdoms()
    data.append(text.strip())
    save_wisdoms(data)
    return len(data)

def delete_wisdom(index):
    data = load_wisdoms()
    if 0 <= index < len(data):
        removed = data.pop(index)
        save_wisdoms(data)
        return removed
    else:
        return None

def count_wisdoms():
    return len(load_wisdoms())
