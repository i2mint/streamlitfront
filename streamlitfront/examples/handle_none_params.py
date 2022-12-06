from typing import Optional
from front import APP_KEY, RENDERING_KEY, ELEMENT_KEY

from streamlitfront.elements import FloatSliderInput
from streamlitfront.base import mk_app
from streamlitfront.elements.elements import TextInput

# BACKEND
# def test(x: Optional[str] = 'test'):
#     pass


def foo(a: int = 1, b: Optional[int] = 2, c: Optional[int] = None, d: str = None):
    # def foo(a: int = 1, b: int = 2, c: int = 3, d: str = ''):
    """This is foo. It computes something"""
    b = b if b is not None else 1
    c = c if c is not None else 0
    d = d or ''
    return str((a * b) + c) + d


def bar(x: str = 'World!', greeting: str = 'Hello'):
    """bar greets its input"""
    return f'{greeting} {x}'


# ======


if __name__ == '__main__':
    app = mk_app([foo, bar], config={APP_KEY: {'title': 'Handle None Parameters'},},)
    app()
