"""Utils"""
from functools import partial
from typing import TypeVar, Iterable, Dict
from i2.signatures import Sig, name_of_obj

from importlib_resources import files  # importlib.resources once only 3.9+ maintained
import streamlit.bootstrap


data_files = files('streamlitfront').joinpath('data')

streamlit_element_func_names = list(
    filter(None, data_files.joinpath('streamlit_elements.txt').read_text().split('\n'))
)


run_streamlit = partial(
    streamlit.bootstrap.run, command_line='', args=[], flag_options={}
)

from i2._deprecated import Command as _Command

# TODO: Consider using functools.partial (or subclass thereof) instead of Command
class Command(_Command):
    def _caller(self):
        def exaecute_commands_in_args():
            for v in self.args:
                if isinstance(v, Command):
                    v = v()  # if a command, execute it
                yield v

        def execute_commands_in_kwargs():
            for k, v in self.kwargs.items():
                if isinstance(v, Command):
                    v = v()  # if a command, execute it
                yield k, v

        return self.func(
            *exaecute_commands_in_args(), **dict(execute_commands_in_kwargs()),
        )


PositionalTypes = TypeVar(
    'PositionalTypes', Iterable[int], Iterable[float], Iterable[str], Iterable[bool]
)
KeywordTypes = TypeVar(
    'KeywordTypes', Dict[str, int], Dict[str, float], Dict[str, str], Dict[str, bool]
)


def incremental_str_maker(str_format='{:03.f}'):
    """Make a function that will produce a (incrementally) new string at every call."""
    i = 0

    def mk_next_str():
        nonlocal i
        i += 1
        return str_format.format(i)

    return mk_next_str


unnamed_page = incremental_str_maker(str_format='UnnamedPage{:03.0f}')


def func_name(func):
    """The func.__name__ of a callable func, or makes and returns one if that fails.
    To make one, it calls unamed_func_name which produces incremental names to reduce the chances of clashing"""
    name = name_of_obj(func)
    if name is None or name == '<lambda>':
        return unnamed_page()
    return name


class Objdict(dict):
    """A dict, whose keys can be access as if they were attributes.

    >>> s = Objdict()

    Write it as you do with attributes or dict keys,
    get it as an attribute and a dict keys.

    >>> s.foo = 'bar'
    >>> assert s.foo == 'bar'
    >>> assert s['foo'] == 'bar'
    >>> s['hello'] = 'world'
    >>> assert s.hello == 'world'
    >>> assert s['hello'] == 'world'
    >>> hasattr(s, 'hello')
    True

    And you can still do dict stuff with it...

    >>> list(s)
    ['foo', 'hello']
    >>> list(s.items())
    [('foo', 'bar'), ('hello', 'world')]
    >>> s.get('key not there', 'nope')
    'nope'
    >>> s.clear()
    >>> assert len(s) == 0

    Note: You can use anything that's a valid dict key as a key

    >>> s['strings with space'] = 1
    >>> s[42] = 'meaning of life'
    >>> s[('tuples', 1, None)] = 'weird'
    >>> list(s)
    ['strings with space', 42, ('tuples', 1, None)]

    But obviously, the only ones you'll be able to access are those that are
    valid attribute names.
    """

    def __getattr__(self, name):
        if name in self:
            return self[name]
        else:
            raise AttributeError('No such attribute: ' + name)

    def __setattr__(self, name, value):
        self[name] = value

    def __delattr__(self, name):
        if name in self:
            del self[name]
        else:
            raise AttributeError('No such attribute: ' + name)


def attr_or_key(obj, k):
    """Get data for `k` by doing obj.k, or obj[k] if k not an attribute of obj

    >>> d = {'a': 1, 2: 'b', '__class__': 'do I win?'}
    >>> attr_or_key(d, 'a')
    1
    >>> attr_or_key(d, 2)
    'b'
    >>> attr_or_key(d, '__class__')
    <class 'dict'>

    That last one shows that `attr_or_key` will also look in attributes to find
    the data of `k`. In fact, it looks there first, before using [k].
    That's why we got the dict type returned, and not the 'do I win?' string.
    Because `d` has an attribute called `__class__` (like... well... all python
    objects do).

    """
    if isinstance(k, str) and hasattr(obj, k):
        return getattr(obj, k)
    else:
        return obj.__getitem__(k)


def attr_or_key_with_dotpaths(obj, k):
    """Get k-data from obj hwere k is a path of keys and attributes leading to the data.

    >>> attr_or_key_with_dotpaths({'a': {'b': 3}}, 'a.b')
    3
    """
    if isinstance(k, str):
        _obj = obj
        for kk in k.split('.'):
            _obj = attr_or_key(_obj, kk)
        return _obj
    else:
        return attr_or_key(obj, k)


class NodeGetter:
    """
    A accessing nested (i.e. tree-like) data as data['a', 'b', 'c']
    instead of data['a']['b']['c']
    This is the base to be able to define other path-based ways to see nested data.
    For example:
        data['a.b.c'.split('.')]

    >>> d = {
    ...     'a': 'simple',
    ...     'b': {'is': 'nested'},
    ...     'c': {'is': 'nested', 'and': 'has', 'a': [1, 2, 3]}
    ... }
    >>> g = NodeGetter(d)
    >>>
    >>> assert g['a'] == 'simple'
    >>> assert g['b', 'is'] == 'nested'
    >>> assert g['c', 'a'] == [1, 2, 3]
    >>> assert g['c', 'a', 1] == 2
    >>>
    >>> assert d['c']['a'][1] == 2  # it's to avoid accessing it this way.
    >>> # But can also expand on this and do things like:
    >>> assert g['b.is'.split('.')] == 'nested'
    >>> assert g['c/a'.split('/')] == [1, 2, 3]
    >>> # ... or subclass/wrap NodeGetter to do it automatically, given a protocol
    >>>
    >>> def int_if_possible(x):
    ...     try:
    ...         return int(x)
    ...     except ValueError:
    ...         return x
    >>> p = lambda k: map(int_if_possible, k.split('.'))
    >>> assert g[p('c.a.1')] == 2
    """

    def __init__(self, src, item_getter=attr_or_key_with_dotpaths):
        self.src = src
        self.item_getter = item_getter

    def __getitem__(self, path):
        _src = self.src
        for k in path:
            try:
                _src = self.item_getter(_src, k)
            except Exception as e:
                raise KeyError(f'Accessing {path} produced an error: {e}')
        return _src


# Note: Started this in case we need more access flexibility
# from glom import glom, Path
# class Glommed:
#     """Wraps nested structure (like a dict) so that elements are accessed with glom
#
#     See glome docs: https://glom.readthedocs.io/en/latest/
#
#     >>> d =
#     """
#
#     def __init__(self, target):
#         self.target = target
#
#     def __getitem__(self, keys):
#         """Get a value from a path of keys"""
#         return glom(self.target, Path(*keys))
#
#     def __call__(self, *keys):
#         """Get a glommed instance from the value of a path of keys"""
#         return Glommed(target=self[keys])


def build_factory(element_factory, kind, idx):
    """
    Build the factory for user input for VP and VK inputs
    """
    factory = element_factory[f'{kind}_factory']
    kwargs = {'label': f'Enter {kind} {idx + 1}', 'key': idx}
    if element_factory[f'{kind}_type'] is int:
        kwargs['value'] = 0
    val = factory(**kwargs)
    return val


# TODO: consider changing the following command factories to return
#  partial(factory, **factory_kwargs) instead
def build_element_commands(
    name, inferred_type, element_factory_for_annot, missing, dflt_element_factory
):
    """
    Build the element factory for each argument to allow for user input
    """
    if inferred_type in PositionalTypes.__constraints__:
        element_factory, factory_kwargs = build_element_factory_helper(
            element_factory_for_annot, inferred_type, missing, 'positional'
        )
    elif inferred_type in KeywordTypes.__constraints__:
        element_factory, factory_kwargs = build_element_factory_helper(
            element_factory_for_annot, inferred_type, missing, 'keyword'
        )
    elif inferred_type is not missing:
        element_factory = element_factory_for_annot.get(inferred_type, missing)
        factory_kwargs = {'label': name}
    else:
        element_factory = dflt_element_factory
        factory_kwargs = {'label': name}
    return element_factory, factory_kwargs


def build_element_factory(
    name, inferred_type, element_factory_for_annot, missing, dflt_element_factory
):
    """
    Build the element factory for each argument to allow for user input
    """
    if inferred_type in PositionalTypes.__constraints__:
        element_factory, factory_kwargs = build_element_factory_helper(
            element_factory_for_annot, inferred_type, missing, 'positional'
        )
    elif inferred_type in KeywordTypes.__constraints__:
        element_factory, factory_kwargs = build_element_factory_helper(
            element_factory_for_annot, inferred_type, missing, 'keyword'
        )
    elif inferred_type is not missing:
        element_factory = element_factory_for_annot.get(inferred_type, missing)
        factory_kwargs = {'label': name}
    else:
        element_factory = dflt_element_factory
        factory_kwargs = {'label': name}
    return element_factory, factory_kwargs


def build_element_factory_helper(
    element_factory_for_annot, inferred_type, missing, args
):
    """
    Helper to build the element factory for VP and VK arguments
    """
    if args == 'positional':
        element_factory = {
            'base': element_factory_for_annot.get(inferred_type, missing)[0],
            'input_type': element_factory_for_annot.get(inferred_type, missing)[1],
            'input_factory': element_factory_for_annot.get(
                element_factory_for_annot.get(inferred_type, missing)[1], missing
            ),
        }
    else:
        element_factory = {
            'base': element_factory_for_annot.get(inferred_type, missing)[0],
            'key_type': element_factory_for_annot.get(inferred_type, missing)[1],
            'key_factory': element_factory_for_annot.get(
                element_factory_for_annot.get(inferred_type, missing)[1], missing
            ),
            'value_type': element_factory_for_annot.get(inferred_type, missing)[2],
            'value_factory': element_factory_for_annot.get(
                element_factory_for_annot.get(inferred_type, missing)[2], missing
            ),
        }
    factory_kwargs = {
        'label': 'Enter the number of positional arguments you would like to pass',
        'value': 0,
    }

    return element_factory, factory_kwargs
