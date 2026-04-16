class Peli:
    def __init__(self, data: dict):
        self.id = data["id"]
        self.nimi = data["screen_name"]
        self.sijainti = data["location"]
        self.kulutus = data["co2_consumed"]
        self.budjetti = data["co2_budget"]
        self.esine_indeksi = data["current_item"]
        self.yritykset = data["attempts"]
        self.vaikeus = data["difficulty"]

    def to_dict(self):
        return {
            "id": self.id,
            "nimi": self.nimi,
            "sijainti": self.sijainti,
            "kulutus": self.kulutus,
            "budjetti": self.budjetti,
            "esine_indeksi": self.esine_indeksi,
            "yritykset" : self.yritykset,
            "vaikeus": self.vaikeus
        }

        