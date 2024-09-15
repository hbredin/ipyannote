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
    let playing = $state(false)

    let wrapper // Wrapper div
    let ws // Wafesurfer component

    function hotkeys(event) {
        if (event.code === 'Space') {
            event.preventDefault()
            ws.playPause()
        }
    }

    function updateRegion(region) {
        const index = $regions.findIndex(x => x.id===region.id)
        const newRegion = Object.assign(
            {}, 
            $regions[index], 
            {
                start: region.start, 
                end: region.end
            })
        $regions[index] = newRegion
    }

</script>

<!-- svelte-ignore a11y_no_static_element_interactions -->
<div class="wrapper" bind:this={wrapper} tabindex="-1" onkeydown={hotkeys}>
    <Wavesurfer 
        {b64_audio} 
        bind:this={ws} 
        bind:playing {zoom}
        {updateRegion}
    >
        {#each $regions as region, i (region.id)}
             <Region {...region}/>
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