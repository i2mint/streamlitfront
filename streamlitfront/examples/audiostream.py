"""Render a stream"""
from collections import deque
from functools import partial

import numpy as np
from audiostream2py import PyAudioSourceReader, PaStatusFlags

import streamlit as st
from front import APP_KEY, RENDERING_KEY, ELEMENT_KEY, Crudifier, NAME_KEY
from front.elements import OutputBase
import matplotlib.pyplot as plt

from streamlitfront import mk_app, binder as b
from streamlitfront.elements import SelectBox


if not b.mall():
    b.mall = dict(
        input_device=PyAudioSourceReader.list_recording_devices(), source=None,
    )

mall = b.mall()
crudifier = partial(Crudifier, mall=mall)


class AudioStreamInfo(OutputBase):
    def render(self):
        if self.output:
            box = st.empty()
            data = deque(maxlen=10)
            for d in self.output:
                timestamp, in_data, _, _, status_flags = d
                arr = np.frombuffer(in_data, dtype='int16')
                item = dict(
                    timestamp=timestamp,
                    wf=arr,
                    mean=np.mean(arr),
                    max=np.max(arr),
                    flag=str(PaStatusFlags(status_flags)),
                )
                data.append(item)
                wf_arr = (
                    np.concatenate(tuple(i['wf'] for i in data))
                    if len(data) > 1
                    else arr
                )
                with box.container():
                    fig, ax = plt.subplots(figsize=(15, 5))
                    st.markdown('## waveform')
                    ax.plot(wf_arr, label='wf')
                    st.pyplot(fig)
                    st.write(item)


@crudifier(output_store='source')
def audio_stream(input_device, rate=44100, width=2, channels=1):
    source = PyAudioSourceReader(
        rate=rate,
        width=width,
        channels=channels,
        input_device=input_device,
        frames_per_buffer=int(rate),
    )
    if mall['source']:  # DO THIS IN crudifier
        try:
            mall['source'].close()
            mall['source'] = None
        except Exception as e:
            print(e)
    source.open()
    return source


if __name__ == '__main__':
    app = mk_app(
        [audio_stream],
        config={
            APP_KEY: {'title': 'My Stream App'},
            RENDERING_KEY: {
                'audio_stream': {
                    NAME_KEY: 'Get Data Stream',
                    'description': {'content': 'Configure soundcard for data stream'},
                    'execution': {
                        'inputs': {
                            'input_device': {
                                ELEMENT_KEY: SelectBox,
                                'options': mall['input_device'],
                            }
                        },
                        'output': {ELEMENT_KEY: AudioStreamInfo},
                    },
                },
            },
        },
    )
    app()
