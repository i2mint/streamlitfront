from know.boxes import *
from functools import partial
from typing import Callable, Iterable
from front import APP_KEY, RENDERING_KEY, ELEMENT_KEY, NAME_KEY
from i2 import Pipe, Sig
from front.crude import Crudifier

from streamlitfront import mk_app, binder as b
from streamlitfront.elements import (
    SelectBox,
    SuccessNotification,
    KwargsInput,
    PipelineMaker,
)

if not b.mall():
    b.mall = dict(
        step_factories=dict(
            # Source Readers
            files_of_folder=FuncFactory(Files),
            files_of_zip=FuncFactory(FilesOfZip),
            # Store Transformers
            key_transformer=key_transformer,
            val_transformer=val_transformer,
            key_filter=filter_keys,
            extract_extension=FuncFactory(extract_extension),
            # Object Transformation
            make_codec=make_decoder,
            # Boolean Functions
            regular_expression_filter=regular_expression_filter,
            make_function_conjunction=make_function_conjunction,
        ),
        steps=dict(),
        pipelines=dict(),
        # exec_outputs=dict(),
    )
mall = b.mall()
if not b.selected_step_factory():
    b.selected_step_factory = 'files_of_folder'

crudifier = partial(Crudifier, mall=mall)


@crudifier(param_to_mall_map=dict(step_factory='step_factories'), output_store='steps')
def mk_step(step_factory: Callable, kwargs: dict):
    return partial(step_factory, **kwargs)


@crudifier(output_store='pipelines')
def mk_pipeline(steps: Iterable[Callable]):
    return Pipe(*steps)


@crudifier(
    param_to_mall_map=dict(pipeline='pipelines'),
    # output_store='exec_outputs'
)
def exec_pipeline(pipeline: Callable, kwargs):
    return pipeline(**kwargs)


def get_step_name(step):
    return [k for k, v in mall['steps'].items() if v == step][0]


def get_selected_pipeline_sig():
    if not b.selected_pipeline():
        return Sig()
    return Sig(mall['pipelines'][b.selected_pipeline()])


config = {
    APP_KEY: {'title': 'Data Preparation'},
    RENDERING_KEY: {
        'mk_step': {
            NAME_KEY: 'Pipeline Step Maker',
            'execution': {
                'inputs': {
                    'step_factory': {
                        ELEMENT_KEY: SelectBox,
                        'options': mall['step_factories'],
                        'value': b.selected_step_factory,
                    },
                    'kwargs': {
                        ELEMENT_KEY: KwargsInput,
                        'func_sig': Sig(
                            mall['step_factories'][b.selected_step_factory()]
                        ),
                    },
                },
                'output': {
                    ELEMENT_KEY: SuccessNotification,
                    'message': 'The step has been created successfully.',
                },
            },
        },
        'mk_pipeline': {
            NAME_KEY: 'Pipeline Maker',
            'execution': {
                'inputs': {
                    'steps': {
                        ELEMENT_KEY: PipelineMaker,
                        'items': list(mall['steps'].values()),
                        'serializer': get_step_name,
                    },
                },
                'output': {
                    ELEMENT_KEY: SuccessNotification,
                    'message': 'The pipeline has been created successfully.',
                },
            },
        },
        'exec_pipeline': {
            NAME_KEY: 'Pipeline Executor',
            'execution': {
                'inputs': {
                    'pipeline': {
                        ELEMENT_KEY: SelectBox,
                        'options': mall['pipelines'],
                        'value': b.selected_pipeline,
                    },
                    'kwargs': {
                        ELEMENT_KEY: KwargsInput,
                        'func_sig': get_selected_pipeline_sig(),
                    },
                }
            },
        },
    },
}

if __name__ == '__main__':
    funcs = [mk_step, mk_pipeline, exec_pipeline]
    app = mk_app(funcs, config=config)
    app()
