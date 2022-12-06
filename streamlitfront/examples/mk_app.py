from typing import Literal, Optional
from front import APP_KEY, RENDERING_KEY, ELEMENT_KEY

from streamlitfront.elements import FloatSliderInput
from streamlitfront.base import mk_app
from streamlitfront.elements.elements import TextInput

# BACKEND
def foo(a: int = 1, b: int = 2, c=3):
    """This is foo. It computes something"""
    return (a * b) + c


def bar(x, greeting):
    """bar greets its input"""
    return f'{greeting} {x}'


def confuser(a: int, x: float = 3.14):
    return (a ** 2) * x


def proportion(x: int = 100, p: float = 0.5):
    return x * p


def test_int(some_int: Optional[int] = None):
    some_int = some_int or 0
    return some_int * 2


def test_str(some_str: Literal['hi', 'hola', 'coucou'] = None):
    some_str = some_str or ''
    return some_str * 2


# ======

if __name__ == '__main__':

    app = mk_app(
        # [foo, bar, confuser, proportion],
        [test_int, test_str],
        config={
            APP_KEY: {'title': 'My app'},
            RENDERING_KEY: {
                # 'foo': {
                #     'execution': {'inputs': {'a': {ELEMENT_KEY: TextInput,}},}
                # },
                'proportion': {
                    'execution': {'inputs': {'p': {ELEMENT_KEY: FloatSliderInput,}},}
                }
            },
        },
    )
    app()
