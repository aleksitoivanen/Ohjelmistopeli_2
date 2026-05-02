const dealerCardsDiv = document.getElementById("dealer-cards");
const playerCardsDiv = document.getElementById("player-cards");
const dealerValueDiv = document.getElementById("dealer-value");
const playerValueDiv = document.getElementById("player-value");
const messageDiv = document.getElementById("message");

document.getElementById("btn-new").onclick = uusiPeli;
document.getElementById("btn-hit").onclick = otaKortti;
document.getElementById("btn-stand").onclick = jaa;

async function uusiPeli() {
    const res = await fetch("/api/uusi");
    render(await res.json());
}

async function otaKortti() {
    const res = await fetch("/api/hit", { method: "POST" });
    render(await res.json());
}

async function jaa() {
    const res = await fetch("/api/stand", { method: "POST" });
    render(await res.json());
}

function render(tila) {
    dealerCardsDiv.innerHTML = "";
    playerCardsDiv.innerHTML = "";

    // Jakajan kortit — näytä vain ensimmäinen jos peli kesken
    tila.jakaja.forEach((kortti, index) => {
        let teksti = kortti;

        if (tila.tila === "pelaa" && index > 0) {
            teksti = "🂠"; // piilotettu kortti
        }

        const el = card(teksti);
        dealerCardsDiv.appendChild(el);
        setTimeout(() => el.classList.add("show"), index * 100);
    });

    // Pelaajan kortit
    tila.pelaaja.forEach((kortti, index) => {
        const el = card(kortti);
        playerCardsDiv.appendChild(el);
        setTimeout(() => el.classList.add("show"), index * 100);
    });

    dealerValueDiv.textContent =
        tila.jakajaArvo !== null ? `Arvo: ${tila.jakajaArvo}` : "Arvo: ?";

    playerValueDiv.textContent = `Arvo: ${tila.pelaajaArvo}`;

    messageDiv.textContent = tila.viesti;

    const pelaa = tila.tila === "pelaa";
    document.getElementById("btn-hit").disabled = !pelaa;
    document.getElementById("btn-stand").disabled = !pelaa;
}

function card(teksti) {
    const div = document.createElement("div");
    div.className = "card";
    div.textContent = teksti;
    return div;
}

uusiPeli();
