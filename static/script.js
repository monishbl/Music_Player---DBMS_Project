// Global variables
let isPlaying = false;
let currentTrackIndex = -1;
let playlistData = [];
let isShuffleOn = false;
let isRepeatOn = false;

// Function to toggle play/pause
function togglePlayPause() {
    const audioPlayer = document.getElementById('audio-player');
    if (isPlaying) {
        audioPlayer.pause();
    } else {
        audioPlayer.play();
    }
    isPlaying = !isPlaying;
    updatePlayPauseButton();
}
document.addEventListener('DOMContentLoaded', function () {
    const audioPlayer = document.getElementById('audio-player');
    const progress = document.getElementById('progress');

    // Update progress bar when the time of the audio player updates
    // Update progress bar when the time of the audio player updates
audioPlayer.addEventListener('timeupdate', function() {
    const currentTime = audioPlayer.currentTime;
    const duration = audioPlayer.duration;
    const progressPercentage = (currentTime / duration) * 100;
    progress.style.width = progressPercentage + '%';

    // Update current time and total duration
    const currentTimeElement = document.getElementById('curtime');
    const totalTimeElement = document.getElementById('tottime');
    currentTimeElement.textContent = formatTime(currentTime);
    totalTimeElement.textContent = formatTime(duration);
});


// Function to format time in minutes and seconds
function formatTime(time) {
    const minutes = Math.floor(time / 60);
    const seconds = Math.floor(time % 60);
    return `${minutes}:${seconds < 10 ? '0' : ''}${seconds}`;
}

});

// Function to update play/pause button text
function updatePlayPauseButton() {
    const playPauseBtn = document.getElementById('play-pause-btn');
    playPauseBtn.textContent = isPlaying ? '⏸' : '▶️';
}

// Function to play a track
function playTrack(index) {
    const audioPlayer = document.getElementById('audio-player');
    const selectedSong = playlistData[index];
    audioPlayer.src = `${selectedSong.src}`;
    console.log(selectedSong.src)
    audioPlayer.load();
    const delayBeforeNextTrack = 500; // in milliseconds (adjust as needed)
    console.log("playing " + selectedSong.name)
    setTimeout(() => {
        audioPlayer.play();
        isPlaying = true;
        updatePlayPauseButton()
    }, delayBeforeNextTrack);
    updatesongname(index);
}

function playTrackfromplaylist(src, index) {
    const audioPlayer = document.getElementById('audio-player');
    
    audioPlayer.src = src;
    console.log(audioPlayer.src)
    audioPlayer.load();
    const delayBeforeNextTrack = 500; // in milliseconds (adjust as needed)
    setTimeout(() => {
        audioPlayer.play();
        isPlaying = true;
        updatePlayPauseButton()
    }, delayBeforeNextTrack);
    updatesongname(index)
}

// Function to play the previous track
function playPrevious() {
    if (isRepeatOn) {
        playTrack(currentTrackIndex);
    } else {
    currentTrackIndex = (currentTrackIndex - 1 + playlistData.length) % playlistData.length;
    playTrack(currentTrackIndex);
    }
}

// Function to play the next track
function playNext() {
    if (isRepeatOn) {
        // Just replay the current track
        playTrack(currentTrackIndex);
    } else {
        if (isShuffleOn) {
            currentTrackIndex = Math.floor(Math.random() * playlistData.length);
        } else {
            currentTrackIndex = (currentTrackIndex + 1) % playlistData.length;
        }
        playTrack(currentTrackIndex);
    }
}

// Function to shuffle an array
function shuffleArray(array) {
    for (let i = array.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [array[i], array[j]] = [array[j], array[i]];
    }
}


// // Function to shuffle playlist and update next song name
// function toggleShuffle() {
//     // Shuffle the playlist
//     shuffleArray(playlistData);
//     const queue = document.getElementById('queue');
//     queue.innerHTML = ''; // Clear existing queue items
    
//     playlistData.forEach((song, index) => {
//         const listItem = document.createElement('li');
//         listItem.textContent = song.name;
//         listItem.setAttribute('data-src', song.src);
//         listItem.addEventListener('click', () => {
//             currentTrackIndex = index;
//             playTrack(currentTrackIndex);
//         });
//         queue.appendChild(listItem);
//     });

//     // Update current track index to point to the first song in the shuffled playlist
//     currentTrackIndex = -1;

//     // Update next song name
//     const nextSongElement = document.getElementById('next-song');
//     nextSongElement.textContent = `Next: ${playlistData.length > 0 ? playlistData[0].name : ''}`;
// }



// Function to toggle repeat mode
function toggleRepeat() {
    isRepeatOn = !isRepeatOn;
    const repeatBtn = document.getElementById('repeat-btn');
    repeatBtn.textContent = isRepeatOn ? 'Repeat: on' : 'Repeat: off';
}

// Function to update song name and duration
function updatesongname(index) {
    const currentSongElement = document.getElementById('current-song');
    const nextSongElement = document.getElementById('next-song');
    currentSongElement.textContent = `Now Playing: ${playlistData[index].name}`;
    nextSongElement.textContent = `Next: ${index + 1 < playlistData.length ? playlistData[index + 1].name : ''}`;
}

function updateplaylistsongname(index) {
    const currentSongElement = document.getElementById('current-song');
    const nextSongElement = document.getElementById('next-song');
    currentSongElement.textContent = `Now Playing: ${playlistData[index].name}`;
    nextSongElement.textContent = `Next: ${index + 1 < playlistData.length ? playlistData[index + 1].name : ''}`;
}

// Function to seek to a specific time in the audio
function seekAudio(event) {
    const audioPlayer = document.getElementById('audio-player');
    const progress = document.getElementById('progress');
    const timelineWidth = event.target.clientWidth;
    const clickX = event.offsetX;
    const duration = audioPlayer.duration;
    const seekTime = (clickX / timelineWidth) * duration;
    audioPlayer.currentTime = seekTime;
}
