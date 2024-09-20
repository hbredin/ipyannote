<script>
    import {onMount} from 'svelte'
    import { createValue } from './stores';
    import Wavesurfer from './Wavesurfer.svelte';
    import Region from './Region.svelte'

    let { model } = $props()

    // create stores from traits
    let b64_audio = createValue(model, 'b64_audio')
    let zoom = createValue(model, 'zoom')
    let regions = createValue(model, 'regions')
    let selectedIndex = createValue(model, 'selected_index', -1)
    let playing = $state(false)

    let wrapper // Wrapper div
    let ws // Wafesurfer component

    function hotkeys(event) {
        if (event.code === 'Space') {
            event.preventDefault()
            ws.playPause()
        } else if (event.code === 'ArrowLeft') {
            ws.skip(event.altKey?-0.1:-1)
        } else if (event.code === 'ArrowRight') {
            ws.skip(event.altKey?0.1:1)
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
        regions.update(r=>[...r, createdRegion])
    }


</script>

<!-- svelte-ignore a11y_no_static_element_interactions -->
<div class="wrapper" bind:this={wrapper} tabindex="-1" onkeydown={hotkeys}>
    <Wavesurfer 
        {b64_audio} 
        bind:this={ws} 
        bind:playing {zoom}
        onclick={()=>wrapper.focus()}
        {addRegion}
    >
        {#each $regions as region, i}
             <Region 
                bind:start={region.start} 
                bind:end={region.end} 
                bind:content={region.content}
                isSelected={$selectedIndex===i}
                select={()=>{$selectedIndex=i}}
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