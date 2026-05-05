import mysql.connector
from geopy import distance
import Tarinat

yhteys = mysql.connector.connect(
    host='localhost',
    port=3306,
    database='ohjelmistopeli',
    user='lauri',
    password='090799',
    autocommit=True
)
#laurin
tarina_funktiot = {
    "Kirje": Tarinat.kirje,
    "Kultainen teelusikka": Tarinat.teelusikka,
    "Kaulakoru": Tarinat.kaulakoru,
    "Nahkahanskat": Tarinat.nahkahanskat,
    "Taskukello": Tarinat.taskukello
}
def hae_pelaajan_esineet(game_id):
    sql = "SELECT item.* FROM item JOIN game_items ON item.id = game_items.item_id WHERE game_items.game_id = %s"
    cursor = yhteys.cursor(dictionary=True)
    cursor.execute(sql, (game_id,))
    tulos = cursor.fetchall()
    cursor.close()
    return tulos


def lisaa_esine_pelaajalle(game_id, item_id):
    sql = "INSERT INTO game_items (game_id, item_id) VALUES (%s, %s)"
    cursor = yhteys.cursor()
    cursor.execute(sql, (game_id, item_id))
    yhteys.commit()
    cursor.close()

#laurin
def hae_maan_nimi(iso_koodi):
    sql = 'SELECT name FROM country WHERE iso_country = %s'
    cursor = yhteys.cursor(dictionary=True)
    cursor.execute(sql, [iso_koodi])
    tulos = cursor.fetchone()
    cursor.close()
    return tulos["name"]
#laurin
def resetoi_peli(game_id, aloitus_icao, difficulty):
    sql = 'UPDATE game SET location=%s, co2_consumed=0, current_item=0, attempts=0, difficulty=%s WHERE id=%s'
    cursor = yhteys.cursor()
    cursor.execute(sql, (aloitus_icao, difficulty, game_id))
    yhteys.commit()
    cursor.close()
#aleksin
def hae_maan_iso_koodi(nimi):
    sql = 'SELECT iso_country FROM country WHERE name = %s'
    cursor = yhteys.cursor(dictionary=True)
    cursor.execute(sql, (nimi,))
    tulos = cursor.fetchone()
    cursor.close()
    if tulos:
        return tulos["iso_country"]
#aleksin
def hae_esineet():
    cursor = yhteys.cursor(dictionary=True)
    cursor.execute("SELECT * FROM item")
    tulos = cursor.fetchall()
    cursor.close()
    return tulos
#aleksin
def hae_maan_paakentta(maa):
    sql = 'SELECT airport.ident FROM airport WHERE iso_country = %s ORDER BY type = "large_airport" DESC LIMIT 1'
    cursor = yhteys.cursor()
    cursor.execute(sql, (maa,))
    tulos = cursor.fetchone()
    return tulos[0] if tulos else None
#pietarin
def lentokentta(icao):
    sql = "SELECT ident, name, latitude_deg, longitude_deg FROM airport WHERE ident = %s"
    cursor = yhteys.cursor(dictionary=True)
    cursor.execute(sql, (icao,))
    return cursor.fetchone()
#pietarin
def etaisyys(icao1, icao2):
    k1 = lentokentta(icao1)
    k2 = lentokentta(icao2)
    p1 = (k1["latitude_deg"], k1["longitude_deg"])
    p2 = (k2["latitude_deg"], k2["longitude_deg"])
    return distance.distance(p1, p2).km
#pietari
def vaikeustaso(km, difficulty):
    if difficulty == 'HELPPO':
        return km * 0.2
    elif difficulty == 'KESKIVAIKEA':
        return km * 0.4
    elif difficulty == 'VAIKEA':
        return km * 0.5
#laurin
def luo_peli(nimi, aloitus_icao, difficulty):
    sql = 'INSERT INTO game (screen_name, location, co2_consumed, co2_budget, current_item, attempts, difficulty) VALUES (%s, %s, 0, 5000, 0, 0, %s)'
    cursor = yhteys.cursor()
    cursor.execute(sql, (nimi, aloitus_icao, difficulty))
    yhteys.commit()
    return cursor.lastrowid
#pietari
def hae_peli(game_id):
    cursor = yhteys.cursor(dictionary=True)
    cursor.execute("SELECT * FROM game WHERE id = %s", (game_id,))
    return cursor.fetchone()
#laurin ja aleksin
def paivita_peli(game_id, location, co2_consumed, current_item, attempts, difficulty):
    sql = 'UPDATE game SET location=%s, co2_consumed=%s, current_item=%s, attempts=%s, difficulty=%s WHERE id=%s'
    cursor = yhteys.cursor()
    cursor.execute(sql, (location, co2_consumed, current_item, attempts, difficulty, game_id))
    yhteys.commit()
#aleksin
def anna_vihje(esine, yritykset):
    if yritykset == 0:
        return esine["vihje1"]
    elif yritykset == 1:
        return esine["vihje2"]
    else:
        return esine["vihje3"]
#aleksin
def tarkista_maa(pelaajan_maa, esine):
    return pelaajan_maa == esine["iso_country"]
#laurin
def lenna(game_id, kohde_maa):
    peli = hae_peli(game_id)
    nykyinen_icao = peli["location"]
    kohde_icao = hae_maan_paakentta(kohde_maa)

    if kohde_icao is None:
        return {
            "status": "error",
            "message": "Tuntematon maa."
        }

    km = etaisyys(nykyinen_icao, kohde_icao)
    paasto = vaikeustaso(km, peli["difficulty"])
    uusi_kulutus = peli["co2_consumed"] + paasto

    paivita_peli(
        game_id,
        kohde_icao,
        uusi_kulutus,
        peli["current_item"],
        peli["attempts"],
        peli["difficulty"]
    )

    maan_nimi = hae_maan_nimi(kohde_maa)

    if uusi_kulutus > peli["co2_budget"]:
        return {
            "status": "game_over",
            "country": maan_nimi,
            "km": round(km, 1),
            "co2": round(uusi_kulutus, 1),
            "budget": peli["co2_budget"],
            "message": "Peli loppui, koska CO2-budjetti ylittyi."
        }

    return {
        "status": "ok",
        "country": maan_nimi,
        "iso_country": kohde_maa,
        "km": round(km, 1),
        "co2": round(uusi_kulutus, 1),
        "budget": peli["co2_budget"]
    }
#laurin
def hae_pelaajan_peli(nimi):
    cursor = yhteys.cursor(dictionary=True)
    cursor.execute('SELECT * FROM game WHERE screen_name = %s ORDER BY id DESC LIMIT 1', [nimi])
    return cursor.fetchone()

#aleksin
def tarkista_esine(game_id, pelaajan_maa, esineet):
    peli = hae_peli(game_id)
    indeksi = peli["current_item"]
    yritykset = peli["attempts"]
    esine = esineet[indeksi]
    if tarkista_maa(pelaajan_maa, esine):
        print(f"Löysit esineen: {esine['nimi']}")
        if esine["nimi"] in tarina_funktiot:
            for rivi in tarina_funktiot[esine["nimi"]]():
                print(rivi)

        # TÄMÄ LISÄTÄÄN:
        lisaa_esine_pelaajalle(game_id, esine["id"])

        paivita_peli(game_id, peli["location"], peli["co2_consumed"], indeksi + 1, 0, peli["difficulty"])
        return True
    else:
        print("Lensit väärään maahan, TOLLO!")
        print("Vihje:", anna_vihje(esine, yritykset))
        yritykset += 1
        paivita_peli(game_id, peli["location"], peli["co2_consumed"], indeksi, yritykset, peli["difficulty"])
        return False

#Peli alkaa
def komentorivipeli():
    # Peli alkaa
    nimi = input("Anna pelaajan nimi: ")
    vanha_peli = hae_pelaajan_peli(nimi)

    if vanha_peli:
        print(f"Löydettiin tallennettu peli pelaajalle {nimi}.")
        print(f"Nykyinen maa: {vanha_peli['location']}")
        print(f"CO2-kulutus: {vanha_peli['co2_consumed']} / {vanha_peli['co2_budget']}")
        print(f"Löydettyjä mummon esineitä: {vanha_peli['current_item']}")
        print(f"Vaikeustaso: {vanha_peli['difficulty']}")
        jatka = input("Haluatko jatkaa tallennettua peliä? (KYLLÄ/EN): ").upper()

        if jatka == "KYLLÄ":
            game_id = vanha_peli["id"]
            print(f"Peli jatkuu! Olet kuluttanut CO2:sta {vanha_peli['co2_consumed']}. Muista, että budjetti on 5000!")
        else:
            for rivi in Tarinat.johdanto():
                print(rivi)
            print("Peli alkaa! CO2-budjetti: 5000")
            aloitus = "EFHK"
            difficulty = input("Valitse vaikeustaso (HELPPO/KESKIVAIKEA/VAIKEA): ").upper()
            resetoi_peli(vanha_peli["id"], aloitus, difficulty)
            game_id = vanha_peli["id"]
    else:
        for rivi in Tarinat.johdanto():
            print(rivi)
        print("Peli alkaa! CO2-budjetti: 5000")
        aloitus = "EFHK"
        difficulty = input("Valitse vaikeustaso (HELPPO/KESKIVAIKEA/VAIKEA): ").upper()
        game_id = luo_peli(nimi, aloitus, difficulty)

    esineet = hae_esineet()

    peli_ohi = False

    while peli_ohi == False:
        peli_tila = hae_peli(game_id)

        if peli_tila["current_item"] >= len(esineet):
            print("Onneksi olkoon, olet löytänyt kaikki mummon hävittäneet esineet. Mummosi on sinulle ikuisesti kiitollinen.")
            peli_ohi = True
            continue

        esine = esineet[peli_tila["current_item"]]
        print("Vihje:", anna_vihje(esine, peli_tila["attempts"]))

        maan_nimi = input("Mihin maahan haluat lentää? ")

        if maan_nimi == "lopeta":
            print("Lopetit pelin. Pelisi on tallennettu.")
            peli_ohi = True
            continue

        pelaajan_maa = hae_maan_iso_koodi(maan_nimi)

        if not pelaajan_maa:
            print("Tuntematon maa. Syötä haluamasi maa uudelleen.")
            continue

        tila = lenna(game_id, pelaajan_maa)

        if tila == "peli loppuu":
            print("Peli loppui, koska ylitit mummon antaman CO2-budjetin. Mummo on nyt pettynyt sinuun.")
            peli_ohi = True
            continue

        tarkista_esine(game_id, pelaajan_maa, esineet)

    esineet = hae_pelaajan_esineet(game_id)

    print("Löysit nämä esineet:")
    for e in esineet:
        print("-", e["nimi"])

if __name__ == "__main__":
    komentorivipeli()