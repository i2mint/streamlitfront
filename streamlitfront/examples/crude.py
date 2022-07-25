from front.crude import prepare_for_crude_dispatch
from front import APP_KEY, RENDERING_KEY, ELEMENT_KEY, OBJ_KEY, NAME_KEY
from collections.abc import Callable

from streamlitfront.base import mk_app
from streamlitfront.elements.elements import SelectBox, TextSection
from streamlitfront.examples.util import get_code_of_current_file


def foo(a, b: float, c: int):
    """This is foo. It computes something"""
    return a + b * c


param_to_mall_map = dict(a='a', b='b_store')
mall = dict(
    a={'one': 1, 'two': 2},
    b_store={'three': 3, 'four': 4},
    unused_store={'to': 'illustrate'}
)


def crudify(funcs):
    for func in funcs:
        yield prepare_for_crude_dispatch(
            func,
            param_to_mall_map=param_to_mall_map,
            mall=mall
        )


app = mk_app(
    [foo],
    config={
        APP_KEY: {'title': 'Crude App'},
        OBJ_KEY: {'trans': crudify},
        RENDERING_KEY: {
            'foo': {
                'execution': {
                    'inputs': {
                        'a': {
                            'options': mall['a'],
                        },
                        'b': {
                            'options': mall['b_store'],
                        },
                        str: {
                            ELEMENT_KEY: SelectBox,
                        }
                    }
                },
                'code': {
                    ELEMENT_KEY: TextSection,
                    NAME_KEY: 'Source Code',
                    'kind': 'code',
                    'language': 'python',
                    'content': get_code_of_current_file(),
                },
            }
        }
    }
)
app()