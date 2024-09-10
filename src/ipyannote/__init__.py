import importlib.metadata
import pathlib
from typing import Optional

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


class Widget(anywidget.AnyWidget):

    _esm = pathlib.Path(__file__).parent / "static" / "widget.js"
    _css = pathlib.Path(__file__).parent / "static" / "widget.css"

    b64_audio = traitlets.Unicode().tag(sync=True)
    regions = traitlets.List().tag(sync=True)

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

