const testWave = (url, index) => {
    // Create a unique container selector based on the passed index
    const waveformContainer = document.getElementById(`waveform-${index}`);
    const playBtn = document.getElementById(`playBtn-${index}`);

    // Check if WaveSurfer is already initialized in the container
    if (waveformContainer.wavesurferInstance) {
        const wavesurfer = waveformContainer.wavesurferInstance;
        // Toggle play/pause
        if (wavesurfer.isPlaying()) {
            wavesurfer.pause();
            playBtn.innerHTML = '<i class="fa-solid fa-play"></i>';
        } else {
            wavesurfer.play();
            playBtn.innerHTML = '<i class="fa-solid fa-pause"></i>';
        }
    } else {
        // Initialize WaveSurfer if not already done
        const wavesurfer = WaveSurfer.create({
            container: waveformContainer,
            waveColor: '#4F4A85',
            progressColor: '#383351',
            responsive: true,
            height: 60,
            url: url,
        });

        // Store the WaveSurfer instance on the container element
        waveformContainer.wavesurferInstance = wavesurfer;

        // Play the audio when the user interacts
        wavesurfer.on('interaction', () => {
            wavesurfer.play();
            playBtn.innerHTML = '<i class="fa-solid fa-pause"></i>';
        });

        // Reset play button when audio ends
        wavesurfer.on('finish', () => {
            playBtn.innerHTML = '<i class="fa-solid fa-play"></i>';
        });
    }
};
