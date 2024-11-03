import "./widget.css";
import Controls from "./Controls.svelte";
import { mount, unmount } from 'svelte';

function render({ model, el }) {
  const widget = mount(Controls, { target: el, props: {model} });
  return () => unmount(widget);;
}

export default { render };