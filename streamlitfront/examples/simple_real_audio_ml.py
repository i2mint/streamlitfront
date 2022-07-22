from typing import Iterable
from meshed import code_to_dag, DAG
from front.elements import (
    FILE_UPLOADER_COMPONENT,
    AUDIO_RECORDER_COMPONENT,
    MULTI_SOURCE_INPUT_CONTAINER,
    FrontComponentBase,
)
from front.spec_maker import APP_KEY, RENDERING_KEY, ELEMENT_KEY, NAME_KEY

from streamlitfront.base import mk_app
from streamlitfront.examples.graph_component import Graph
from streamlitfront.elements import MultiSourceInputContainer, FileUploader, AudioRecorder


WaveForm = Iterable[int]


@code_to_dag
def learn_model(train_audio: WaveForm, raw_audio_learner):
    model = learn_model(train_audio, raw_audio_learner)


config_ = {
    APP_KEY: {'title': 'Simple Real Audio ML'},
    RENDERING_KEY: {
        DAG: {
            'execution': {
                'inputs': {
                    'train_audio': {
                        ELEMENT_KEY: MultiSourceInputContainer,
                        'From a file': {
                            ELEMENT_KEY: FileUploader,
                            'type': 'wav',
                        },
                        'From the microphone': {ELEMENT_KEY: AudioRecorder},
                    }
                },
            },
            'graph': {ELEMENT_KEY: Graph, NAME_KEY: 'Flow',},
        }
    },
}

app = mk_app([learn_model], config=config_)
app()
