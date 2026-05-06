from flask import Flask, request, jsonify
from flask_cors import CORS
from paaohjelma import *
from blackjack import aloitustila, hit, stand, serialisoi

app = Flask(__name__)
CORS(app)

# Blackjack / Ruotsi2
BLACKJACK_PELI = None
BLACKJACK_VOITOT = 0
RUOTSI_AVATTU = False

# Matikka / Italia
MATIKKA_TEHTAVAT = [
    {"kysymys": "7 * 7", "vastaus": 49},
    {"kysymys": "2000 / 20", "vastaus": 100},
    {"kysymys": "Paljonko on 15 % numerosta 350?", "vastaus": 52.5},
    {"kysymys": "6 * 11", "vastaus": 66},
    {"kysymys": "9 * 250", "vastaus": 2250}
]

MATIKKA_OIKEIN = 0
ITALIA_AVATTU = False
MATIKKA_KYSYMYS = None
MATIKKA_VASTAUS = None
MATIKKA_INDEKSI = 0


def seuraava_matiikkatehtava():
    global MATIKKA_KYSYMYS, MATIKKA_VASTAUS, MATIKKA_INDEKSI

    tehtava = MATIKKA_TEHTAVAT[MATIKKA_INDEKSI]
    MATIKKA_KYSYMYS = tehtava["kysymys"]
    MATIKKA_VASTAUS = tehtava["vastaus"]
    return MATIKKA_KYSYMYS


@app.route("/api/aloita", methods=["POST"])
def api_aloita():
    global BLACKJACK_PELI, BLACKJACK_VOITOT, RUOTSI_AVATTU
    global MATIKKA_OIKEIN, ITALIA_AVATTU, MATIKKA_KYSYMYS, MATIKKA_VASTAUS, MATIKKA_INDEKSI

    data = request.get_json()
    nimi = data["nimi"]
    difficulty = data["difficulty"]
    jatka = data.get("jatka")
    aloitus = "EFHK"

    vanha_peli = hae_pelaajan_peli(nimi)

    # Jos pelaajalta löytyy vanha peli, ei resetata sitä heti.
    # Ensin kerrotaan frontendille, että vanha peli löytyi.
    if vanha_peli and jatka is None:
        return jsonify({
            "status": "vanha_peli",
            "message": "Pelaajalle löytyi tallennettu peli.",
            "co2": vanha_peli["co2_consumed"],
            "budget": vanha_peli["co2_budget"],
            "current_item": vanha_peli["current_item"],
            "difficulty": vanha_peli["difficulty"]
        })

    # Minipelien tila nollataan, kun selainpelisessio käynnistyy.
    BLACKJACK_PELI = None
    BLACKJACK_VOITOT = 0
    RUOTSI_AVATTU = False

    MATIKKA_OIKEIN = 0
    ITALIA_AVATTU = False
    MATIKKA_KYSYMYS = None
    MATIKKA_VASTAUS = None
    MATIKKA_INDEKSI = 0

    if vanha_peli and jatka is True:
        # Jatketaan vanhaa peliä ilman resetointia
        game_id = vanha_peli["id"]
        status = "jatkettu"

    elif vanha_peli:
        # Käyttäjä valitsi aloittaa alusta
        resetoi_peli(vanha_peli["id"], aloitus, difficulty)
        game_id = vanha_peli["id"]
        status = "uusi"

    else:
        # Pelaajalla ei ollut vanhaa peliä
        game_id = luo_peli(nimi, aloitus, difficulty)
        status = "uusi"

    peli = hae_peli(game_id)
    esineet = hae_esineet()

    if peli["current_item"] >= len(esineet):
        return jsonify({
            "status": "win",
            "game_id": game_id,
            "message": "Olet jo löytänyt kaikki esineet. Voit aloittaa uuden pelin samalla nimellä valitsemalla 'Aloita alusta'.",
            "co2": peli["co2_consumed"],
            "budget": peli["co2_budget"]
        })

    esine = esineet[peli["current_item"]]

    return jsonify({
        "status": status,
        "game_id": game_id,
        "hint": anna_vihje(esine, peli["attempts"]),
        "co2": peli["co2_consumed"],
        "budget": peli["co2_budget"]
    })


@app.route("/api/lenna", methods=["POST"])
def api_lenna():
    global RUOTSI_AVATTU, ITALIA_AVATTU

    data = request.get_json()
    game_id = data["game_id"]
    kohde_maa = data["iso_country"]

    # Ruotsi vaatii blackjackin
    if kohde_maa == "SE" and not RUOTSI_AVATTU:
        return jsonify({
            "status": "blackjack_required",
            "message": "Ruotsiin lentäminen vaatii blackjack-haasteen. Voita 5 kierrosta."
        })

    # Italia vaatii matikkapelin
    if kohde_maa == "IT" and not ITALIA_AVATTU:
        return jsonify({
            "status": "math_required",
            "message": "Italiaan lentäminen vaatii matikkahaasteen. Ratkaise 5 tehtävää oikein."
        })

    lento = lenna(game_id, kohde_maa)

    if lento["status"] == "game_over":
        return jsonify(lento)

    esineet = hae_esineet()
    esine_tila = tarkista_esine(game_id, kohde_maa, esineet)

    peli = hae_peli(game_id)

    if peli["current_item"] >= len(esineet):
        return jsonify({
            "status": "win",
            "message": "Voitit pelin!"
        })

    seuraava_esine = esineet[peli["current_item"]]

    # UUSI KOHTA: haetaan tarina vain silloin, kun esine löytyi
    tarina = None

    if esine_tila == "loydetty":
        loydetty_esine = None

        for esine in esineet:
            if esine["iso_country"] == kohde_maa:
                loydetty_esine = esine
                break

        if loydetty_esine is not None:
            tarina = hae_esineen_tarina_ja_kuva(loydetty_esine)

    return jsonify({
        **lento,
        "found_item": esine_tila == "loydetty",
        "item_status": esine_tila,
        "hint": anna_vihje(seuraava_esine, peli["attempts"]),
        "tarina": tarina
    })


# -------------------------
# BLACKJACK / RUOTSI
# -------------------------

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


# -------------------------
# MATIKKA / ITALIA
# -------------------------

@app.route("/api/matikka/aloita", methods=["POST"])
def matikka_aloita():
    global MATIKKA_OIKEIN, MATIKKA_KYSYMYS, MATIKKA_VASTAUS, MATIKKA_INDEKSI

    MATIKKA_OIKEIN = 0
    MATIKKA_INDEKSI = 0
    kysymys = seuraava_matiikkatehtava()

    return jsonify({
        "kysymys": kysymys,
        "oikein": MATIKKA_OIKEIN,
        "valmis": False,
        "viesti": "Ratkaise tehtävä ennen ajan loppumista."
    })


@app.route("/api/matikka/vastaa", methods=["POST"])
def matikka_vastaa():
    global MATIKKA_OIKEIN, ITALIA_AVATTU, MATIKKA_VASTAUS, MATIKKA_INDEKSI

    data = request.get_json()
    vastaus = data.get("vastaus")

    oikein = False

    try:
        annettu = float(vastaus)
        if annettu == float(MATIKKA_VASTAUS):
            oikein = True
    except:
        oikein = False

    if oikein:
        MATIKKA_OIKEIN += 1
        MATIKKA_INDEKSI += 1

    if MATIKKA_OIKEIN >= 5:
        ITALIA_AVATTU = True
        return jsonify({
            "oikein": MATIKKA_OIKEIN,
            "valmis": True,
            "viesti": "Hienoa! Ratkaisit 5 tehtävää oikein. Nyt voit lentää Italiaan."
        })

    if oikein:
        kysymys = seuraava_matiikkatehtava()
        return jsonify({
            "kysymys": kysymys,
            "oikein": MATIKKA_OIKEIN,
            "valmis": False,
            "onnistuiko": True,
            "viesti": "Oikein!"
        })
    else:
        return jsonify({
            "kysymys": MATIKKA_KYSYMYS,
            "oikein": MATIKKA_OIKEIN,
            "valmis": False,
            "onnistuiko": False,
            "viesti": "Väärä vastaus tai aika loppui. Yritä samaa tehtävää uudestaan."
        })


if __name__ == "__main__":
    app.run(debug=True)