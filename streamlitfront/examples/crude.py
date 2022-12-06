from front.crude import prepare_for_crude_dispatch
from front import APP_KEY, RENDERING_KEY, ELEMENT_KEY, OBJ_KEY, NAME_KEY
from collections.abc import Callable
from i2 import Sig
import streamlit as st

from streamlitfront import mk_app, binder as b
from streamlitfront.elements.elements import SelectBox, TextInput, TextSection
from streamlitfront.examples.util import get_code_of_current_file


def foo(a, b: float):
    """This is foo. It computes something"""
    return a + b


def bar(foo_output: float):
    return foo_output * 10


if __name__ == '__main__':
    # param_to_mall_map = dict(a='a', b='b_store')

    if not b.mall():
        b.mall = dict(
            a=dict(one=1, two=2),
            b=dict(three=3, four=4),
            foo_output=dict(),
            bar_output=dict(),
        )

    mall = b.mall()

    foo = prepare_for_crude_dispatch(
        foo,
        mall=mall,
        param_to_mall_map=list(Sig(foo)),
        # output_store = f'{foo.__name__}_output'
    )
    bar = prepare_for_crude_dispatch(
        bar,
        mall=mall,
        param_to_mall_map=list(Sig(bar)),
        # output_store = f'{bar.__name__}_output'
    )

    # def crudify(funcs):
    #     for func in funcs:
    #         param_to_mall_map = list(Sig(func))
    #         output_store = f'{func.__name__}_output'
    #         yield prepare_for_crude_dispatch(
    #             func,
    #             param_to_mall_map=param_to_mall_map,
    #             mall=mall,
    #             output_store=output_store,
    #         )

    app = mk_app(
        [foo, bar],
        config={
            APP_KEY: {'title': 'Crude App'},
            # OBJ_KEY: {'trans': crudify},
            RENDERING_KEY: {
                Callable: {
                    'execution': {
                        'inputs': {
                            'save_name': {
                                ELEMENT_KEY: TextInput,
                                NAME_KEY: 'Save output as',
                            },
                            str: {ELEMENT_KEY: SelectBox,},
                        }
                    },
                    # 'code': {
                    #     ELEMENT_KEY: TextSection,
                    #     NAME_KEY: 'Source Code',
                    #     'kind': 'code',
                    #     'language': 'python',
                    #     'content': get_code_of_current_file(),
                    # },
                },
            },
        },
    )
    app()
    st.write(mall)
