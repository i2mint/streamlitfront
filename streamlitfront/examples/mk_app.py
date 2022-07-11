from front.spec_maker import APP_KEY, RENDERING_KEY, ELEMENT_KEY
from front.elements import FLOAT_INPUT_SLIDER_COMPONENT

from streamlitfront.base import mk_app


def foo(a: int = 1, b: int = 2, c=3):
    """This is foo. It computes something"""
    return (a * b) + c


def bar(x, greeting='hello'):
    """bar greets its input"""
    return f'{greeting} {x}'


def confuser(a: int, x: float = 3.14):
    return (a ** 2) * x


def proportion(x: int = 100, p: float = 0.5):
    return x * p


app = mk_app(
    [foo, bar, confuser, proportion],
    config={
        APP_KEY: {'title': 'My app'},
        RENDERING_KEY: {
            'proportion': {
                'execution': {
                    'inputs': {'p': {ELEMENT_KEY: FLOAT_INPUT_SLIDER_COMPONENT,}},
                }
            }
        },
    },
)
app()
