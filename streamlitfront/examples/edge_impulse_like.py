from dataclasses import dataclass
from functools import partial
import os
from pathlib import Path
import time
from typing import Iterable
from dol import Files
from front.elements import DEFAULT_INPUT_KEY, OutputBase
from meshed import code_to_dag, DAG
from front import APP_KEY, RENDERING_KEY, ELEMENT_KEY, NAME_KEY, OBJ_KEY
from collections.abc import Callable
from front.crude import prepare_for_crude_dispatch
from streamlitfront.elements import TextInput, SelectBox
from dol.appendable import appendable

from streamlitfront.base import mk_app
from streamlitfront.examples.util import Graph
from streamlitfront.elements import (
    AudioRecorder,
    FileUploader,
    MultiSourceInputContainer,
)
import streamlit as st

# ============ BACKEND ============
WaveForm = Iterable[int]

# rootdir = os.path.join(Path('~').expanduser(), '.front', 'edge_impluse_like')
# os.makedirs(rootdir, exist_ok=True)

# def tagged_timestamped_kv(tag_and_val_item, default_tag='untagged'):
#     utc_seconds_timestamp = int(time.time())
#     tag, val = tag_and_val_item
#     key = f"{utc_seconds_timestamp}-{tag}"

#     return key, val

# tagged_wf_store = appendable(Files, item2kv=tagged_timestamped_kv)
if 'mall' not in st.session_state:
    st.session_state['mall'] = dict(
        tagged_wf=dict()
    )
mall = st.session_state['mall']
crudify = partial(prepare_for_crude_dispatch, mall=mall)


def identity(x):
    return x


@crudify(output_store='tagged_wf')
def tag_wf(wf: WaveForm, tag: str):
    return (wf, tag)


get_tagged_wf = crudify(identity, param_to_mall_map=dict(x='tagged_wf'))
get_tagged_wf.__name__ = 'get_tagged_wf'
# ============ END BACKEND ============


# ============ FRONTEND ============
def timestamped_kv(value):
    utc_seconds_timestamp = str(int(time.time() * 1000))
    return utc_seconds_timestamp, value


AppendableFiles = appendable(Files, item2kv=timestamped_kv, return_keys=True)

rootdir = os.path.join(Path('~').expanduser(), '.front', 'edge_impluse_like')

@dataclass
class AudioPersister(AudioRecorder):
    save_dir: str = None

    def __post_init__(self):
        super().__post_init__()
        self.store = AppendableFiles(self.save_dir)
        # self.store = Files(self.save_dir) if self.save_dir else None

    def render(self):
        audio_data = super().render()
        if audio_data and self.store is not None:
            print('YEAH')
            key = self.store.append(audio_data)
            return os.path.join(self.save_dir, key)
            # self.store.append(audio_data)
        return audio_data


class TaggedAudioPlayer(OutputBase):
    def render(self):
        if self.output:
            sound, tag = self.output
            if isinstance(sound, str):
                with open(sound, 'rb') as f:
                    st.audio(f)
            else:
                st.audio(sound)


get_data_description = '''
Feed the system with wave forms from wav files or directly \
from your microphone, and tag them.
'''

config_ = {
    APP_KEY: {'title': 'Edge-Impulse-like App'},
    RENDERING_KEY: {
        'tag_wf': {
            NAME_KEY: 'Get Data',
            'description': {
                'content': get_data_description
            },
            'execution': {
                'inputs': {
                    'wf': {
                        ELEMENT_KEY: MultiSourceInputContainer,
                        NAME_KEY: 'Wave Form',
                        'From a file': {
                            ELEMENT_KEY: FileUploader,
                            'type': 'wav',
                            'display_label': False
                        },
                        'From the microphone': {
                            ELEMENT_KEY: AudioPersister,
                            'save_dir': rootdir
                        },
                    }
                }
            }
        },
        'get_tagged_wf': {
            NAME_KEY: 'Data Explorer',
            'description': {
                'content': '''Explore the existing tagged wave forms and play them.'''
            },
            'execution': {
                'inputs': {
                    'x': {
                        ELEMENT_KEY: SelectBox,
                        'options': mall['tagged_wf'],
                    }
                },
                'output': {
                    ELEMENT_KEY: TaggedAudioPlayer,
                },
                'auto_submit': True
            }
        },
        DAG: {
            'graph': {
                ELEMENT_KEY: Graph,
                NAME_KEY: 'Flow',
            }
        },
        Callable: {
            'execution': {
                'inputs': {
                    'save_name': {
                        ELEMENT_KEY: TextInput,
                        NAME_KEY: 'Save output as',
                    }
                }
            }
        }
    }
}

app = mk_app([tag_wf, get_tagged_wf], config=config_)
app()
st.write(mall)
# ============ END FRONTEND ============
