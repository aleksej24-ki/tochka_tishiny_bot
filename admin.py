from flask import Flask, render_template, request, redirect, url_for
import json
import os

app = Flask(__name__)

WISDOM_PATH = "wisdom.json"

def load_wisdoms():
    if not os.path.exists(WISDOM_PATH):
        return []
    with open(WISDOM_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def save_wisdoms(data):
    with open(WISDOM_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/wisdoms", methods=["GET", "POST"])
def list_wisdoms():
    wisdoms = load_wisdoms()
    if request.method == "POST":
        text = request.form.get("wisdom", "").strip()
        if text:
            if text not in wisdoms:
                wisdoms.append(text)
                save_wisdoms(wisdoms)
        return redirect(url_for("list_wisdoms"))
    return render_template("wisdom_list.html", wisdoms=wisdoms)

@app.route("/wisdoms/delete/<int:index>", methods=["POST"])
def delete_wisdom(index):
    wisdoms = load_wisdoms()
    if 0 <= index < len(wisdoms):
        del wisdoms[index]
        save_wisdoms(wisdoms)
    return redirect(url_for("list_wisdoms"))

if __name__ == "__main__":
    app.run(debug=True)

