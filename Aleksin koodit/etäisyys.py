def etaisyys(icao1, icao2):
    k1 = lentokentta(icao1)
    k2 = lentokentta(icao2)
    p1 = (k1.lat, k1.lon)
    p2 = (k2.lat, k2.lon)
    return distance.distance(p1, p2).km
