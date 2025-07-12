import os
from flask import Flask, render_template, request, redirect, session, url_for
import json

app = Flask(__name__)
app.secret_key = os.getenv("ADMIN_SECRET_KEY", "dev-secret")

WISDOM_FILE = "wisdom.json"

def load_wisdoms():
    if os.path.exists(WISDOM_FILE):
        with open(WISDOM_FILE, encoding="utf-8") as f:
            return json.load(f)
    return []

def save_wisdoms(data):
    with open(WISDOM_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

@app.route("/")
def index():
    if not session.get("logged_in"):
        return redirect(url_for("login"))
    return redirect(url_for("list_wisdoms"))

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        password = request.form.get("password")
        if password == os.getenv("ADMIN_SECRET_KEY"):
            session["logged_in"] = True
            return redirect(url_for("list_wisdoms"))
        return render_template("login.html", error="Неверный пароль")
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

@app.route("/wisdoms")
def list_wisdoms():
    if not session.get("logged_in"):
        return redirect(url_for("login"))
    wisdoms = load_wisdoms()
    return render_template("wisdom_list.html", wisdoms=wisdoms)

@app.route("/add", methods=["POST"])
def add_wisdom():
    if not session.get("logged_in"):
        return redirect(url_for("login"))
    text = request.form.get("wisdom")
    if text:
        wisdoms = load_wisdoms()
        if text not in wisdoms:
            wisdoms.append(text)
            save_wisdoms(wisdoms)
    return redirect(url_for("list_wisdoms"))

@app.route("/delete/<int:index>")
def delete_wisdom(index):
    if not session.get("logged_in"):
        return redirect(url_for("login"))
    wisdoms = load_wisdoms()
    if 0 <= index < len(wisdoms):
        del wisdoms[index]
        save_wisdoms(wisdoms)
    return redirect(url_for("list_wisdoms"))
