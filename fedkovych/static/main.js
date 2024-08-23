const playButton = document.getElementById('radio-play');
const pauseButton = document.getElementById('radio-pause');
const currentTrack = document.getElementById('current-track');
const audioPlayer = document.getElementById('radio-player');
const signalSlider = document.getElementById('signal-slider');
const signalBars = document.querySelectorAll('.signal-bar');

const delay = 15;

function updateCurrentTrack() {
    fetch('/api/radio_schedule')
    .then(response => response.json())
    .then(data => {
        schedule = data['schedule'];
        const timerId = setInterval(() => {
            if (schedule.length === 0) {
                clearInterval(timerId);
                currentTrack.innerHTML = '';
                updateCurrentTrack();
                return;
            }

            const [time, ...rest] = schedule[0].split(' ');
            const trackTitle = rest.join(' ');
            const time_now = Math.floor(Date.now() / 1000);

            if (time_now - parseInt(time) < delay) {
                currentTrack.innerHTML = trackTitle;
            } else {
                schedule.shift();
            }
        }, 1000);
    })
    .catch(error => console.error('Error fetching data:', error));
}

window.onload = updateCurrentTrack;

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