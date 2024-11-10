import importlib.metadata
import pathlib
from typing import Optional

import ipywidgets
import anywidget
import traitlets

import numpy as np
import io
import base64
import scipy.io.wavfile
# import torchaudio


try:
    __version__ = importlib.metadata.version("ipyannote")
except importlib.metadata.PackageNotFoundError:
    __version__ = "unknown"


_DEV = True  # switch to False for production

if _DEV:
    # from `npx vite`
    ESM_LABELS = "http://localhost:5173/js/labels.js?anywidget"
    ESM_CONTROLS = "http://localhost:5173/js/controls.js?anywidget"
    ESM_WAVEFORM = "http://localhost:5173/js/waveform.js?anywidget"
    CSS = ""
else:
    # from `npx vite build`
    bundled_assets_dir = pathlib.Path(__file__).parent / "static"
    ESM_LABELS = (bundled_assets_dir / "labels.mjs").read_text()
    ESM_CONTROLS = (bundled_assets_dir / "controls.mjs").read_text()
    ESM_WAVEFORM = (bundled_assets_dir / "waveform.mjs").read_text()
    CSS = (bundled_assets_dir / "style.css").read_text()


COLORS = [
    '#a1c9f4',
    '#ffb482',
    '#8de5a1',
    '#ff9f9b',
    '#d0bbff',
    '#debb9b',
    '#fab0e4',
    '#ffe700',
    '#b9f2f0'
]

class Labels(anywidget.AnyWidget):
    _esm = ESM_LABELS
    _css = CSS

    labels = traitlets.List([]).tag(sync=True)
    selected_label = traitlets.Unicode().tag(sync=True)
    colors = traitlets.List(list(COLORS)).tag(sync=True)

class Controls(anywidget.AnyWidget):
    _esm = ESM_CONTROLS
    _css = CSS

    zoom = traitlets.Integer(20).tag(sync=True) # pixels per second
    playing = traitlets.Bool(False).tag(sync=True) # are we playing or paused

class Waveform(anywidget.AnyWidget):

    _esm = ESM_WAVEFORM
    _css = CSS

    b64_audio = traitlets.Unicode().tag(sync=True)
    regions = traitlets.List().tag(sync=True)
    selected_index = traitlets.Integer(-1).tag(sync=True)
    # shared with Labels widget
    labels = traitlets.List([]).tag(sync=True)
    selected_label = traitlets.Unicode().tag(sync=True)
    colors = traitlets.List(list(COLORS)).tag(sync=True)
    # shared with Controls widget
    zoom = traitlets.Integer(20).tag(sync=True) # pixels per second
    playing = traitlets.Bool(False).tag(sync=True) # are we playing or paused

    def __init__(self, audio: Optional[str] = None, **kwargs):
        super().__init__(**kwargs)
        if audio is None:
            del self.audio
        else:
            self.audio = audio

    def to_base64(self, waveform: np.ndarray, sample_rate: int) -> str:
        with io.BytesIO() as content:
            scipy.io.wavfile.write(content, sample_rate, waveform)
            content.seek(0)
            b64 = base64.b64encode(content.read()).decode()
            b64 = f"data:audio/x-wav;base64,{b64}"
        return b64

    def set_audio(self, audio: str):
        sample_rate, waveform = scipy.io.wavfile.read(audio)
        waveform = waveform.astype(np.float32)
        waveform /= np.max(np.abs(waveform)) + 1e-8
        self.b64_audio = self.to_base64(waveform, sample_rate)
   
    def del_audio(self):
        sample_rate = 16000
        waveform = np.zeros((sample_rate, ), dtype=np.float32)
        self.b64_audio = self.to_base64(waveform, sample_rate)

    audio = property(None, set_audio, del_audio)


class IpyannoteWidget(ipywidgets.VBox):

    def __init__(self, audio: Optional[str] = None, **kwargs_):
        self._waveform = Waveform(audio, **kwargs_)
        self._labels = Labels(**kwargs_)
        self._controls = Controls(**kwargs_)
        super().__init__([self._waveform, self._labels, self._controls])
        # link widgets so they can interact
        # links to labels
        ipywidgets.link((self._labels, 'labels'), (self._waveform, 'labels'))
        ipywidgets.link((self._labels, 'colors'), (self._waveform, 'colors'))
        ipywidgets.link((self._labels, 'selected_label'), (self._waveform, 'selected_label'))
        def handle_create_label(_, content, buffers):
            if content == 'create_label':
                self._labels.send('create_label')
        self._waveform.on_msg(handle_create_label)

        # links to controls
        ipywidgets.link((self._controls, 'zoom'), (self._waveform, 'zoom'))
        ipywidgets.link((self._controls, 'playing'), (self._waveform, 'playing'))


    # properties from waveform traits - super tedious to write this for every trait
    @property
    def audio(self):
        return self._waveform.audio

    @audio.setter
    def _set_audio(self, value):
        self._waveform.audio = value

    @property
    def b64_audio(self):
        return self._waveform.b64_audio

    @b64_audio.setter
    def _set_b64_audio(self, value):
        self._waveform.b64_audio = value

    @property
    def regions(self):
        return self._waveform.regions

    @regions.setter
    def _set_regions(self, value):
        self._waveform.regions = value

    @property
    def selected_index(self):
        return self._waveform.selected_index

    @selected_index.setter
    def _set_selected_index(self, value):
        self._waveform.selected_index = value

    @property
    def labels(self):
        return self._waveform.labels

    @labels.setter
    def _set_labels(self, value):
        self._waveform.labels = value

    @property
    def selected_label(self):
        return self._waveform.selected_label

    @selected_label.setter
    def _set_selected_label(self, value):
        self._waveform.selected_label = value

    @property
    def colors(self):
        return self._waveform.colors

    @colors.setter
    def _set_colors(self, value):
        self._waveform.colors = value

    @property
    def zoom(self):
        return self._waveform.zoom

    @zoom.setter
    def _set_zoom(self, value):
        self._waveform.zoom = value

    @property
    def playing(self):
        return self._waveform.playing

    @playing.setter
    def _set_playing(self, value):
        self._waveform.playing = value



    def observe(self, handler, names=traitlets.All, type='change'):
        if hasattr(self, '_waveform'):
            # check if the widget is initialized
            self._waveform.observe(handler, names=names, type=type)
        else:
            super().observe(handler, names=names, type=type)

