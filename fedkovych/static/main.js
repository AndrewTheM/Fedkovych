const playButton = document.getElementById('radio-play');
const pauseButton = document.getElementById('radio-pause');
const currentTrack = document.getElementById('current-track');
const radioPlayer = document.getElementById('radio-player');
const videoPlayer = document.getElementById('video-player');
const signalSlider = document.getElementById('signal-slider');
const signalBars = document.querySelectorAll('.signal-bar');

const delay = 15;

window.addEventListener('load', updateCurrentTrack);
signalSlider.addEventListener('input', updateVolume);
playButton.addEventListener('click', playRadio);
pauseButton.addEventListener('click', pauseRadio);
videoPlayer.addEventListener('play', pauseRadio);

// Initialize volume slider from local storage
signalSlider.value = parseInt(localStorage.getItem('volume'));
updateSignalBars(signalSlider.value);

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
            const timeNow = Math.floor(Date.now() / 1000);

            if (timeNow - parseInt(time) < delay) {
                currentTrack.innerHTML = trackTitle;
            } else {
                schedule.shift();
            }
        }, 1000);
    })
    .catch(error => console.error('Error fetching data:', error));
}

function updateVolume() {
    radioPlayer.volume = signalSlider.value / 5;
    localStorage.setItem('volume', signalSlider.value.toString());
    updateSignalBars(signalSlider.value);
}

function updateSignalBars(level) {
    signalBars.forEach((bar, index) => {
        if (index < level) {
            bar.classList.add('active');
        } else {
            bar.classList.remove('active');
        }
    });
}

function playRadio() {
    radioPlayer.play();
    videoPlayer.pause();
    playButton.hidden = true;
    pauseButton.hidden = false;
}

function pauseRadio() {
    radioPlayer.pause();
    playButton.hidden = false;
    pauseButton.hidden = true;
}