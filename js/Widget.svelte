<script>
    import { createValue, createRegionsValue } from './stores';
    import Wavesurfer from './Wavesurfer.svelte';
    import Region from './Region.svelte'

    let { model } = $props()

    // create stores from traits
    let b64_audio = createValue(model, 'b64_audio')
    let zoom = createValue(model, 'zoom')
    let regions = createRegionsValue(model, 'regions')
    let selectedIndex = createValue(model, 'selected_index', -1)
    
    let playing = $state(false)

    let wrapper // Wrapper div
    let ws // Wavesurfer component

    function hotkeys(event) {
        if (event.code === 'Space') {
            event.preventDefault()
            ws.playPause()
        } else if (event.code === 'ArrowLeft') {
            ws.skip(event.altKey?-0.1:-1)
        } else if (event.code === 'ArrowRight') {
            ws.skip(event.altKey?0.1:1)
        } else if (event.code === 'Delete') {
            if ($selectedIndex !== -1) {
                $selectedIndex = regions.deleteRegion($selectedIndex)
            }
        } else if (event.code === 'Tab') {
            event.preventDefault()
            if ($selectedIndex === -1) return
            if (event.shiftKey) {
                // select previous region
                $selectedIndex = Math.max(0, $selectedIndex - 1)
            } else {
                // select next region
                $selectedIndex = Math.min($regions.length - 1, $selectedIndex + 1)
            }
        }
    }

    function addRegion(region) {
        // check if this region was created by dragging on the waveform
        // in that case its id will be "drag"
        // and we'll remove it and create a new region by updating the store
        if (region.id !== 'drag') {
            return
        }
        const createdRegion = {
            start: region.start,
            end: region.end,
            content: '?', // todo assign active label
        }
        // can't directly remove a newborn region for some reason
        setTimeout(()=>region.remove(), 10)
        $selectedIndex = regions.addRegion(createdRegion)
    }

    // make regions dodge each other when they overlap
    let overlap = $derived.by(()=>{
        const moments = [
            ...$regions.map((r,i)=>{return {time: r.start, start: true, index: i}}),
            ...$regions.map((r,i)=>{return {time: r.end, start: false, index: i}}),
        ]
        moments.sort((a,b)=>a.time - b.time)
        const tracks = [...$regions.map(r=>-1)]
        const activeTracks = new Set()
        for (let {start, index} of moments) {
            if (start) {
                let mytrack = -1
                for (let track=0; track<10; track++) {
                    if (!activeTracks.has(track)) {
                        mytrack=track
                        break
                    }
                }
                tracks[index] = mytrack
                activeTracks.add(mytrack)
            } else {
                activeTracks.delete(tracks[index])
            }
        }
        return tracks
    })


</script>

<!-- svelte-ignore a11y_no_static_element_interactions -->
<div class="wrapper" bind:this={wrapper} tabindex="-1" onkeydown={hotkeys}>
    <Wavesurfer 
        {b64_audio} 
        bind:this={ws} 
        bind:playing {zoom}
        onclick={()=>{wrapper.focus(); $selectedIndex=-1}}
        {addRegion}
    >
        {#each $regions as region, i (region)}
             <Region 
                start={region.start} 
                end={region.end} 
                content={region.content}
                isSelected={$selectedIndex===i}
                select={()=>{$selectedIndex=i}}
                focus={()=>wrapper.focus()}
                update={(region)=>$selectedIndex=regions.updateRegion(region, i)}
                overlap={overlap[i]}
                play={()=>ws.playRegion(region)}
                loop={()=>ws.loopRegion(region)}
                />
        {/each}
    </Wavesurfer>
</div>

<div class="controls">
    <button onclick={ws.playPause} title="Press Space to play/pause">
        {#if playing}
                Pause
        {:else}
                Play
        {/if}
    </button>
    <input bind:value={$zoom} type='range' min='1' max='200'>
    <button onclick={regions.clear}>Clear regions</button>
</div>


<style>
    .wrapper {
        margin: 1px;
    }
    .wrapper:focus {
        outline: 1px solid #4F4A85;
    }
    .controls {
        margin-top: 2em;
    }
</style>