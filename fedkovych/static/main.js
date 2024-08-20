const playButton = document.getElementById("radio-play");
const pauseButton = document.getElementById("radio-pause");

const signalSlider = document.getElementById('signal-slider');
const signalBars = document.querySelectorAll('.signal-bar');
const audioPlayer = document.getElementById('radio-player');

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
    const volumeLevel = signalSlider.value / 5;
    audioPlayer.volume = volumeLevel;
    updateSignalBars(signalSlider.value);
});

// Initialize with default value
updateSignalBars(signalSlider.value);   

function play() {
    console.log("Play button clicked");  // Debugging line
    audioPlayer.play().then(() => {
        playButton.hidden = true;
        pauseButton.hidden = false;
    }).catch(error => {
        console.error("Error playing audio: ", error);
    });
}

function pause() {
    console.log("Pause button clicked");  // Debugging line
    audioPlayer.pause();
    playButton.hidden = false;
    pauseButton.hidden = true;
}