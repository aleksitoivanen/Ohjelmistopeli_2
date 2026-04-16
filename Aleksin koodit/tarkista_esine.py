def tarkista_esine(game_id, pelaajan_maa, esineet):
    peli = hae_peli(game_id)

    indeksi = peli.esine_indeksi
    yritykset = peli.yritykset
    esine = esineet[indeksi]

    if pelaajan_maa == esine.maa:

        tarina = []
        if esine.nimi in tarina_funktiot:
            tarina = list(tarina_funktiot[esine.nimi]())

        peli.esine_indeksi = indeksi + 1
        peli.yritykset = 0
        paivita_peli(peli)

        return {
            "correct": True,
            "item_name": esine.nimi,
            "story": tarina
        }


    else:
        vihje = esine.vihje(yritykset)

        peli.yritykset = yritykset + 1
        paivita_peli(peli)

        return {
            "correct": False,
            "hint": vihje,
            "attempts": peli.yritykset
        }
