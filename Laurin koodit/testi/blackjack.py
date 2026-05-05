import random

KORTTIARVOT = {
    "2": 2, "3": 3, "4": 4, "5": 5, "6": 6,
    "7": 7, "8": 8, "9": 9, "10": 10,
    "J": 10, "Q": 10, "K": 10, "A": 11
}

RANGIT = list(KORTTIARVOT.keys())
MAAT = ["♠", "♥", "♦", "♣"] #löyty netistä merkit näille valmiiks


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
        "tila": "pelaa",  # pelaa / pelaaja_yli / jakaja_yli / pelaaja_voitti / jakaja_voitti / tasapeli ja kaikki eri vaihtoehdot
        "viesti": "Hit tai Stand"
    }


def hit(tila):
    if tila["tila"] != "pelaa":
        return tila
    tila["pelaaja"].append(tila["pakka"].pop())
    if kasiarvo(tila["pelaaja"]) > 21:
        tila["tila"] = "pelaaja_yli"
        tila["viesti"] = "Pelaaja meni yli! Hävisit."
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
        tila["viesti"] = "Jakaja meni yli! Sinä Voitit!"
    elif pelaaja > jakaja:
        tila["tila"] = "Sinä_voittit"
        tila["viesti"] = "Voitit!"
    elif pelaaja < jakaja:
        tila["tila"] = "jakaja_voitti"
        tila["viesti"] = "Hävisit."
    else:
        tila["tila"] = "tasapeli"
        tila["viesti"] = "Tasapeli."

    return tila


def serialisoi(tila):
    def fmt(kasi): #tää fmt vain muokkaa listaa helpommaksi.
        return [f"{r}{m}" for r, m in kasi]

    return {
        "pelaaja": fmt(tila["pelaaja"]),
        "jakaja": fmt(tila["jakaja"]),
        "pelaajaArvo": kasiarvo(tila["pelaaja"]),
        "jakajaArvo": kasiarvo(tila["jakaja"]) if tila["tila"] != "pelaa" else None,
        "tila": tila["tila"],
        "viesti": tila["viesti"]
    }
#pitää vielä lisätä co2 +100 ja -100