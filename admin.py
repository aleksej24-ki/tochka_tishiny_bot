from flask import Flask, render_template_string, request, redirect, url_for
import json
import os

WISDOM_FILE = os.path.join(os.path.dirname(__file__), "wisdom.json")

app = Flask(__name__)

# HTML-шаблон (минимализм)
TEMPLATE = """
<!doctype html>
<title>Admin — Мудрость</title>
<h2>📜 Все мудрости</h2>
<ul>
  {% for i, w in enumerate(wisdoms) %}
    <li>{{ i }}. {{ w }} 
        <a href="{{ url_for('delete_wisdom', index=i) }}">❌ Удалить</a>
    </li>
  {% endfor %}
</ul>

<h3>➕ Добавить мудрость</h3>
<form method="post" action="{{ url_for('add_wisdom') }}">
    <input name="text" size="60">
    <button type="submit">Добавить</button>
</form>
"""

# Загрузка
def load_wisdom():
    if not os.path.exists(WISDOM_FILE):
        return []
    with open(WISDOM_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

# Сохранение
def save_wisdom(data):
    with open(WISDOM_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

@app.route("/")
def index():
    wisdoms = load_wisdom()
    return render_template_string(TEMPLATE, wisdoms=wisdoms)

@app.route("/add", methods=["POST"])
def add_wisdom():
    text = request.form.get("text", "").strip()
    if text:
        data = load_wisdom()
        if text not in data:
            data.append(text)
            save_wisdom(data)
    return redirect(url_for("index"))

@app.route("/delete/<int:index>")
def delete_wisdom(index):
    data = load_wisdom()
    if 0 <= index < len(data):
        del data[index]
        save_wisdom(data)
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True, port=8000)
