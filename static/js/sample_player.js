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

const playerControls = {
	playBtn: document.getElementById('playBtn'),
	nxtBtn: document.getElementById('nxtBtn'),
	prvBtn: document.getElementById('prvBtn'),
};

let sound = null;
let currentUrl = ''
let wavesurfer = null
const playPause = (url) => {
	if (!wavesurfer) {
		const wavesurfer = WaveSurfer.create({
			container: '#waveform',
			waveColor: '#4F4A85',
			progressColor: '#383351',
			url: [url],
		});

		wavesurfer.on('click', () => {
			wavesurfer.play()
		});
	}

	if (url !== currentUrl) {
		if (sound) {
			sound.stop();
		}
		sound = new Howl({
			src: [url],
			autoplay: false,
			loop: false,
			html5: true,
			format: ['mp3', 'wav'],
		});
		currentUrl = url;
	}
	sound.playing() ? sound.pause() : sound.play();
};
