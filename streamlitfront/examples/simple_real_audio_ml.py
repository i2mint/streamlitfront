from typing import Iterable
from meshed import code_to_dag, DAG
from front import APP_KEY, RENDERING_KEY, ELEMENT_KEY, NAME_KEY

from streamlitfront.base import mk_app
from streamlitfront.examples.util import Graph
from streamlitfront.elements import (
    AudioRecorder,
    FileUploader,
    MultiSourceInput,
)


WaveForm = Iterable[int]


@code_to_dag
def learn_model(train_audio: WaveForm, raw_audio_learner):
    model = learn_model(train_audio, raw_audio_learner)


config_ = {
    APP_KEY: {'title': 'Simple Real Audio ML'},
    RENDERING_KEY: {
        DAG: {
            'description': {'content': 'A very simple learn model example.'},
            'execution': {
                'inputs': {
                    'train_audio': {
                        ELEMENT_KEY: MultiSourceInput,
                        'From a file': {ELEMENT_KEY: FileUploader, 'type': 'wav',},
                        'From the microphone': {ELEMENT_KEY: AudioRecorder},
                    }
                },
            },
            'graph': {ELEMENT_KEY: Graph, NAME_KEY: 'Flow',},
        }
    },
}

if __name__ == '__main__':
    app = mk_app([learn_model], config=config_)
    app()
