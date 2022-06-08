"""Alternative proposal for the way we do FrontElementBase now"""

from streamlitfront.util import streamlit_element_func_names

# for now, just itemgetter (or attrgetter?)
class StateGet:
    def __init__(self, key):
        self.key = key

    def __call__(self, state):
        return state[self.key]


def _resolve_values_with_state(state, args: tuple, kwargs: dict):
    def args_gen():
        for v in args:
            if isinstance(v, StateGet):
                v = v(state)
            yield v

    def kwargs_gen():
        for k, v in kwargs.items():
            if isinstance(v, StateGet):
                v = v(state)
            yield k, v

    return tuple(args_gen()), dict(kwargs_gen())


class Renderer:
    """A Renderer is a callable that makes objects parametrized by a state.

    It is like ``functools.partial` but where one can specify some values with
    ``StateGet(key)`` which will have the effect of looking for that ``key`` in the
    ``state`` when the ``Renderer`` instance is called.

    Note: it is

    >>> def test_element(a, b=2, c=3):
    ...     return a + b * c
    ...
    >>> f = Renderer(test_element, a=StateGet('a'), b=StateGet('some.thing'), c=10)
    >>>
    >>> state = {'a': 1, 'some.thing': 2}
    >>> f(state) == 21
    True
    >>>
    >>> state = {'a': 2, 'some.thing': 10}
    >>> f(state) == 102
    True
    """

    def __init__(self, func, *args, **kwargs):
        self.func = func
        self.args = args
        self.kwargs = kwargs

    def render(self, state):
        return self.func(*args, **kwargs)

    __call__ = render


from functools import wraps


# TODO: Use i2.wrapper, or other method to make renderers pickalable
# TODO: Here the renderers can be called without required fields (try slider).
#   Must raise error in that case, not wait for renderer to be called at runtime!
def mk_renderer_factory_for_func(func):
    @wraps(func)
    def renderer(*args, **kwargs):
        return Renderer(func, *args, **kwargs)

    return renderer


class StreamlitRenderers:
    """A collection of streamlit renders"""


import streamlit as st


for name in streamlit_element_func_names:
    func = getattr(st, name, None)
    if func is not None:
        setattr(
            StreamlitRenderers, name, staticmethod(mk_renderer_factory_for_func(func))
        )
    else:
        print(f'Missing {name}')
    # TODO: Add warning if func missing?
