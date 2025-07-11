from flask import Flask, render_template, request, redirect, url_for
import json
import os

app = Flask(__name__)

WISDOM_FILE = os.path.join(os.getcwd(), "wisdom.json")

def load_wisdoms():
    if not os.path.exists(WISDOM_FILE):
        return []
    with open(WISDOM_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_wisdoms(wisdoms):
    with open(WISDOM_FILE, "w", encoding="utf-8") as f:
        json.dump(wisdoms, f, ensure_ascii=False, indent=2)

@app.route("/wisdoms", methods=["GET", "POST"])
def list_wisdoms():
    if request.method == "POST":
        new_wisdom = request.form.get("new_wisdom", "").strip()
        if new_wisdom:
            wisdoms = load_wisdoms()
            if new_wisdom not in wisdoms:
                wisdoms.append(new_wisdom)
                save_wisdoms(wisdoms)
        return redirect(url_for("list_wisdoms"))

    wisdoms = load_wisdoms()
    return render_template("wisdom_list.html", wisdoms=wisdoms)

@app.route("/delete/<int:index>", methods=["POST"])
def delete_wisdom(index):
    wisdoms = load_wisdoms()
    if 0 <= index < len(wisdoms):
        wisdoms.pop(index)
        save_wisdoms(wisdoms)
    return redirect(url_for("list_wisdoms"))

if __name__ == "__main__":
    app.run(debug=True)
