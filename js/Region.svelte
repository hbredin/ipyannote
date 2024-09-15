<script>
    import {onMount, getContext} from 'svelte'
    let {start, end, id} = $props()

    onMount(()=>{
        const regions = getContext('regions')
        const region = regions.addRegion({
            start,
            end,
            id,
            // label? TODO
        })

        return () => {
            region.remove()
        }
    })
</script>