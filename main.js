const playButton = document.getElementById("radio-play");
const pauseButton = document.getElementById("radio-pause");

const signalSlider = document.getElementById('signalSlider');
const signalBars = document.querySelectorAll('.signal-bar');

function updateSignalBars(level) {
    signalBars.forEach((bar, index) => {
        if (index < level) {
            bar.classList.add('active');
        } else {
            bar.classList.remove('active');
        }
    });
}

signalSlider.addEventListener('input', function() {
    updateSignalBars(signalSlider.value);
});

// Initialize with default value
updateSignalBars(signalSlider.value);   

function play() {
    playButton.hidden = true;
    pauseButton.hidden = false;
}

function pause() {
    playButton.hidden = false;
    pauseButton.hidden = true;
}