const playButton = document.getElementById('radio-play');
const pauseButton = document.getElementById('radio-pause');
const currentTrackLabel = document.getElementById('current-track');
const radioPlayer = document.getElementById('radio-player');
const videoPlayer = document.getElementById('video-player');

let currentSchedule;

window.addEventListener('DOMContentLoaded', loadSchedule);
playButton.addEventListener('click', playRadio);
pauseButton.addEventListener('click', pauseRadio);
videoPlayer.addEventListener('play', pauseRadio);

function loadSchedule() {
    fetch('/api/radio_schedule')
    .then(response => response.json())
    .then(data => {
        const schedule = data['schedule'];
        currentSchedule = schedule.map(item => {
            const [time, ...rest] = item.split(' ');
            return { timestamp: parseInt(time), track: rest.join(' ') };
        });
        const timerId = setInterval(() => {
            const currentTrack = getCurrentTrack();
            if (!currentTrack) {
                clearInterval(timerId);
                currentTrackLabel.innerHTML = '';
                loadSchedule();
                return;
            }
            if (currentTrackLabel.innerHTML !== currentTrack) {
                currentTrackLabel.innerHTML = currentTrack;
            }
        }, 1000);
    })
    .catch(error => console.error('Error fetching schedule:', error));
}

function getCurrentTrack() {
    let currentTrack;
    const timeNow = Math.floor(Date.now() / 1000);
    for (let i = 0; i < currentSchedule.length; i++) {
        const { timestamp, track } = currentSchedule[i];
        if (timeNow < timestamp) {
            currentTrack = track;
            break;
        }
    }
    return currentTrack;
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