from distutils.command.config import config
from typing import Iterable

from streamlitfront.base import mk_app
from front.elements import FILE_UPLOADER_COMPONENT, AUDIO_RECORDER_COMPONENT, INT_INPUT_SLIDER_COMPONENT
from meshed import code_to_dag, DAG


WaveForm = Iterable[int]


@code_to_dag
def learn_model(train_audio: WaveForm, raw_audio_learner):
    model = learn_model(train_audio, raw_audio_learner)


app = mk_app(
    [learn_model],
    config={
        'app': {'title': 'Simple Real Audio ML'},
        'rendering': {
            DAG: {
                'execution': {
                    'inputs': {
                        'train_audio': {
                            'From a file':{
                                'component': FILE_UPLOADER_COMPONENT,
                                'type': 'wav'
                            },
                            'From the microphone':{
                                'component': AUDIO_RECORDER_COMPONENT
                            },
                        }
                    },
                },
                # 'image': {
                #     'container': SECTION_CONTAINER,
                #     'name': 'Flow',
                #     'component': GRAPH_COMPONENT,
                #     'display': True,
                #     'display_for_single_node': False,
                #     # from operators import method
                #     # 'image_render_callback': ,
                # },
            }
        },
    },
)
app()
