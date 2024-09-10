import WaveSurfer from 'https://cdn.jsdelivr.net/npm/wavesurfer.js@7.8.4/dist/wavesurfer.esm.js'
import RegionsPlugin from 'https://cdn.jsdelivr.net/npm/wavesurfer.js@7.8.4/dist/plugins/regions.esm.js'

function loadAudioBlob(model, wavesurfer) {
    // https://stackoverflow.com/questions/27980612/converting-base64-to-blob-in-javascript
    // https://ionic.io/blog/converting-a-base64-string-to-a-blob-in-javascript
    
	const b64 = model.get('b64_audio')
	const byteString = atob(b64.split(',')[1]);
    const ab = new ArrayBuffer(byteString.length);
    const ia = new Uint8Array(ab);

    for (let i = 0; i < byteString.length; i++) {
      ia[i] = byteString.charCodeAt(i);
    }
    const blob = new Blob([ab], { type: 'audio/x-wav' });
	wavesurfer.loadBlob(blob);
}

function render({ model, el }) {

	// create a container for the wavesurfer instance that is focused when the mouse enters.
	// this allows the user to interact with the player using keyboard shortcuts.
	const container = document.createElement("div");
	container.tabIndex = 1;
	container.addEventListener("mouseenter", () => {
		container.focus();
	});

	const regions_plugin = RegionsPlugin.create();

    const wavesurfer = WaveSurfer.create({
		container: container,
		waveColor: '#4F4A85',
		progressColor: '#383351',
		barGap: 1,
		barHeight: 1,
		barRadius: 2,
		barWidth: 2,
		scrollParent: true,
		plugins: [regions_plugin],
    });

	// load audio blob once wavesurfer is ready
	wavesurfer.on("init", () => {
		loadAudioBlob(model, wavesurfer);
	});

	// load audio blob when it changes on Python side
	model.on("change:b64_audio", () => {
		loadAudioBlob(model, wavesurfer);
	});

	// update regions when they change on Python side
	model.on("change:regions", () => {
		const regions = model.get("regions");
		regions.forEach((region) => {
			regions_plugin.addRegion(region);
		});
	});

	wavesurfer.on("'region-update-end'", () => {
		model.set("regions", wavesurfer.regions.list);
		model.save_changes();
	});

	// play/pause on space key
	container.addEventListener("keydown", (event) => {  
		event.stopPropagation();
		if (event.code === "Tab") {
			event.preventDefault();
			if (wavesurfer.isPlaying()) {
				wavesurfer.pause();
			} else {
				wavesurfer.play();
			}
		}
	});

	el.appendChild(container);

	return () => {
		// callback that is executed any time the view is removed from the DOM. This feature is useful when dealing with complex event listeners, subscriptions, or third-party libraries that require proper teardown.
		
		// stop playing?
		// destroy wavesurfer?
	
	};

}

export default { render };
