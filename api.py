from flask import Blueprint, jsonify
import json
import os

api = Blueprint("api", __name__)

WISDOM_FILE = os.path.join(os.getcwd(), "wisdom.json")

@api.route("/api/wisdoms", methods=["GET"])
def get_all_wisdoms():
    try:
        with open(WISDOM_FILE, "r", encoding="utf-8") as f:
            wisdoms = json.load(f)
        return jsonify(wisdoms), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
