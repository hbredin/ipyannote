<script>
    let {
        labels,
        selectedLabel=$bindable()
    } = $props()
</script>

<div class="labels">
    {#each labels as label, i}
        {@const key = (i<9) ? i+1:0}
         <button 
            class="label" 
            class:selected={label===selectedLabel}
            onclick={()=>selectedLabel=label}
            >
            <span class="label" contenteditable bind:innerHTML={labels[i]}></span>
            {#if i < 10}
                <span class="key">{key}</span>
            {/if}
        </button>
    {/each}
</div>

<style>
    button {
        min-width: 10em;
        min-height: 2em;
    }
    button.selected {
        background-image: repeating-linear-gradient( 45deg, transparent, transparent 10px, #fff 10px, #ffffff 15px );
    }
    span.key {
        font-size: 80%;
        font-family: monospace;
        padding: 2px 5px;
        background-color: white;
        right: 2px;
        color: #888;
        border: 1px solid #888;
    }
</style>