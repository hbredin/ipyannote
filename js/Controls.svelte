<script>
    import { createValue } from './stores';
    let { model } = $props()

    let playing = createValue(model, 'playing', false)
    let zoom = createValue(model, 'zoom')

    function togglePlaying() {
        $playing = !$playing
    }
</script>

<div class="controls">
    <button onclick={togglePlaying} title="Press Space to play/pause">
        {#if $playing}
                Pause
        {:else}
                Play
        {/if}
    </button>
    <label>Zoom <input bind:value={$zoom} type='range' min='1' max='200'> </label>
</div>

<style>
    .controls {
        margin-top: 2em;
        display: flex;
        flex-direction: row;
        column-gap: 1em;
    }
    button {
        min-width: 10em;
        min-height: 2em;
        position: relative;
    }
    label {
        display: flex;
        align-items: center;
    }
</style>