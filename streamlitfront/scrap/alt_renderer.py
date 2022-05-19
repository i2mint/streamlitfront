"""Alternative proposal for the way we do FrontElementBase now"""

from functools import partial

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

    # Since self.kwargs is (should) fixed, could curry it out and use curried in
    # __call__ instead of calling _resolve_values_with_state directly (see (*))
    #         self.resolve_inputs = partial(
    #               _resolve_values_with_state, d=kwargs
    #           )

    def render(self, state):
        args, kwargs = _resolve_values_with_state(state, self.args, self.kwargs)
        # (*) could be this instead:
        # args, kwargs = self.resolve_inputs(state)
        return self.func(*args, **kwargs)

    __call__ = render
