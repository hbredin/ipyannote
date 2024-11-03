import "./widget.css";
import Labels from "./Labels.svelte";
import { mount, unmount } from 'svelte';

function render({ model, el }) {
  const widget = mount(Labels, { target: el, props: {model} });
  return () => unmount(widget);;
}

export default { render };

