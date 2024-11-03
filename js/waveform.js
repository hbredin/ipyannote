import "./widget.css";
import Waveform from "./Waveform.svelte";
import { mount, unmount } from 'svelte';

function render({ model, el }) {
  const widget = mount(Waveform, { target: el, props: {model} });
  return () => unmount(widget);;
}

export default { render };

