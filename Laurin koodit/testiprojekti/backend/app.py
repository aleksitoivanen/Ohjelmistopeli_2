from flask import Flask, request, jsonify
from flask_cors import CORS
from paaohjelma import *
from blackjack import aloitustila, hit, stand, serialisoi
import random
import Tarinat

app = Flask(__name__)
CORS(app)

def muodosta_alkutarina():
    return {
        "otsikko": "Mummon viesti",
        "teksti": "\n".join(Tarinat.johdanto()),
        "kuva": ""
    }


def muodosta_voittotarina():
    return {
        "otsikko": "Voitit pelin!",
        "teksti": "Voitit pelin! Löysit kaikki mummon kadottamat esineet. Mummo on sinulle ikuisesti kiitollinen.",
        "kuva": "kuvat/mummo.png"
    }


#aleksi
BLACKJACK_PELI = None
BLACKJACK_VOITOT = 0
RUOTSI_AVATTU = False

#aleksi
MATIKKA_TEHTAVAT = [
    {"kysymys": "7 * 7", "vastaus": 49},
    {"kysymys": "2000 / 20", "vastaus": 100},
    {"kysymys": "Paljonko on 15 % numerosta 350?", "vastaus": 52.5},
    {"kysymys": "6 * 11", "vastaus": 66},
    {"kysymys": "9 * 250", "vastaus": 2000}
]
MATIKKA_OIKEIN = 0
ITALIA_AVATTU = False
MATIKKA_KYSYMYS = None
MATIKKA_VASTAUS = None
MATIKKA_INDEKSI = 0

#pietari
HEPAT = ["Hevonen 1", "Hevonen 2", "Hevonen 3"]
HEPPA_PAJAT = [0, 0, 0]
HEPPA_MAALISSA = []
BRITANNIA_AVATTU = False

#aleksi
def seuraava_matiikkatehtava():
    global MATIKKA_KYSYMYS, MATIKKA_VASTAUS, MATIKKA_INDEKSI

    tehtava = MATIKKA_TEHTAVAT[MATIKKA_INDEKSI]
    MATIKKA_KYSYMYS = tehtava["kysymys"]
    MATIKKA_VASTAUS = tehtava["vastaus"]
    return MATIKKA_KYSYMYS

#yhessä
@app.route("/api/aloita", methods=["POST"])
def api_aloita():
    global BLACKJACK_PELI, BLACKJACK_VOITOT, RUOTSI_AVATTU
    global MATIKKA_OIKEIN, ITALIA_AVATTU, MATIKKA_KYSYMYS, MATIKKA_VASTAUS, MATIKKA_INDEKSI
    global HEPPA_PAJAT, HEPPA_MAALISSA, BRITANNIA_AVATTU

    data = request.get_json()
    nimi = data["nimi"]
    difficulty = data["difficulty"]
    jatka = data.get("jatka")
    aloitus = "EFHK"

    vanha_peli = hae_pelaajan_peli(nimi)

    if vanha_peli and jatka is None:
        return jsonify({
            "status": "vanha_peli",
            "message": "Pelaajalle löytyi tallennettu peli.",
            "co2": vanha_peli["co2_consumed"],
            "budget": vanha_peli["co2_budget"],
            "current_item": vanha_peli["current_item"],
            "difficulty": vanha_peli["difficulty"]
        })

    BLACKJACK_PELI = None
    BLACKJACK_VOITOT = 0
    RUOTSI_AVATTU = False

    MATIKKA_OIKEIN = 0
    ITALIA_AVATTU = False
    MATIKKA_KYSYMYS = None
    MATIKKA_VASTAUS = None
    MATIKKA_INDEKSI = 0

    HEPPA_PAJAT = [0, 0, 0]
    HEPPA_MAALISSA = []
    BRITANNIA_AVATTU = False

    if vanha_peli and jatka is True:
        game_id = vanha_peli["id"]
        status = "jatkettu"
    elif vanha_peli:
        resetoi_peli(vanha_peli["id"], aloitus, difficulty)
        game_id = vanha_peli["id"]
        status = "uusi"
    else:
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
            "budget": peli["co2_budget"],
            "voittotarina": muodosta_voittotarina()
        })

    esine = esineet[peli["current_item"]]

    vastaus = {
        "status": status,
        "game_id": game_id,
        "hint": anna_vihje(esine, peli["attempts"]),
        "co2": peli["co2_consumed"],
        "budget": peli["co2_budget"]
    }

    if status == "uusi":
        vastaus["alkutarina"] = muodosta_alkutarina()

    return jsonify(vastaus)

#aleksi ja lauri
@app.route("/api/lenna", methods=["POST"])
def api_lenna():
    global RUOTSI_AVATTU, ITALIA_AVATTU, BRITANNIA_AVATTU

    data = request.get_json()
    game_id = data["game_id"]
    kohde_maa = data["iso_country"]

    if kohde_maa == "SE" and not RUOTSI_AVATTU:
        return jsonify({
            "status": "blackjack_required",
            "message": "Ruotsiin lentäminen vaatii blackjack-haasteen. Voita 5 kierrosta."
        })

    if kohde_maa == "IT" and not ITALIA_AVATTU:
        return jsonify({
            "status": "math_required",
            "message": "Italiaan lentäminen vaatii matikkahaasteen. Ratkaise 5 tehtävää oikein."
        })

    if kohde_maa == "GB" and not BRITANNIA_AVATTU:
        return jsonify({
            "status": "horse_required",
            "message": "Iso-Britanniaan lentäminen vaatii heppakisan. Valitse hevonen ja voita kisa."
        })

    lento = lenna(game_id, kohde_maa)

    if lento["status"] == "game_over":
        return jsonify(lento)

    esineet = hae_esineet()
    esine_tila = tarkista_esine(game_id, kohde_maa, esineet)
    peli = hae_peli(game_id)
    tarina = None

    if esine_tila == "loydetty":
        loydetty_esine = None

        for esine in esineet:
            if esine["iso_country"] == kohde_maa:
                loydetty_esine = esine
                break

        if loydetty_esine is not None:
            tarina = hae_esineen_tarina_ja_kuva(loydetty_esine)

    vastaus = dict(lento)
    vastaus["found_item"] = esine_tila == "loydetty"
    vastaus["item_status"] = esine_tila
    vastaus["tarina"] = tarina

    if peli["current_item"] >= len(esineet):
        vastaus["status"] = "win"
        vastaus["message"] = "Voitit pelin!"
        vastaus["hint"] = ""
        vastaus["voittotarina"] = muodosta_voittotarina()
        return jsonify(vastaus)

    seuraava_esine = esineet[peli["current_item"]]
    vastaus["hint"] = anna_vihje(seuraava_esine, peli["attempts"])

    return jsonify(vastaus)

#aleksi
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

#aleksi
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


#pietari

@app.route("/api/heppa/aloita", methods=["POST"])
def heppa_aloita():
    global HEPPA_PAJAT, HEPPA_MAALISSA

    HEPPA_PAJAT = [0, 0, 0]
    HEPPA_MAALISSA = []

    return jsonify({
        "positions": HEPPA_PAJAT,
        "finished": HEPPA_MAALISSA
    })


@app.route("/api/heppa/liiku", methods=["POST"])
def heppa_liiku():
    global HEPPA_PAJAT, HEPPA_MAALISSA, BRITANNIA_AVATTU

    data = request.get_json()
    valittu_hevonen = data.get("chosenHorse")

    if len(HEPPA_MAALISSA) >= 1:
        voittaja = HEPPA_MAALISSA[0]
        voitto = voittaja == valittu_hevonen

        if voitto:
            BRITANNIA_AVATTU = True

        return jsonify({
            "positions": HEPPA_PAJAT,
            "finished": HEPPA_MAALISSA,
            "winner": voittaja,
            "won": voitto,
            "valmis": True
        })

    for i in range(len(HEPPA_PAJAT)):
        if HEPAT[i] not in HEPPA_MAALISSA:
            askel = random.randint(1, 6)
            HEPPA_PAJAT[i] += askel

            if HEPPA_PAJAT[i] >= 30 and HEPAT[i] not in HEPPA_MAALISSA:
                HEPPA_MAALISSA.append(HEPAT[i])

    voittaja = HEPPA_MAALISSA[0] if HEPPA_MAALISSA else None
    voitto = voittaja == valittu_hevonen if voittaja else False

    if voitto:
        BRITANNIA_AVATTU = True

    return jsonify({
        "positions": HEPPA_PAJAT,
        "finished": HEPPA_MAALISSA,
        "winner": voittaja,
        "won": voitto,
        "valmis": len(HEPPA_MAALISSA) >= 1
    })


if __name__ == "__main__":
    app.run(debug=True)