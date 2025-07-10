import json
import os

FILE_PATH = os.path.join("..", "wisdom.json")

def load_wisdoms():
    try:
        with open(FILE_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
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
