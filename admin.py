import os
import json
from flask import Flask, request, render_template, redirect, url_for, session, flash
from functools import wraps

app = Flask(__name__)
app.secret_key = os.getenv("ADMIN_SECRET_KEY", "supersecretkey")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "admin123")

WISDOM_PATH = os.path.join(os.path.dirname(__file__), "wisdom.json")


def load_wisdoms():
    if not os.path.exists(WISDOM_PATH):
        return []
    with open(WISDOM_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def save_wisdoms(wisdoms):
    with open(WISDOM_PATH, "w", encoding="utf-8") as f:
        json.dump(wisdoms, f, ensure_ascii=False, indent=2)


def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if not session.get("logged_in"):
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return wrapper


@app.route("/", methods=["GET", "POST"])
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        if request.form.get("password") == ADMIN_PASSWORD:
            session["logged_in"] = True
            return redirect(url_for("list_wisdoms"))
        else:
            flash("Неверный пароль")
    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


@app.route("/wisdoms", methods=["GET", "POST"])
@login_required
def list_wisdoms():
    wisdoms = load_wisdoms()

    if request.method == "POST":
        new_wisdom = request.form.get("new_wisdom", "").strip()
        if new_wisdom and new_wisdom not in wisdoms:
            wisdoms.append(new_wisdom)
            save_wisdoms(wisdoms)
            flash("✅ Добавлено!")
        elif new_wisdom:
            flash("⚠️ Такая мудрость уже существует.")

    query = request.args.get("q", "").strip().lower()
    filtered = [w for w in wisdoms if query in w.lower()] if query else wisdoms

    return render_template("wisdom_list.html", wisdoms=filtered, query=query)


@app.route("/delete/<int:index>")
@login_required
def delete_wisdom(index):
    wisdoms = load_wisdoms()
    if 0 <= index < len(wisdoms):
        removed = wisdoms.pop(index)
        save_wisdoms(wisdoms)
        flash(f"🗑 Удалено: {removed[:50]}")
    return redirect(url_for("list_wisdoms"))
