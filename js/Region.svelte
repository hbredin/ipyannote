<script>
    import {onMount, getContext} from 'svelte'
    let {
        start, 
        end, 
        content, 
        color,
        isSelected=true,
        select,
        focus,
        update,
        overlap,
        play,
        loop
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
            if (event.shiftKey) {
                loop()
            } else {
                play()
            }
        } else {
            select()
        }
        focus()
    }

    $effect(()=>{if (region) {
        const parts = new Set(element.getAttribute('part').split(' '))
        if (isSelected) {
            parts.add('region-selected')
        } else {
            parts.delete('region-selected')
        }
        element.setAttribute('part', [...parts].join(' '))
    }})

    $effect(()=>{if (region) {
        const dodge = Math.ceil(overlap/2)*(overlap%2===0?-1:1)
        element.style.top = `${30+5*dodge}%`
    }})

    $effect(()=>{if (region) {
        element.style.backgroundColor = color
    }})

    $effect(()=>{if (region) {
        region.setContent(content)
    }})

    onMount(()=>{
        region = regions.addRegion({
            start,
            end,
            content,
        })
        element = region.element
        element.style.height = '40%'
        element.style.opacity = '75%'

        region.on('update-end', handleUpdate)
        region.on('click', handleClick)

        return () => {
            region.remove()
        }
    })
</script>

<style>
:global(::part(region-selected)) {
    background-image: repeating-linear-gradient( 45deg, transparent, transparent 10px, #fff 10px, #ffffff 15px );
    z-index: 1000;
}
</style>