<script>
    import {onMount, getContext} from 'svelte'
    let {start=$bindable(), end=$bindable(), content=$bindable()} = $props()
    let thisRegion = null

    function update() {
        start = thisRegion.start
        end = thisRegion.end
    }

    onMount(()=>{
        const regions = getContext('regions')
        thisRegion = regions.addRegion({
            start,
            end,
            content,
        })
        thisRegion.element.style.top = '30%'
        thisRegion.element.style.height = '40%'

        thisRegion.on('update-end', update)

        return () => {
            thisRegion.unAll()
            thisRegion.remove()
        }
    })
</script>