def hae_esineet():
    cursor = yhteys.cursor(dictionary=True)
    cursor.execute("SELECT * FROM item")
    rows = cursor.fetchall()
    cursor.close()

    esineet = []
    for r in rows:
        esine = Esine(r)
        esineet.append(esine)

    return esineet
