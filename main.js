const playButton = document.getElementById("radio-play");
const pauseButton = document.getElementById("radio-pause");

function play() {
    playButton.hidden = true;
    pauseButton.hidden = false;
}

function pause() {
    playButton.hidden = false;
    pauseButton.hidden = true;
}