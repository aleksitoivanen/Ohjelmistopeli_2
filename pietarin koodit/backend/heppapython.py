from flask import Flask, send_from_directory, jsonify
import random

app = Flask(
    __name__,
    static_folder="../frontend",
    static_url_path=""
)

hepat = ["Hevonen 1", "Hevonen 2", "Hevonen 3"]

positions = [0, 0, 0]
finished = []

@app.route("/")
def index():
    return send_from_directory(app.static_folder, "heppahtml.html")

@app.route("/reset")
def reset():
    global positions, finished
    positions = [0, 0, 0]
    finished = []
    return jsonify({"status": "reset"})

@app.route("/move")
def move():
    global positions, finished


    if len(finished) >= 1:
        return jsonify({"positions": positions, "finished": finished})

    for i in range(len(positions)):
        if hepat[i] not in finished:
            step = random.randint(1, 6)
            positions[i] += step
            if positions[i] >= 30 and hepat[i] not in finished:
                finished.append(hepat[i])

    return jsonify({"positions": positions, "finished": finished})

if __name__ == "__main__":
    app.run(debug=True)
