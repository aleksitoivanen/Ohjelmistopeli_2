#aleksi
import random

KORTTIARVOT = {
    "2": 2, "3": 3, "4": 4, "5": 5, "6": 6,
    "7": 7, "8": 8, "9": 9, "10": 10,
    "J": 10, "Q": 10, "K": 10, "A": 11
}

RANGIT = list(KORTTIARVOT.keys())
MAAT = ["♠", "♥", "♦", "♣"]


def uusi_pakka():
    pakka = [(r, m) for r in RANGIT for m in MAAT]
    random.shuffle(pakka)
    return pakka


def kasiarvo(kasi):
    arvo = sum(KORTTIARVOT[r] for r, _ in kasi)
    assat = sum(1 for r, _ in kasi if r == "A")

    while arvo > 21 and assat > 0:
        arvo -= 10
        assat -= 1

    return arvo


def aloitustila():
    pakka = uusi_pakka()
    pelaaja = [pakka.pop(), pakka.pop()]
    jakaja = [pakka.pop(), pakka.pop()]

    return {
        "pakka": pakka,
        "pelaaja": pelaaja,
        "jakaja": jakaja,
        "tila": "pelaa",
        "viesti": "Ota kortti tai jää."
    }


def hit(tila):
    if tila["tila"] != "pelaa":
        return tila

    tila["pelaaja"].append(tila["pakka"].pop())

    if kasiarvo(tila["pelaaja"]) > 21:
        tila["tila"] = "pelaaja_yli"
        tila["viesti"] = "Pelaaja meni yli! Hävisit tämän kierroksen."

    return tila


def stand(tila):
    if tila["tila"] != "pelaa":
        return tila

    while kasiarvo(tila["jakaja"]) < 17:
        tila["jakaja"].append(tila["pakka"].pop())

    pelaaja = kasiarvo(tila["pelaaja"])
    jakaja = kasiarvo(tila["jakaja"])

    if jakaja > 21:
        tila["tila"] = "jakaja_yli"
        tila["viesti"] = "Jakaja meni yli! Voitit tämän kierroksen."
    elif pelaaja > jakaja:
        tila["tila"] = "pelaaja_voitti"
        tila["viesti"] = "Voitit tämän kierroksen."
    elif pelaaja < jakaja:
        tila["tila"] = "jakaja_voitti"
        tila["viesti"] = "Jakaja voitti tämän kierroksen."
    else:
        tila["tila"] = "tasapeli"
        tila["viesti"] = "Tasapeli."

    return tila


def serialisoi(tila):
    def fmt(kasi):
        return [f"{r}{m}" for r, m in kasi]

    return {
        "pelaaja": fmt(tila["pelaaja"]),
        "jakaja": fmt(tila["jakaja"]),
        "pelaajaArvo": kasiarvo(tila["pelaaja"]),
        "jakajaArvo": kasiarvo(tila["jakaja"]) if tila["tila"] != "pelaa" else None,
        "tila": tila["tila"],
        "viesti": tila["viesti"]
    }