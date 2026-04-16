def lentokentta(icao):
    cursor = yhteys.cursor(dictionary=True)
    cursor.execute(
        "SELECT ident, name, latitude_deg, longitude_deg FROM airport WHERE ident = %s",
        (icao,)
    )
    row = cursor.fetchone()
    cursor.close()

    if row:
        return Airport(row)
    return None
