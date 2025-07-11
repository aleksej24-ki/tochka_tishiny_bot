from flask import Flask, render_template, request, redirect
import os
import json

app = Flask(__name__)
FILE_PATH = os.path.join(os.getcwd(), "wisdom.json")

def load_wisdoms():
    try:
        with open(FILE_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []

def save_wisdoms(data):
    with open(FILE_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

@app.route("/")
def index():
    return redirect("/wisdoms")

@app.route("/wisdoms", methods=["GET"])
def list_wisdoms():
    wisdoms = load_wisdoms()
    return render_template("wisdom_list.html", wisdoms=wisdoms)

@app.route("/add", methods=["POST"])
def add_wisdom():
    new = request.form.get("wisdom", "").strip()
    if new:
        wisdoms = load_wisdoms()
        if new not in wisdoms:  # защита от дубликатов
            wisdoms.append(new)
            save_wisdoms(wisdoms)
    return redirect("/wisdoms")

@app.route("/delete/<int:index>", methods=["POST"])
def delete_wisdom(index):
    wisdoms = load_wisdoms()
    if 0 <= index < len(wisdoms):
        wisdoms.pop(index)
        save_wisdoms(wisdoms)
    return redirect("/wisdoms")

if __name__ == "__main__":
    app.run(debug=True)
