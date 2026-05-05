let gameId = null;
let odottavaMaa = null;
let odottavaItalia = null;

let matikkaAjastin = null;
let matikkaAikaaJaljella = 10;

async function aloitaPeli() {
  const nimi = document.getElementById("nimi").value.trim();
  const difficulty = document.getElementById("difficulty").value;

  if (nimi === "") {
    alert("Anna pelaajan nimi.");
    return;
  }

  await lahetaAloituspyynto(nimi, difficulty);
}

async function lahetaAloituspyynto(nimi, difficulty, jatka = null) {
  try {
    const body = {
      nimi: nimi,
      difficulty: difficulty
    };

    if (jatka !== null) {
      body.jatka = jatka;
    }

    const response = await fetch("http://127.0.0.1:5000/api/aloita", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify(body)
    });

    const data = await response.json();

    if (data.status === "vanha_peli") {
      const jatketaanko = confirm(
        `Pelaajalle löytyi vanha peli.

` +
        `CO2: ${data.co2} / ${data.budget}
` +
        `Löydettyjä esineitä: ${data.current_item}
` +
        `Vaikeustaso: ${data.difficulty}

` +
        `Paina OK, jos haluat jatkaa vanhaa peliä.
` +
        `Paina Peruuta, jos haluat aloittaa alusta.`
      );

      await lahetaAloituspyynto(nimi, difficulty, jatketaanko);
      return;
    }

    gameId = data.game_id;

    if (data.status === "win") {
      document.getElementById("info").textContent = data.message;
      document.getElementById("hint").textContent = "";
      return;
    }

    const alkuTeksti = data.status === "jatkettu" ? "Peli jatkuu" : "Peli alkoi";

    document.getElementById("info").textContent =
      `${alkuTeksti}! CO2: ${data.co2} / ${data.budget}`;

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

    if (data.status === "math_required") {
      odottavaItalia = isoCountry;
      document.getElementById("info").textContent = data.message;
      await avaaMatikka();
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

    if (data.item_status === "loydetty") {
      document.getElementById("hint").textContent =
        "Löysit esineen! Uusi vihje: " + data.hint;
    } else if (data.item_status === "jo_saatu") {
      document.getElementById("hint").textContent =
        "Olet saanut esineen täältä jo aiemmin.";
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

/* -------------------------
   BLACKJACK
------------------------- */

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

/* -------------------------
   MATIKKA2
------------------------- */

async function avaaMatikka() {
  const response = await fetch("http://127.0.0.1:5000/api/matikka/aloita", {
    method: "POST"
  });

  const data = await response.json();
  document.getElementById("matikka-container").style.display = "block";
  renderMatikka(data);
  kaynnistaMatikkaAjastin();
}

function kaynnistaMatikkaAjastin() {
  clearInterval(matikkaAjastin);
  matikkaAikaaJaljella = 10;
  document.getElementById("matikka-ajastin").textContent = `Aikaa: ${matikkaAikaaJaljella}`;

  matikkaAjastin = setInterval(async () => {
    matikkaAikaaJaljella--;
    document.getElementById("matikka-ajastin").textContent = `Aikaa: ${matikkaAikaaJaljella}`;

    if (matikkaAikaaJaljella <= 0) {
      clearInterval(matikkaAjastin);
      await lahetaMatikkaVastaus(null);
    }
  }, 1000);
}

async function matikkaVastaa() {
  const kentta = document.getElementById("matikka-vastaus");
  const vastaus = kentta.value.trim();

  if (vastaus === "") {
    return;
  }

  await lahetaMatikkaVastaus(vastaus);
}

async function lahetaMatikkaVastaus(vastaus) {
  clearInterval(matikkaAjastin);

  const response = await fetch("http://127.0.0.1:5000/api/matikka/vastaa", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({
      vastaus: vastaus
    })
  });

  const data = await response.json();
  renderMatikka(data);

  if (data.valmis) {
    document.getElementById("matikka-container").style.display = "none";
    document.getElementById("info").textContent =
      "Matikkahaaste läpäisty. Lennetään Italiaan...";

    if (odottavaItalia) {
      const maa = odottavaItalia;
      odottavaItalia = null;
      await lenna(maa);
    }
    return;
  }

  kaynnistaMatikkaAjastin();
}

function renderMatikka(data) {
  document.getElementById("matikka-progress").textContent = `Oikein: ${data.oikein} / 5`;
  document.getElementById("matikka-kysymys").textContent = data.kysymys || "";
  document.getElementById("matikka-info").textContent = data.viesti || "";
  document.getElementById("matikka-vastaus").value = "";
  document.getElementById("matikka-vastaus").focus();
}