from dataclasses import dataclass
from functools import partial
from io import BytesIO
import os
from pathlib import Path
import time
from typing import Any, Iterable, Union
from dol import Files
from front.elements import DEFAULT_INPUT_KEY, OutputBase
from meshed import code_to_dag, DAG
from front import APP_KEY, RENDERING_KEY, ELEMENT_KEY, NAME_KEY, OBJ_KEY
from collections.abc import Callable
from front.crude import Crudifier, prepare_for_crude_dispatch
from streamlitfront.elements import TextInput, SelectBox
from dol.appendable import appendable
import soundfile as sf
import matplotlib.pyplot as plt

from streamlitfront import mk_app, binder as b
from streamlitfront.examples.util import Graph
from streamlitfront.elements import (
    AudioRecorder,
    FileUploader,
    MultiSourceInput,
    SuccessNotification,
)
import streamlit as st

# ============ BACKEND ============
WaveForm = Any

# rootdir = os.path.join(Path('~').expanduser(), '.front', 'edge_impluse_like')
# os.makedirs(rootdir, exist_ok=True)

# def tagged_timestamped_kv(tag_and_val_item, default_tag='untagged'):
#     utc_seconds_timestamp = int(time.time())
#     tag, val = tag_and_val_item
#     key = f"{utc_seconds_timestamp}-{tag}"

#     return key, val

# tagged_wf_store = appendable(Files, item2kv=tagged_timestamped_kv)
if not b.mall():
    b.mall = dict(tagged_wf=dict(), dummy_store=dict(),)
mall = b.mall()
crudifier = partial(Crudifier, mall=mall)


def auto_namer(*, arguments):
    return '_'.join(map(str, arguments.values()))


@crudifier(output_store='tagged_wf', auto_namer=auto_namer)
def tag_wf(wf: WaveForm, tag: str):
    return (wf, tag)


@crudifier(param_to_mall_map=dict(x='tagged_wf'))
def get_tagged_wf(x: Any):
    return x


funcs = [tag_wf, get_tagged_wf]

# ============ END BACKEND ============


# ============ FRONTEND ============
# def timestamped_kv(value):
#     utc_seconds_timestamp = str(int(time.time() * 1000))
#     return utc_seconds_timestamp, value


# AppendableFiles = appendable(Files, item2kv=timestamped_kv, return_keys=True)

# rootdir = os.path.join(Path("~").expanduser(), ".front", "edge_impulse_like")
# Path(rootdir).mkdir(parents=True, exist_ok=True)


# @dataclass
# class AudioPersister(AudioRecorder):
#     save_dir: str = None

#     def __post_init__(self):
#         super().__post_init__()
#         self.store = AppendableFiles(self.save_dir)
#         # self.store = Files(self.save_dir) if self.save_dir else None

#     def render(self):
#         audio_data = super().render()
#         if audio_data and self.store is not None:
#             key = self.store.append(audio_data)
#             return os.path.join(self.save_dir, key)
#             # self.store.append(audio_data)
#         return audio_data


class FileReader(FileUploader):
    def render(self):
        uploaded_file = super().render()
        if uploaded_file:
            return uploaded_file.getvalue()


class TaggedAudioPlayer(OutputBase):
    def render(self):
        if self.output:
            sound, tag = self.output
            arr = sf.read(BytesIO(sound), dtype='int16')[0]
            tab1, tab2 = st.tabs(['Audio Player', 'Waveform'])
            with tab1:
                st.audio(sound)
            with tab2:
                fig, ax = plt.subplots(figsize=(15, 5))
                ax.plot(arr, label=f'Tag={tag}')
                ax.legend()
                st.pyplot(fig)
                # st.write(arr[:10])


get_data_description = '''
Feed the system with wave forms from wav files or directly \
from your microphone, and tag them.
'''

config_ = {
    APP_KEY: {'title': 'Edge-Impulse-like App'},
    RENDERING_KEY: {
        'tag_wf': {
            NAME_KEY: 'Get Data',
            'description': {'content': get_data_description},
            'execution': {
                'inputs': {
                    'wf': {
                        ELEMENT_KEY: MultiSourceInput,
                        NAME_KEY: 'Wave Form',
                        'From a file': {
                            ELEMENT_KEY: FileReader,
                            'type': 'wav',
                            'display_label': False,
                        },
                        'From the microphone': {
                            ELEMENT_KEY: AudioRecorder,
                            # "save_dir": rootdir,
                        },
                    }
                },
                'output': {
                    ELEMENT_KEY: SuccessNotification,
                    'message': 'The wave form has been tagged successfully.',
                },
            },
        },
        'get_tagged_wf': {
            NAME_KEY: 'Data Explorer',
            'description': {
                'content': '''Explore the existing tagged wave forms and play them.'''
            },
            'execution': {
                'output': {ELEMENT_KEY: TaggedAudioPlayer,},
                'auto_submit': True,
            },
        },
        DAG: {'graph': {ELEMENT_KEY: Graph, NAME_KEY: 'Flow',}},
        Callable: {
            'execution': {
                'inputs': {
                    'save_name': {ELEMENT_KEY: TextInput, NAME_KEY: 'Save output as',}
                }
            }
        },
    },
}
# ============ END FRONTEND ============

if __name__ == '__main__':
    app = mk_app(funcs, config=config_)
    app()
