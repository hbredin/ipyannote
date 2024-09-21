import { writable } from "svelte/store";

export function createValue(model, name_, value_) {
  const name = name_;
  // use value from python if it is set when creating widget
  const modelValue = model.get(name);
  const curVal = writable(modelValue === undefined ? value_ : modelValue);
  model.on("change:" + name, () => curVal.set(model.get(name)), null);

  return {
    set: (v) => {
      curVal.set(v);
      if (Array.isArray(v)) {
        model.set(name, [], {silent: true})
      }
      model.set(name, v);
      model.save_changes();
    },
    subscribe: curVal.subscribe,
    update: (func) => {
      curVal.update((v) => {
        let out = func(v);
        if (Array.isArray(out)) {
          model.set(name, [], {silent: true})
        }
        model.set(name, out);
        model.save_changes();
        return out;
      });
    },
  };
}

// A custom store for regions trait
// Keeps regions sorted by start time
// 
export function createRegionsValue(model, name) {
  // use value from python if it is set when creating widget
  let modelValue = model.get(name);
  if (modelValue === undefined) {
    modelValue = []
  }
  function compareRegions(a, b) {
    return a.start - b.start
  }
  modelValue.sort(compareRegions)

  const curVal = writable(modelValue);

  model.on("change:" + name, () => {
    const regions = model.get(name)
    regions.sort(compareRegions)
    curVal.set(regions)
  }, null);

  // binary search to find an insertion index that keeps regions sorted
  function sortedIndex(regions, region) {
    let low = 0,
        high = regions.length;
    while (low < high) {
        let mid = (low + high) >>> 1;
        if (regions[mid].start < region.start) low = mid + 1;
        else high = mid;
    }
    return low;
  }

  return {
    subscribe: curVal.subscribe,
    updateRegion: (region, index) => {
      let newIndex = 0
      curVal.update((regions) => {
        regions.splice(index, 1)
        newIndex = sortedIndex(regions, region)
        regions.splice(newIndex, 0, region)
        model.set(name, [])
        model.set(name, regions)
        model.save_changes()
        return regions
      })
      return newIndex
    },
    addRegion: (region) => {
      let newIndex = 0
      curVal.update((regions) => {
        newIndex = sortedIndex(regions, region)
        regions.splice(newIndex, 0, region)
        model.set(name, [...regions])
        model.save_changes()
        return regions
      })
      return newIndex
    },
    deleteRegion: (index) => {
      let newIndex = 0
      curVal.update((regions) => {
        regions.splice(index, 1)
        model.set(name, [...regions])
        model.save_changes()
        newIndex = Math.min(index, regions.length-1)
        return regions
      })
      return newIndex
    },
  };
}
