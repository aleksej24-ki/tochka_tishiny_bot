import os
import json
from flask import Flask, request, render_template, redirect, url_for, session
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = "super-secret-key"  # Можно заменить
WISDOM_FILE = "wisdom.json"
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")


def load_wisdoms():
    if not os.path.exists(WISDOM_FILE):
        return []
    with open(WISDOM_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_wisdoms(wisdoms):
    with open(WISDOM_FILE, "w", encoding="utf-8") as f:
        json.dump(wisdoms, f, ensure_ascii=False, indent=2)


@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        if request.form.get("password") == ADMIN_PASSWORD:
            session["admin"] = True
            return redirect(url_for("list_wisdoms"))
        return render_template("login.html", error="❌ Неверный пароль.")
    return render_template("login.html")


@app.route("/logout")
def logout():
    session.pop("admin", None)
    return redirect(url_for("login"))


@app.route("/wisdoms", methods=["GET", "POST"])
def list_wisdoms():
    if not session.get("admin"):
        return redirect(url_for("login"))

    wisdoms = load_wisdoms()
    search = request.args.get("search", "").lower()
    if search:
        wisdoms = [w for w in wisdoms if search in w.lower()]

    if request.method == "POST":
        new_wisdom = request.form.get("new_wisdom", "").strip()
        if new_wisdom and new_wisdom not in wisdoms:
            wisdoms.append(new_wisdom)
            save_wisdoms(wisdoms)
            return redirect(url_for("list_wisdoms"))
    return render_template("wisdom_list.html", wisdoms=wisdoms, search=search)


@app.route("/delete/<int:index>")
def delete(index):
    if not session.get("admin"):
        return redirect(url_for("login"))

    wisdoms = load_wisdoms()
    if 0 <= index < len(wisdoms):
        del wisdoms[index]
        save_wisdoms(wisdoms)
    return redirect(url_for("list_wisdoms"))
