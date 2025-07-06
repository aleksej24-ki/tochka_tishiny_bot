import json
import random

WISDOM_FILE = "wisdoms.json"

def load_wisdoms():
    with open(WISDOM_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_wisdoms(wisdoms):
    with open(WISDOM_FILE, "w", encoding="utf-8") as f:
        json.dump(wisdoms, f, ensure_ascii=False, indent=2)

def add_wisdom(text):
    wisdoms = load_wisdoms()
    if text.lower().strip() in [w.lower().strip() for w in wisdoms]:
        return False
    wisdoms.append(text)
    save_wisdoms(wisdoms)
    return True

def get_random_wisdom():
    wisdoms = load_wisdoms()
    return random.choice(wisdoms)

def search_wisdoms(keyword):
    wisdoms = load_wisdoms()
    return [f"{i+1}. {w}" for i, w in enumerate(wisdoms) if keyword in w.lower()]

def delete_wisdom_by_index(index):
    wisdoms = load_wisdoms()
    if 0 <= index < len(wisdoms):
        removed = wisdoms.pop(index)
        save_wisdoms(wisdoms)
        return removed
    return None
