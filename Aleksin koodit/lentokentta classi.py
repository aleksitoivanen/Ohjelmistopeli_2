class Airport:
    def __init__(self, data: dict):
        self.ident = data["ident"]
        self.name = data["name"]
        self.lat = data["latitude_deg"]
        self.lon = data["longitude_deg"]

    