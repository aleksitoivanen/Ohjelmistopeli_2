def lenna(game_id, kohde_maa):
    peli = hae_peli(game_id)

    nykyinen_icao = peli.sijainti
    kohde_icao = hae_maan_paakentta(kohde_maa)

    if kohde_icao is None:
        return {"status": "error", "message": "Tuntematon maa."}

    km = etaisyys(nykyinen_icao, kohde_icao)
    paasto = vaikeustaso(km, peli.vaikeus)
    uusi_kulutus = peli.kulutus + paasto

    # CO2-budjetti ylittyy
    if uusi_kulutus > peli.budjetti:
        peli.sijainti = kohde_icao
        peli.kulutus = uusi_kulutus
        paivita_peli(peli)

        return {
            "status": "game_over",
            "co2": uusi_kulutus,
            "budget": peli.budjetti
        }

    maan_nimi = hae_maan_nimi(kohde_maa)

    peli.sijainti = kohde_icao
    peli.kulutus = uusi_kulutus
    paivita_peli(peli)

    return {
        "status": "ok",
        "country_name": maan_nimi,
        "km": km,
        "co2": uusi_kulutus,
        "budget": peli.budjetti
    }
