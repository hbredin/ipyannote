<script>
    import {onMount, getContext} from 'svelte'
    let {
        start, 
        end, 
        content, 
        isSelected=true,
        select,
        focus,
        update
    } = $props()

    let region = $state()
    let element = $state()

    const regions = getContext('regions')

    function handleUpdate() {
        update({start: region.start, end: region.end, content})
    }

    function handleClick(event) {
        event.stopPropagation()
        if (isSelected) {
            // play on click?
        } else {
            select()
        }
        focus()
    }

    $effect(()=>{if (region) {
        const el = region.element
        const parts = new Set(el.getAttribute('part').split(' '))
        if (isSelected) {
            parts.add('region-selected')
        } else {
            parts.delete('region-selected')
        }
        el.setAttribute('part', [...parts].join(' '))
    }})

    onMount(()=>{
        region = regions.addRegion({
            start,
            end,
            content,
        })
        element = region.element
        element.style.top = '30%'
        element.style.height = '40%'
        element.style.backgroundColor = 'rgb(255,215,0)'
        element.style.opacity = '75%'

        region.on('update-end', handleUpdate)
        region.on('click', handleClick)

        return () => {
            region.unAll()
            region.remove()
        }
    })
</script>

<style>
:global(::part(region-selected)) {
    background-image: repeating-linear-gradient( 45deg, transparent, transparent 10px, #fff 10px, #ffffff 15px );
}
</style>