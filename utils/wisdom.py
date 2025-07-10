import random
import json
import os

WISDOM_FILE = "data/wisdom.json"

def load_wisdoms():
    if not os.path.exists(WISDOM_FILE):
        return []
    with open(WISDOM_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data.get("wisdom", [])

def save_wisdoms(wisdoms):
    with open(WISDOM_FILE, "w", encoding="utf-8") as f:
        json.dump({"wisdom": wisdoms}, f, ensure_ascii=False, indent=2)

def get_random_wisdom():
    import random
    wisdoms = load_wisdoms()
    if not wisdoms:
        return "📭 Пока нет мудростей."
    return random.choice(wisdoms)

def add_wisdom(text):
    wisdoms = load_wisdoms()
    if text in wisdoms:
        return False  # Уже есть
    wisdoms.append(text)
    save_wisdoms(wisdoms)
    return True

def delete_wisdom(text):
    wisdoms = load_wisdoms()
    if text not in wisdoms:
        return False
    wisdoms.remove(text)
    save_wisdoms(wisdoms)
    return True

def count_wisdom():
    return len(load_wisdoms())

WISDOMS = [
    "Настоящее — единственное, что реально.",
    "Мысли — не ты. Наблюдай, не вовлекайся.",
    "Позволь быть. Себе. Другим. Миру.",
    "Один вдох может изменить всё.",
    "Когда ты в тишине — ты дома."
]

def get_random_wisdom():
    return random.choice(WISDOMS)
