<script>
    import { tick } from 'svelte';
    let {
        labels,
        selectedLabel=$bindable(),
        colors,
        relabelSelectedRegion,
        createLabel,
        focus,
    } = $props()

    let addingLabel = $state(false)
    let newLabel = $state('')
    let labelInput = $state()
    
    function handleClick(label) {
        selectedLabel = label
        relabelSelectedRegion(label)
    }

    export async function addLabel() {
        addingLabel = true
        await tick()
        labelInput.focus()
    }

    function handleKeydown(event) {
        event.stopPropagation() // prevent widget hotkeys when editing name
        if (event.code === 'Enter') {
            labelInput.blur()
        }
    }

    function finishAddingLabel() {
        addingLabel = false
        if ((newLabel !== '')&&(!labels.includes(newLabel))) {
            createLabel(newLabel)
        }
        newLabel = ''
        focus()
    }
</script>

<div class="labels">
    {#each labels as label, i}
        {@const key = (i<9) ? i+1:0}
         <button 
            class="label" 
            class:selected={label===selectedLabel}
            style="background-color:{colors[i%colors.length]};"
            onclick={()=>handleClick(label)}
            >
            <span class="label">{label}</span>
            {#if i < 10}
                <span class="key">{key}</span>
            {/if}
        </button>
    {/each}
    {#if addingLabel}
        <input type="text" 
            bind:this={labelInput}
            bind:value={newLabel}
            onkeydown={handleKeydown}
            onblur={finishAddingLabel}
            >
         
    {:else}
        <button
            class="add-label"
            onclick={addLabel}>
            Add label
            {#if labels.length < 10}
                <span class="key">{labels.length===9 ? 0:labels.length+1}</span>
            {/if}
        </button>
    {/if}
</div>

<style>
    button {
        min-width: 10em;
        min-height: 2em;
        position: relative;
    }
    button:hover {
        filter: brightness(90%);
    }
    button.selected {
        background-image: repeating-linear-gradient( 45deg, transparent, transparent 10px, #fff 10px, #ffffff 15px );
    }
    button.add-label {
        border-style: dotted;
        border-color: #ccc;
        background-color: transparent;
        color: #888;
    }
    span.key {
        font-size: 80%;
        font-family: monospace;
        padding: 2px 4px;
        border-radius: 3px;
        background-color: #f8f8f8;
        right: 2px;
        color: #888;
        border: 1px solid #888;
        position: absolute;
        top: 4px;
        right: 4px;
    }
</style>