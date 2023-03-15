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


# ======

if __name__ == '__main__':

    app = mk_app(
        [foo, bar, confuser, proportion],
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
