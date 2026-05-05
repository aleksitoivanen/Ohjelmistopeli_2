let positions = [0, 0, 0];
let finished = [];
let chosenHorse = null;

function render() {
    const tracksDiv = document.getElementById("tracks");
    tracksDiv.innerHTML = "";

    positions.forEach((pos, i) => {
        let percent = Math.min((pos / 30) * 100, 100);

        tracksDiv.innerHTML += `
        <div class="track">
            <div class="horse" style="left:${percent}%"></div>
        </div>`;
    });
}

function startGame() {
    if (!chosenHorse) {
        alert("Valitse hevonen!");
        return;
    }

    fetch('/reset');

    document.getElementById("game").style.display = "block";
    document.getElementById("result").innerText = "";
    positions = [0, 0, 0];
    finished = [];
    render();
}

function chooseHorse(horse) {
    chosenHorse = horse;
    document.getElementById("startBtn").disabled = false;
}

function moveHorses() {
    const sound = document.getElementById("hirnahdus");
    sound.currentTime = 0;
    sound.play();

    fetch('/move')
    .then(res => res.json())
    .then(data => {
        positions = data.positions;
        finished = data.finished;
        render();

        if (finished.length >= 1) {
            if (finished[0] === chosenHorse) {
                document.getElementById("result").innerText =
                    "Voitit! " + chosenHorse + " tuli ensimmäisenä maaliin!";
            } else {
                document.getElementById("result").innerText =
                    "Hävisit! Voittaja oli " + finished[0] + ".";
            }
        }
    });
}

document.addEventListener("DOMContentLoaded", render);
