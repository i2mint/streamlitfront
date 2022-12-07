"""Alternative proposal for the way we do FrontElementBase now"""


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
        return self.func(state)

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
from importlib_resources import files  # importlib.resources once only 3.9+ maintained


data_files = files('streamlitfront').joinpath('data')


streamlit_element_func_names = list(
    filter(None, data_files.joinpath('streamlit_elements.txt').read_text().split('\n'))
)


for name in streamlit_element_func_names:
    func = getattr(st, name, None)
    if func is not None:
        setattr(
            StreamlitRenderers, name, staticmethod(mk_renderer_factory_for_func(func))
        )
    else:
        print(f'Missing {name}')
    # TODO: Add warning if func missing?


renderers = StreamlitRenderers()

# ------------------
from functools import partial
from typing import Callable
from types import MethodType

from i2 import Sig, call_forgivingly, name_of_obj
from front.elements import FrontComponentBase, implement_component


# TODO: Add render type (protocol?)
def _empty_render(self):
    pass


# TODO: Make this more robust -- scary as is.
# TODO: Setup for pickability, but it's not yet
def mk_component_base(
    component_factory: Callable,
    base_cls: type = FrontComponentBase,
    render: Callable = _empty_render,
    name: str = None,
) -> type:
    # TODO: could "camelize" name_of_obj output.
    name = name or name_of_obj(component_factory) or 'ComponentBase'
    component_sig = Sig(component_factory)
    sig: Sig = 'self' + component_sig + Sig(base_cls)

    @sig
    def __init__(*args, **kwargs) -> None:
        kw = sig.kwargs_from_args_and_kwargs(args, kwargs, apply_defaults=True)
        self = kw.pop('self')
        call_forgivingly(base_cls.__init__, self, **kw)
        for name in component_sig:
            if not hasattr(self, name):
                setattr(self, name, kw[name])

    return type(name, (base_cls,), {'__init__': __init__, 'render': render})


def implement_component_from_factory(
    component_factory: Callable,
    base_cls: type = FrontComponentBase,
    *,
    input_value_callback: Callable = None,
    render=_empty_render,
    name=None,
    **input_mapping,
):
    ComponentBaseClass = mk_component_base(
        component_factory, base_cls, render=render, name=name
    )
    return implement_component(
        ComponentBaseClass,
        component_factory,
        input_value_callback=input_value_callback,
        **input_mapping,
    )


# test of mk_component_base
def test_mk_component_base():
    import streamlit as st
    from front.elements import InputBase

    C = mk_component_base(st.audio, InputBase)

    # verify that the arguments of C is the aggregation of the arguments of audio and
    # InputBase:
    assert sorted(Sig(C).names) == sorted((Sig(st.audio) + Sig(InputBase)).names)

    c = C(1, name='tag')
    assert (c.data, c.name) == (1, 'tag')


def test_implement_component_from_factory():
    from front.elements import InputBase

    component = implement_component_from_factory(st.audio, InputBase)
    assert sorted(Sig(component).names) == sorted(
        (Sig(st.audio) + Sig(InputBase)).names
    )
