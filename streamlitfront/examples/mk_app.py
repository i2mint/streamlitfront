from distutils.command.config import config

from streamlitfront.base import mk_app
from front.elements import FLOAT_INPUT_SLIDER_COMPONENT


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
        'app': {'title': 'My app'},
        # 'obj': {
        #     'bindings': {
        #         'Foo.a': 'Proportion.x'
        #     }
        # }
        'rendering': {
            'Proportion': {
                'inputs': {'p': {'component': FLOAT_INPUT_SLIDER_COMPONENT,}},
            }
        },
    },
)
app()
