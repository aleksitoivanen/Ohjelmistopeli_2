def hae_peli(game_id):
    cursor = yhteys.curcsor(dictionary=True)
    cursor.execute("SELECT * FROM game WHERE id = %s", (game_id,))
    data = cursor.fetchone()
    cursor.close()
    return Peli(data) if data else None