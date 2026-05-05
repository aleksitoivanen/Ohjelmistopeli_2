let positions = [0, 0, 0];
let finished = [];
let chosenHorse = null;

const tracksDiv = document.getElementById("tracks");
const resultText = document.getElementById("result");
const gameDiv = document.getElementById("game");
const startBtn = document.getElementById("startBtn");
const sound = document.getElementById("hirnahdus");

function render() {
    tracksDiv.innerHTML = positions.map(pos => {
        let percent = Math.min((pos / 30) * 100, 100);
        return `
        <div class="track">
            <div class="horse" style="left:${percent}%"></div>
        </div>`;
    }).join("");
}

function startGame() {
    if (!chosenHorse) return alert("Valitse hevonen!");

    fetch('/reset');

    positions = [0, 0, 0];
    finished = [];

    gameDiv.style.display = "block";
    resultText.innerText = "";

    render();
}

function chooseHorse(horse) {
    chosenHorse = horse;
    startBtn.disabled = false;
}

function moveHorses() {
    sound.currentTime = 0;
    sound.play();

    fetch('/move')
        .then(res => res.json())
        .then(data => {
            positions = data.positions;
            finished = data.finished;
            render();

            if (finished.length) {
                const winner = finished[0];
                resultText.innerText =
                    winner === chosenHorse
                        ? `Voitit! ${winner} tuli ensimmäisenä maaliin!`
                        : `Hävisit! Voittaja oli ${winner}.`;
            }
        });
}

document.addEventListener("DOMContentLoaded", render);
