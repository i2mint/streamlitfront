"""Render a stream"""
import time
from collections import deque
from functools import partial

import numpy as np
from stream2py import StreamBuffer
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


def window_gen(data_gen, window_size=10):
    timestamp, in_data, _, _, status_flags = next(iter(data_gen), None)
    arr = np.frombuffer(in_data, dtype='int16')
    data = deque(maxlen=window_size)
    wf_arr = np.ones(len(arr) * window_size)
    item = dict(
        timestamp=timestamp,
        wf=arr,
        mean=np.mean(arr),
        max=np.max(arr),
        flag=str(PaStatusFlags(status_flags)),
    )
    yield wf_arr, item
    for d in data_gen:
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
        wf_arr = np.concatenate((wf_arr[len(arr) :], arr))
        yield wf_arr, item


class AudioStreamInfo(OutputBase):
    def render(self):
        if self.output:
            box = st.empty()
            chart = st.line_chart([1])
            buffer_reader = self.output.mk_reader()
            for wf_arr, item in window_gen(buffer_reader):
                new_chart = st.line_chart(wf_arr, width=800, height=600)
                chart.empty()
                chart = new_chart
                with box.container():
                    st.write(
                        f'Render delay: {time.time() - item["timestamp"] / 1e6:.2f}s'
                    )


class AudioStreamInfo1(OutputBase):
    def render(self):
        if self.output:
            box = st.empty()
            buffer_reader = self.output.mk_reader()
            for wf_arr, item in window_gen(buffer_reader):
                with box.container():
                    fig, ax = plt.subplots(figsize=(15, 5))
                    st.markdown('## waveform')
                    ax.plot(wf_arr, label='wf')
                    st.pyplot(fig)
                    st.write(item)
                    st.write(f'Render delay: {time.time()-item["timestamp"]/1e6:.2f}s')
                    plt.close(fig)


@crudifier(output_store='source')
def audio_stream(input_device, rate=44100, width=2, channels=1):
    source_reader = PyAudioSourceReader(
        rate=rate,
        width=width,
        channels=channels,
        input_device=input_device,
        frames_per_buffer=int(rate / 5),
    )
    source = StreamBuffer(source_reader=source_reader, maxlen=100)  # buffer
    if mall['source']:  # DO THIS IN crudifier
        try:
            mall['source'].stop()
            mall['source'] = None
        except Exception as e:
            print(e)
    source.start()
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
