let peliId = null;

// Luo uusi peli
async function uusiPeli() {
    const nimi = document.getElementById("nimi").value;
    const aloitus = document.getElementById("aloitus").value;

    const vastaus = await fetch("/api/uusi_peli", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ nimi: nimi, aloitus: aloitus })
    });

    const data = await vastaus.json();
    peliId = data.peli_id;

    nayta(JSON.stringify(data, null, 2));
}

// Lennä maahan
async function lenna() {
    const kohde = document.getElementById("kohde").value;

    const vastaus = await fetch("/api/lenna", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ peli_id: peliId, kohde: kohde })
    });

    const data = await vastaus.json();
    nayta(JSON.stringify(data, null, 2));
}

// Tarkista esine
async function tarkistaEsine() {
    const maa = document.getElementById("kohde").value;

    const vastaus = await fetch("/api/tarkista_esine", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ peli_id: peliId, maa: maa })
    });

    const data = await vastaus.json();
    nayta(JSON.stringify(data, null, 2));
}

// Näytä vastaus ruudulla
function nayta(teksti) {
    document.getElementById("tuloste").textContent = teksti;
}
