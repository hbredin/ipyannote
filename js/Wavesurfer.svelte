<script>
    import WaveSurfer from 'wavesurfer.js/dist/wavesurfer.esm.js'
    import RegionsPlugin from 'wavesurfer.js/dist/plugins/regions.esm.js'
    import TimelinePlugin from 'wavesurfer.js/dist/plugins/timeline.esm.js'
    import {onMount, setContext} from 'svelte'

    let { 
        b64_audio, 
        playing=$bindable(),
        zoom,
        onclick,
        children,
        addRegion,
    } = $props()
    let container
    let wavesurfer
    let ready = $state(false)

    const regions = RegionsPlugin.create()
    
    setContext('getWavesurfer', ()=>wavesurfer)
    setContext('regions', regions)

    function loadAudioBlob(b64) {
        // https://stackoverflow.com/questions/27980612/converting-base64-to-blob-in-javascript
        // https://ionic.io/blog/converting-a-base64-string-to-a-blob-in-javascript
        
        const byteString = atob(b64.split(',')[1]);
        const ab = new ArrayBuffer(byteString.length);
        const ia = new Uint8Array(ab);

        for (let i = 0; i < byteString.length; i++) {
        ia[i] = byteString.charCodeAt(i);
        }
        const blob = new Blob([ab], { type: 'audio/x-wav' });
        ready = false
        wavesurfer.loadBlob(blob);
    }

    export function playPause() {
        wavesurfer.playPause()
    }

    export function skip(time) {
        wavesurfer.skip(time)
    }

    onMount(()=>{
        wavesurfer = WaveSurfer.create({
            container: container,
            waveColor: '#4F4A85',
            progressColor: '#383351',
            barGap: 1,
            barHeight: 1,
            barRadius: 2,
            barWidth: 2,
            scrollParent: true,
            height: 300,
            plugins: [
                regions,
                TimelinePlugin.create({
                    insertPosition: 'beforebegin',
                }),
            ]
        })
        wavesurfer.on('play', ()=>{playing=true})
        wavesurfer.on('pause', ()=>{playing=false})
        wavesurfer.on('ready', ()=>ready=true)
        wavesurfer.on('dragstart', (X)=>{console.log('dragstart', X)})
        wavesurfer.on('click', onclick)

        regions.enableDragSelection({
            id: 'drag'
        })
        regions.on('region-created', addRegion)

        return () => {
            regions.destroy()
            wavesurfer.destroy()
        }
    })

    $effect(()=>loadAudioBlob($b64_audio))
    $effect(()=>{if (ready) {
        wavesurfer.zoom($zoom)
    }})

</script>

<div class="waveform" bind:this={container}>
    {#if ready}
        {@render children()}
    {/if}
</div>

<style>
    .waveform {
        height: 300px;
        width: 100%;
    }
</style>