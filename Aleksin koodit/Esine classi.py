class Esine:
    def __init__(self, data: dict):
        self.id = data["id"]
        self.nimi = data["nimi"]
        self.maa = data["maa"]
        self.vihje1 = data["vihje1"]
        self.vihje2 = data["vihje2"]
        self.vihje3 = data["vihje3"]

    def vihje(self, yritykset):
        if yritykset == 0:
            return self.vihje1
        elif yritykset == 1:
            return self.vihje2
        return self.vihje3

    def to_dict(self):
        return {
            "id": self.id,
            "nimi": self.nimi,
            "maa": self.maa,
            "vihje1": self.vihje1,
            "vihje2": self.vihje2,
            "vihje3": self.vihje3
        }
