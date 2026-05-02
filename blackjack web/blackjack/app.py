from flask import Flask, jsonify, request, send_from_directory
from blackjack import aloitustila, hit, stand, serialisoi

app = Flask(__name__, static_folder="../frontend", static_url_path="")

PELI = aloitustila()


@app.route("/")
def index():
    return send_from_directory("../frontend", "index.html")


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
