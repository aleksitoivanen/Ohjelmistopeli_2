import os
from flask import Flask, jsonify, send_from_directory
from blackjack import aloitustila, hit, stand, serialisoi

BASE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(BASE, ".."))
FRONT = os.path.join(ROOT, "frontend")

app = Flask(__name__, static_folder=FRONT, static_url_path="")

PELI = aloitustila()

@app.route("/")
def index():
    return send_from_directory(FRONT, "BLACKJACK.html")


@app.get("/api/uusi")
def api_uusi():
    global PELI
    PELI = aloitustila()
    return jsonify(serialisoi(PELI))


@app.post("/api/hit")
def api_hit():
    global PELI
    PELI = hit(PELI)
    return jsonify(serialisoi(PELI))


@app.post("/api/stand")
def api_stand():
    global PELI
    PELI = stand(PELI)
    return jsonify(serialisoi(PELI))


if __name__ == "__main__":
    app.run(debug=True)
