// function playSample(url) {
// 	var sound = new Howl({
// 		src: [url],
// 		autoplay: false,
// 		loop: false,
// 		html5: true,
// 		format: ['mp3', 'wav'],
// 	});
// 	sound.play();
// }

// const playerControls = {
// 	playBtn: document.getElementById('playBtn'),
// 	nxtBtn: document.getElementById('nxtBtn'),
// 	prvBtn: document.getElementById('prvBtn'),
// };
// 
// let currentUrl = ''
// let wavesurfer = null
// 
// const initWaveSurfer = (url) => {
// 	wavesurfer = WaveSurfer.create({
// 		container: '#waveform',
// 		waveColor: '#4F4A85',
// 		progressColor: '#383351',
// 		backend: 'MediaElement',
// 	});
// 	wavesurfer.load(url);
// };
// 
// const playPause = (url) => {
// 	if (!wavesurfer) {
// 		initWaveSurfer(url)
// 	}
// 
// 	if (url !== currentUrl) {
// 		wavesurfer.load(url);
// 		currentUrl = url
// 	}
// 
// 	wavesurfer.isPlaying() ? wavesurfer.pause() : wavesurfer.play();
// };
// 
// playerControls.playBtn.addEventListener('click', () => playPause(currentUrl));
//

document.addEventListener('DOMContentLoaded', () => {
	// Get the first sample URL from the hidden input
	const sampleUrl = document.querySelector('.sample-url')?.value;

	if (sampleUrl) {
		initWaveSurfer(sampleUrl);
		// Automatically play the audio when loaded
	}
});

let wavesurfer = null;
let currentUrl = '';

const initWaveSurfer = (url) => {
	wavesurfer = WaveSurfer.create({
		container: '{waveform-#}',  // Assuming we want the first waveform to play automatically
		waveColor: '#4F4A85',
		progressColor: '#383351',
		backend: 'MediaElement',
	});
	wavesurfer.load(url);
	wavesurfer.on('interaction', () => {
		wavesurfer.isPlaying() ? wavesurfer.pause() : wavesurfer.play();
	});
};

