let gameId = null;

async function aloitaPeli() {
  const nimi = document.getElementById("nimi").value.trim();
  const difficulty = document.getElementById("difficulty").value;

  if (nimi === "") {
    alert("Anna pelaajan nimi.");
    return;
  }

  try {
    const response = await fetch("http://127.0.0.1:5000/api/aloita", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        nimi: nimi,
        difficulty: difficulty
      })
    });

    const data = await response.json();

    gameId = data.game_id;

    document.getElementById("info").textContent =
      `Peli alkaa! CO2: ${data.co2} / ${data.budget}`;

    document.getElementById("hint").textContent =
      `Vihje: ${data.hint}`;

  } catch (error) {
    console.error(error);
    document.getElementById("info").textContent =
      "Virhe: Flask-palvelimeen ei saatu yhteyttä. Tarkista, että app.py on käynnissä.";
  }
}

async function lenna(isoCountry) {
  if (gameId === null) {
    alert("Aloita peli ensin.");
    return;
  }

  try {
    const response = await fetch("http://127.0.0.1:5000/api/lenna", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        game_id: gameId,
        iso_country: isoCountry
      })
    });

    const data = await response.json();

    if (data.status === "game_over") {
      document.getElementById("info").textContent =
        `${data.message} CO2: ${data.co2} / ${data.budget}`;

      document.getElementById("hint").textContent = "";
      return;
    }

    if (data.status === "win") {
      document.getElementById("info").textContent = data.message;
      document.getElementById("hint").textContent = "";
      return;
    }

    if (data.status === "error") {
      document.getElementById("info").textContent = data.message;
      return;
    }

    document.getElementById("info").textContent =
      `Lensit maahan ${data.country}. Matka: ${data.km} km. CO2: ${data.co2} / ${data.budget}`;

    if (data.found_item) {
      document.getElementById("hint").textContent =
        "Löysit esineen! Uusi vihje: " + data.hint;
    } else {
      document.getElementById("hint").textContent =
        "Väärä maa. Vihje: " + data.hint;
    }

  } catch (error) {
    console.error(error);
    document.getElementById("info").textContent =
      "Virhe lentäessä. Tarkista Flask-palvelin ja Pythonin virheilmoitus.";
  }
}