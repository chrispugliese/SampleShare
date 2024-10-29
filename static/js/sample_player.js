document.addEventListener('DOMContentLoaded', () => {
	const sampleElements = document.querySelectorAll('.sample-url');

	sampleElements.forEach((sampleEle, index) => {
		const sampleUrl = sampleEle.value;
		const containerId = `waveform-${index + 1}`;
		initWaveSurfer(sampleUrl, containerId);
	});
});

const initWaveSurfer = (url, containerId) => {
	//some of the options for waveforms, more here: https://wavesurfer.xyz/examples/?all-options.js
	const wavesurfer = WaveSurfer.create({
		container: `#${containerId}`,
		height: 150,
		width: 800,
		normalize: false,
		waveColor: '#4F4A85',
		progressColor: '#000000',
		cursorColor: '#000000',
		barWidth: 3,
		barGap: NaN,
		barRadius: 5,
		cursorWidth: 2,
		fillParent: true,
		mediaControls: false,
		dragToSeek: true,
		backend: 'MediaElement',

		//	renderFunction: (channels, ctx) => {
		//		const { width, height } = ctx.canvas
		//		const scale = channels[0].length / width
		//		const step = 10

		//		ctx.translate(0, height / 2)
		//		ctx.strokeStyle = ctx.fillStyle
		//		ctx.beginPath()

		//		for (let i = 0; i < width; i += step * 2) {
		//			const index = Math.floor(i * scale)
		//			const value = Math.abs(channels[0][index])
		//			let x = i
		//			let y = value * height

		//			ctx.moveTo(x, 0)
		//			ctx.lineTo(x, y)
		//			ctx.arc(x + step / 2, y, step / 2, Math.PI, 0, true)
		//			ctx.lineTo(x + step, 0)

		//			x = x + step
		//			y = -y
		//			ctx.moveTo(x, 0)
		//			ctx.lineTo(x, y)
		//			ctx.arc(x + step / 2, y, step / 2, Math.PI, 0, false)
		//			ctx.lineTo(x + step, 0)
		//		}

		//		ctx.stroke()
		//		ctx.closePath()
		//	},
	});
	wavesurfer.load(url);
	wavesurfer.on('interaction', () => {
		wavesurfer.isPlaying() ? wavesurfer.pause() : wavesurfer.play();
	});
};

