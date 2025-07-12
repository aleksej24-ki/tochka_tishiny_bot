import os
import json
from flask import Flask, render_template, request, redirect, url_for, session, flash

app = Flask(__name__)
app.secret_key = os.getenv("ADMIN_SECRET_KEY")

WISDOM_FILE = "wisdom.json"

def load_wisdoms():
    if not os.path.exists(WISDOM_FILE):
        return []
    with open(WISDOM_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_wisdoms(data):
    with open(WISDOM_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        password = request.form.get("password")
        if password == os.getenv("ADMIN_PASSWORD"):
            session["logged_in"] = True
            return redirect(url_for("list_wisdoms"))
        else:
            flash("❌ Неверный пароль")
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.pop("logged_in", None)
    return redirect(url_for("login"))

@app.route("/wisdoms", methods=["GET", "POST"])
def list_wisdoms():
    if not session.get("logged_in"):
        return redirect(url_for("login"))

    wisdoms = load_wisdoms()

    if request.method == "POST":
        new_text = request.form.get("new_wisdom", "").strip()
        if new_text and new_text not in wisdoms:
            wisdoms.append(new_text)
            save_wisdoms(wisdoms)
        return redirect(url_for("list_wisdoms"))

    return render_template("wisdom_list.html", wisdoms=wisdoms)

@app.route("/delete/<int:index>", methods=["POST"])
def delete_wisdom(index):
    if not session.get("logged_in"):
        return redirect(url_for("login"))

    wisdoms = load_wisdoms()
    if 0 <= index < len(wisdoms):
        wisdoms.pop(index)
        save_wisdoms(wisdoms)
    return redirect(url_for("list_wisdoms"))

if __name__ == "__main__":
    app.run(debug=True)
