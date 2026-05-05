from flask import Flask, request, jsonify
from flask_cors import CORS
from Pääohjelma import *

app = Flask(__name__)
CORS(app)

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

if __name__ == "__main__":
    app.run(debug=True)