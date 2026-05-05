from flask import Flask, request, jsonify
from flask_cors import CORS
from paaohjelma import *
from blackjack import aloitustila, hit, stand, serialisoi
app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})

@app.after_request
def after_request(response):
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add("Access-Control-Allow-Headers", "Content-Type,Authorization")
    response.headers.add("Access-Control-Allow-Methods", "GET,POST,OPTIONS")
    return response

BLACKJACK_PELI = None
BLACKJACK_WINS = 0
BLACKJACK_ACTIVE = False
@app.route("/api/aloita", methods=["POST"])
def api_aloita():
    data = request.get_json()

    nimi = data["nimi"]
    difficulty = data["difficulty"]
    aloitus = "EFHK"

    vanha_peli = hae_pelaajan_peli(nimi)

    if vanha_peli:
        resetoi_peli(vanha_peli["id"], aloitus, difficulty)
        game_id = vanha_peli["id"]
    else:
        game_id = luo_peli(nimi, aloitus, difficulty)

    peli = hae_peli(game_id)
    esineet = hae_esineet()
    esine = esineet[peli["current_item"]]

    return jsonify({
        "game_id": game_id,
        "hint": anna_vihje(esine, peli["attempts"]),
        "co2": peli["co2_consumed"],
        "budget": peli["co2_budget"]
    })

@app.route("/api/lenna", methods=["POST"])
def api_lenna():
    data = request.get_json()

    game_id = data["game_id"]
    kohde_maa = data["iso_country"]

    lento = lenna(game_id, kohde_maa)

    if lento["status"] == "game_over":
        return jsonify(lento)

    esineet = hae_esineet()
    osui = tarkista_esine(game_id, kohde_maa, esineet)

    peli = hae_peli(game_id)

    if peli["current_item"] >= len(esineet):
        return jsonify({
            "status": "win",
            "message": "Voitit pelin!"
        })

    seuraava_esine = esineet[peli["current_item"]]

    return jsonify({
        **lento,
        "found_item": osui,
        "hint": anna_vihje(seuraava_esine, peli["attempts"])
    })
@app.route("/api/blackjack/start", methods=["POST"])
def blackjack_start():
    global BLACKJACK_PELI, BLACKJACK_WINS, BLACKJACK_ACTIVE

    BLACKJACK_PELI = aloitustila()
    BLACKJACK_WINS = 0
    BLACKJACK_ACTIVE = True

    return jsonify(serialisoi(BLACKJACK_PELI))


@app.route("/api/blackjack/hit", methods=["POST"])
def blackjack_hit():
    global BLACKJACK_PELI

    BLACKJACK_PELI = hit(BLACKJACK_PELI)
    return jsonify(serialisoi(BLACKJACK_PELI))


@app.route("/api/blackjack/stand", methods=["POST"])
def blackjack_stand():
    global BLACKJACK_PELI, BLACKJACK_WINS, BLACKJACK_ACTIVE

    BLACKJACK_PELI = stand(BLACKJACK_PELI)
    data = serialisoi(BLACKJACK_PELI)

    if data["tila"] in ["jakaja_yli", "Sinä_voittit"]:
        BLACKJACK_WINS += 1

    if BLACKJACK_WINS >= 5:
        BLACKJACK_ACTIVE = False
        data["valmis"] = True
    else:
        data["valmis"] = False
        data["voitot"] = BLACKJACK_WINS

    return jsonify(data)

@app.route("/api/resetoi", methods=["POST", "OPTIONS"])
def api_resetoi():
    if request.method == "OPTIONS":
        return jsonify({"status": "ok"}), 200

    try:
        data = request.get_json() or {}
        nimi = data.get("nimi", "").strip()
        difficulty = data.get("difficulty", "HELPPO")
        aloitus = "EFHK"

        if nimi == "":
            return jsonify({
                "status": "error",
                "message": "Käyttäjätunnus puuttuu."
            }), 400

        vanha_peli = hae_pelaajan_peli(nimi)

        if vanha_peli:
            game_id = vanha_peli["id"]
            resetoi_peli(game_id, aloitus, difficulty)
            message = "Peli resetoitiin ja aloitettiin alusta!"
        else:
            game_id = luo_peli(nimi, aloitus, difficulty)
            message = "Uusi peli luotiin!"

        peli = hae_peli(game_id)
        esineet = hae_esineet()

        if not esineet:
            return jsonify({
                "status": "error",
                "message": "Item-taulusta ei löytynyt yhtään esinettä."
            }), 500

        esine = esineet[peli["current_item"]]

        return jsonify({
            "status": "ok",
            "game_id": game_id,
            "message": message,
            "hint": anna_vihje(esine, peli["attempts"]),
            "co2": round(peli["co2_consumed"], 1),
            "budget": peli["co2_budget"]
        })

    except Exception as e:
        print("Virhe /api/resetoi:", e)
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

if __name__ == "__main__":
    app.run(debug=True)