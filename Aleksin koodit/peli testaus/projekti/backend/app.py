from flask import Flask, request, jsonify
from flask_cors import CORS
from paaohjelma import *
from blackjack import aloitustila, hit, stand, serialisoi

app = Flask(__name__)
CORS(app)

BLACKJACK_PELI = None
BLACKJACK_VOITOT = 0
RUOTSI_AVATTU = False


@app.route("/api/aloita", methods=["POST"])
def api_aloita():
    global BLACKJACK_PELI, BLACKJACK_VOITOT, RUOTSI_AVATTU

    data = request.get_json()
    nimi = data["nimi"]
    difficulty = data["difficulty"]
    aloitus = "EFHK"

    # Resetoidaan blackjack-haaste uutta peliä varten
    BLACKJACK_PELI = None
    BLACKJACK_VOITOT = 0
    RUOTSI_AVATTU = False

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
    global RUOTSI_AVATTU

    data = request.get_json()
    game_id = data["game_id"]
    kohde_maa = data["iso_country"]

    # Ruotsiin pääsee vain blackjack-haasteen jälkeen
    if kohde_maa == "SE" and not RUOTSI_AVATTU:
        return jsonify({
            "status": "blackjack_required",
            "message": "Ruotsiin lentäminen vaatii blackjack-haasteen. Voita 5 kierrosta."
        })

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


@app.route("/api/blackjack/aloita", methods=["POST"])
def blackjack_aloita():
    global BLACKJACK_PELI, BLACKJACK_VOITOT

    BLACKJACK_PELI = aloitustila()
    BLACKJACK_VOITOT = 0

    data = serialisoi(BLACKJACK_PELI)
    data["voitot"] = BLACKJACK_VOITOT
    data["valmis"] = False
    data["kierros_loppui"] = False
    return jsonify(data)


@app.route("/api/blackjack/uusi", methods=["POST"])
def blackjack_uusi():
    global BLACKJACK_PELI, BLACKJACK_VOITOT

    BLACKJACK_PELI = aloitustila()

    data = serialisoi(BLACKJACK_PELI)
    data["voitot"] = BLACKJACK_VOITOT
    data["valmis"] = False
    data["kierros_loppui"] = False
    return jsonify(data)


@app.route("/api/blackjack/hit", methods=["POST"])
def blackjack_hit():
    global BLACKJACK_PELI, BLACKJACK_VOITOT

    if BLACKJACK_PELI is None:
        BLACKJACK_PELI = aloitustila()

    BLACKJACK_PELI = hit(BLACKJACK_PELI)
    data = serialisoi(BLACKJACK_PELI)

    kierros_loppui = data["tila"] != "pelaa"

    data["voitot"] = BLACKJACK_VOITOT
    data["valmis"] = False
    data["kierros_loppui"] = kierros_loppui
    return jsonify(data)


@app.route("/api/blackjack/stand", methods=["POST"])
def blackjack_stand():
    global BLACKJACK_PELI, BLACKJACK_VOITOT, RUOTSI_AVATTU

    if BLACKJACK_PELI is None:
        BLACKJACK_PELI = aloitustila()

    BLACKJACK_PELI = stand(BLACKJACK_PELI)
    data = serialisoi(BLACKJACK_PELI)

    if data["tila"] in ["jakaja_yli", "pelaaja_voitti"]:
        BLACKJACK_VOITOT += 1

    if BLACKJACK_VOITOT >= 5:
        RUOTSI_AVATTU = True
        data["valmis"] = True
        data["viesti"] = "Hienoa! Voitit 5 kertaa. Nyt voit lentää Ruotsiin."
    else:
        data["valmis"] = False

    data["voitot"] = BLACKJACK_VOITOT
    data["kierros_loppui"] = True

    return jsonify(data)


if __name__ == "__main__":
    app.run(debug=True)