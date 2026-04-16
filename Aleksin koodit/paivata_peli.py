def paivita_peli(peli: Peli):
    sql = '''
        UPDATE game SET 
            location=%s,
            co2_consumed=%s,
            current_item=%s,
            attempts=%s,
            difficulty=%s
        WHERE id=%s
    '''
    cursor = yhteys.cursor()
    cursor.execute(sql, (
        peli.sijainti,
        peli.kulutus,
        peli.esine_indeksi,
        peli.yritykset,
        peli.vaikeus,
        peli.id
    ))
    yhteys.commit()
    cursor.close()
