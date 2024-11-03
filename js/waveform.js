import "./widget.css";
import Widget from "./Widget.svelte";
import { mount, unmount } from 'svelte';

function render({ model, el }) {
  const widget = mount(Widget, { target: el, props: {model} });
  return () => unmount(widget);;
}

export default { render };

