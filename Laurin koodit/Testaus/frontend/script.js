let gameId = null;
let odottavaMaa = null;

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
      `Peli alkoi! CO2: ${data.co2} / ${data.budget}`;

    document.getElementById("hint").textContent =
      `Vihje: ${data.hint}`;

  } catch (error) {
    console.error(error);
    document.getElementById("info").textContent =
      "Virhe: Flask-palvelimeen ei saatu yhteyttä.";
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

    if (data.status === "blackjack_required") {
      odottavaMaa = isoCountry;
      document.getElementById("info").textContent = data.message;
      await avaaBlackjack();
      return;
    }

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
      "Virhe lentäessä. Tarkista Flask-palvelin.";
  }
}

async function avaaBlackjack() {
  const response = await fetch("http://127.0.0.1:5000/api/blackjack/aloita", {
    method: "POST"
  });

  const data = await response.json();
  document.getElementById("blackjack-container").style.display = "block";
  renderBlackjack(data);
}

async function bjUusi() {
  const response = await fetch("http://127.0.0.1:5000/api/blackjack/uusi", {
    method: "POST"
  });

  const data = await response.json();
  renderBlackjack(data);
}

async function bjHit() {
  const response = await fetch("http://127.0.0.1:5000/api/blackjack/hit", {
    method: "POST"
  });

  const data = await response.json();
  renderBlackjack(data);
}

async function bjStand() {
  const response = await fetch("http://127.0.0.1:5000/api/blackjack/stand", {
    method: "POST"
  });

  const data = await response.json();
  renderBlackjack(data);

  if (data.valmis) {
    document.getElementById("blackjack-container").style.display = "none";
    document.getElementById("info").textContent =
      "Blackjack-haaste läpäisty. Lennetään Ruotsiin...";

    if (odottavaMaa) {
      const maa = odottavaMaa;
      odottavaMaa = null;
      await lenna(maa);
    }
  }
}

function renderBlackjack(data) {
  const dealerDiv = document.getElementById("bj-dealer");
  const playerDiv = document.getElementById("bj-player");
  const infoDiv = document.getElementById("bj-info");
  const progressDiv = document.getElementById("bj-progress");

  dealerDiv.innerHTML = "<h3>Jakaja</h3>";
  playerDiv.innerHTML = "<h3>Pelaaja</h3>";

  data.jakaja.forEach((kortti, i) => {
    let teksti = kortti;

    if (data.tila === "pelaa" && i > 0) {
      teksti = "🂠";
    }

    const span = document.createElement("span");
    span.className = "bj-kortti";
    span.textContent = teksti;
    dealerDiv.appendChild(span);
  });

  const dealerArvo = document.createElement("p");
  dealerArvo.textContent =
    data.jakajaArvo !== null ? `Arvo: ${data.jakajaArvo}` : "Arvo: ?";
  dealerDiv.appendChild(dealerArvo);

  data.pelaaja.forEach((kortti) => {
    const span = document.createElement("span");
    span.className = "bj-kortti";
    span.textContent = kortti;
    playerDiv.appendChild(span);
  });

  const playerArvo = document.createElement("p");
  playerArvo.textContent = `Arvo: ${data.pelaajaArvo}`;
  playerDiv.appendChild(playerArvo);

  progressDiv.textContent = `Voitot: ${data.voitot} / 5`;
  infoDiv.textContent = data.viesti;

  const peliKesken = data.tila === "pelaa";
  document.getElementById("bj-hit").disabled = !peliKesken;
  document.getElementById("bj-stand").disabled = !peliKesken;
  document.getElementById("bj-uusi").disabled = peliKesken;

  if (!peliKesken && !data.valmis) {
    infoDiv.textContent += " Aloita uusi kierros painamalla 'Uusi kierros'.";
  }
}