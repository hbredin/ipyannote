<script>
    import WaveSurfer from 'wavesurfer.js/dist/wavesurfer.esm.js'
    import RegionsPlugin from 'wavesurfer.js/dist/plugins/regions.esm.js'
    import TimelinePlugin from 'wavesurfer.js/dist/plugins/timeline.esm.js'
    import {onMount, setContext} from 'svelte'

    let { 
        b64_audio, 
        playing,
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

    export function play() {
        wavesurfer.play()
    }

    export function pause() {
        wavesurfer.pause()
    }

    export function skip(time) {
        wavesurfer.skip(time)
    }

    let playedRegion, loopedRegion
    export function playRegion(region) {
        wavesurfer.setTime(region.start)
        playedRegion = region
        $playing = true
    }

    export function loopRegion(region) {
        wavesurfer.setTime(region.start)
        loopedRegion = region
        $playing = true
    }

    function handleTime(t) {
        if (playedRegion) {
            if ((t < playedRegion.start)||(t>playedRegion.end)) {
                if ($playing) {
                    $playing=false
                }
                playedRegion = undefined
            }
        } else if (loopedRegion) {
            if ((t < loopedRegion.start)||(t>loopedRegion.end+0.3)) {
                if ($playing) {
                    $playing = false
                }
                loopedRegion = undefined
            } else if ((t > loopedRegion.end)&&$playing) {
                wavesurfer.setTime(loopedRegion.start)
            }
        }
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
        wavesurfer.on('ready', ()=>ready=true)
        wavesurfer.on('click', onclick)
        wavesurfer.on('timeupdate', handleTime)

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