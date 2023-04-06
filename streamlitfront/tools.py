"""Tools made with streamlitfront

"""

from typing import Iterable, Tuple, Callable, KT, VT, Any, Dict
from streamlitfront.base import mk_app, Map
from front import RENDERING_KEY, NAME_KEY, ELEMENT_KEY
from front.elements import OutputBase

from i2 import name_of_obj, Pipe

# ------------------------------------------------------------------------------
# Config validation


# TODO: Make it plugin-able. User should be able to chose what and how to validate.
#  By "what" I mean what conditions to check, and by "how" I mean what to do when
#  a condition is not met. Here we raise an exception, but we could just warn the user,
#  or modify the config, or whatever.
def validate_config(configs: dict, funcs):
    func_names = [name_of_obj(f) for f in funcs]
    render_names_not_in_funcs = set(
        filter(
            lambda x: isinstance(x, str), set(configs[RENDERING_KEY]) - set(func_names)
        )
    )
    if render_names_not_in_funcs:
        raise ValueError(
            f'Render names not matched to func name: {render_names_not_in_funcs}\n'
            f'Your func names are: {func_names}'
        )
    # func_names_not_in_render = set(func_names) - set(configs[RENDERING_KEY])


# ------------------------------------------------------------------------------
# Output rendering factory

# TODO: Perhaps front itself should use this to cast non-OutputBase callables?
# TODO: Make it more general, and picklable
#  Take https://github.com/i2mint/streamlitfront/blob/79e4a6c0bcc53c26c164a40d58eb4ada50cc87b6/streamlitfront/examples/custom_output.py#L17
#  as an target example, or something like it. Use dataclasses with top level class
def mk_output_renderer(*output_trans: Callable, name=None):
    output_trans_pipe = Pipe(*output_trans)

    class CustomRenderer(OutputBase):
        def render(self):
            return output_trans_pipe(self.output)

    if name:
        CustomRenderer.__name__ = name
    return CustomRenderer


# ------------------------------------------------------------------------------
# Render edits

from itertools import chain
from i2 import mk_sentinel
from dol.paths import Edits
from typing import Hashable, NewType

RenderKey = NewType('RenderKey', Hashable)
RenderKeyEdits = Dict[str, dict]
# Why do the following make mypy complain?
# RenderKeyEdits = NewType('RenderKeyEdits', Dict[RenderKey, Edits])
# RenderKeyEdits = NewType('RenderKeyEdits', Dict[str, dict])

NoChanges = mk_sentinel('NoChanges')


def render_edits(render_key_edits: RenderKeyEdits):
    return chain.from_iterable(
        render_edits_gen(render_key, **edits)
        for render_key, edits in render_key_edits.items()
    )


# TODO: Make this into a plugin architecture
def render_edits_gen(
    render_key,
    output_trans=NoChanges,
    name_key=NoChanges,
    description_content=NoChanges,
):
    _render_key = (RENDERING_KEY, render_key)
    if output_trans is not NoChanges:
        yield _render_key + ('execution', 'output', ELEMENT_KEY), output_trans
    if name_key is not NoChanges:
        yield _render_key + (NAME_KEY,), name_key
    if description_content is not NoChanges:
        yield _render_key + ('description', 'content'), description_content


# ------------------------------------------------------------------------------
# 1. Render keys

KV = Tuple[KT, VT]

# def validate_bijection(objs, config):
#     object_names = list(map(name_of_obj, objs))
#     if set(object_names) != set(get_render_keys(config)):
#         raise ValueError(f"The object names don't match the render keys of configs")


# TODO: Make one that is smarter than taking first (example, take closest in mro)
def first_element_matching_type(obj, types):
    """returns the first type found that obj is an instance of"""
    for type_ in types:
        if isinstance(obj, type_):
            return type_
    # else return None


OBJECT = 'OBJECT'
NAME_OF_OBJ = 'NAME_OF_OBJ'
SUBTYPE = 'SUBTYPE'


# TODO: Finish. Intened to be used with _find_render_keys function that handles a
#  single obj (do we need global view?)
# TODO: Replace if/elif statement by parametrized function + factory that produces
#  this function based on rules. (Routing, once again).
# def _find_val(objs, render_keys: dict):
#     """Generates render config items for each object"""
#     # TODO: raise specific error with more info instead of assert:
#     objs = list(objs)
#     assert len(set(objs)) == objs, f"Some of your objects weren't unique"
#
#     for obj in objs:
#         if obj in render_keys:
#             yield OBJECT, (obj, render_keys[obj])
#         elif name_of_obj(obj) in render_keys:
#             yield NAME_OF_OBJ, (name_of_obj(obj), render_keys[name_of_obj(obj)])
#         elif (type_ := first_element_matching_type(
#                 SUBTYPE, (obj, filter(lambda x: isinstance(x, type), render_keys))
#         )) is not None:
#             yield type_, name_of_obj(type_)
#         else:
#             # TODO: More significant error (perhaps list ALL the objects that are not
#             #  mapped and suggest what to do about it (given the specific objects and
#             #  render keys).
#             raise ValueError(
#                 f"Object couldn't be mapped to a render_keys key: {obj}"
#             )

# TODO: Extract routing logic (the if/elifs) and expose control to interface
def _find_render_keys(objs, render_keys: dict):
    """Make a static configs that has a one to one relationship with objects"""
    # TODO: raise specific error with more info instead of assert:
    assert set(objs) == set(objs), f"Some of your objects weren't unique"

    for obj in objs:
        yield from __find_render_keys(obj, render_keys)


def __find_render_keys(obj, render_keys):
    if obj in render_keys:
        return OBJECT, (obj, render_keys[obj])
    elif name_of_obj(obj) in render_keys:
        return NAME_OF_OBJ, (name_of_obj(obj), render_keys[name_of_obj(obj)])
    elif (
        type_ := first_element_matching_type(
            SUBTYPE, (obj, filter(lambda x: isinstance(x, type), render_keys))
        )
    ) is not None:
        return type_, name_of_obj(type_)
    else:
        # TODO: More significant error (perhaps list ALL the objects that are not
        #  mapped and suggest what to do about it (given the specific objects and
        #  render keys).
        raise ValueError(f"Object couldn't be mapped to a render_keys key: {obj}")


def _map_render_keys(objs, render_keys: Iterable[KV]):
    """Translate render_keys to render_keys that can be handled by front"""
    for kind, (key, rendering_specs) in render_keys:
        if kind == OBJECT:
            obj = key
            yield name_of_obj(obj), rendering_specs
        else:
            yield key, rendering_specs


def mk_render_keys(objs, render_keys, find_render_keys: Callable = _find_render_keys):
    """Make a static render_keys that has a one-to-one relationship with objects

    # >>> find_render_keys = lambda objs, render_keys:
    # >>> dict(mk_render_keys([1, 2, 3], {1: 'a', 2: 'b', 3: 'c'}))
    # {1: 'a', 2: 'b', 3: 'c'}

    """
    render_keys = find_render_keys(objs, render_keys)
    render_keys = _map_render_keys(objs, render_keys)
    return render_keys


def mk_specs(objs, configs):
    """
    Make a static configs that has a one-to-one relationship with objects
    """

    render_keys = mk_render_keys(objs, configs[RENDERING_KEY])
    return dict(configs, **dict(RENDERING_KEY=render_keys))


def app_maker(
    objs: Iterable,
    config: Map = None,
    convention: Map = None,
    static_config=True,
    allow_config_excess=False,
):
    specs = mk_specs(config, convention)
    app = mk_app(objs, specs, convention)
    app.config, app.convention, app.specs = config, convention, specs
    return app


def alt_mk_render_keys(objs, render_keys, resolver: Callable):
    """Make a static render_keys that has a one-to-one relationship with objects

    # >>> find_render_keys = lambda objs, render_keys:
    # >>> dict(mk_render_keys([1, 2, 3], {1: 'a', 2: 'b', 3: 'c'}))
    # {1: 'a', 2: 'b', 3: 'c'}

    """
    render_keys = resolver(objs, render_keys)
    render_keys = _map_render_keys(objs, render_keys)
    return render_keys


from typing import TypeVar, Tuple, Iterable, Callable

Obj = TypeVar('Obj')
Output = TypeVar('Output')
Cond = Callable[[Obj], bool]
Then = Callable[[Obj], Output]
Rule = Tuple[Cond, Then]
Rules = Iterable[Rule]

# Note: We could iterate over objs or over rules. Context tells what's best.
"""
typical use is to define rules and apply to objs like so
```
from functools import partial
singular_find_render_keys = partial(mk_find_render_keys, rules=rules)  # fix rules
find_render_keys = partial(map, singular_find_render_keys)  # apply to iterable
```
"""


# -----------------------------------------------------------------------------
# Say we want to make a function like the following have a plugin architecture

# TODO: Extract routing logic (the if/elifs) and expose control to interface
def target_render_keys_func(obj, render_keys):
    if obj in render_keys:
        return OBJECT, (obj, render_keys[obj])
    elif name_of_obj(obj) in render_keys:
        return NAME_OF_OBJ, (name_of_obj(obj), render_keys[name_of_obj(obj)])
    elif (
        type_ := first_element_matching_type(
            SUBTYPE, (obj, filter(lambda x: isinstance(x, type), render_keys))
        )
    ) is not None:
        return type_, name_of_obj(type_)
    else:
        # TODO: More significant error (perhaps list ALL the objects that are not
        #  mapped and suggest what to do about it (given the specific objects and
        #  render keys).
        raise ValueError(f"Object couldn't be mapped to a render_keys key: {obj}")


# -----------------------------------------------------------------------------
# In this case we need a function that implements the if then logic in a loop...


def cond_then(obj: Obj, rules: Rules) -> Iterable[Output]:
    for cond, then in rules:
        if cond(obj):
            yield then(obj)


def mk_target_render_keys_func():
    """Will use mk_find_render_keys to make a function equivalent to
    target_render_keys_func
    """

    def _target_render_keys_func(obj, render_keys):
        rules = [
            (
                lambda obj: obj in render_keys,
                lambda obj: (OBJECT, (obj, render_keys[obj])),
            ),
            (
                lambda obj: name_of_obj(obj) in render_keys,
                lambda obj: (
                    NAME_OF_OBJ,
                    (name_of_obj(obj), render_keys[name_of_obj(obj)]),
                ),
            ),
            # TODO: Note in the following how first_element_matching_type needs to be
            #  called three times in the following rule. This is where the feature
            #  based rules can come in handy.
            (
                lambda obj: (
                    first_element_matching_type(
                        SUBTYPE,
                        (obj, filter(lambda x: isinstance(x, type), render_keys)),
                    )
                )
                is not None,
                lambda obj: (
                    first_element_matching_type(
                        SUBTYPE,
                        (obj, filter(lambda x: isinstance(x, type), render_keys)),
                    ),
                    name_of_obj(
                        first_element_matching_type(
                            SUBTYPE,
                            (obj, filter(lambda x: isinstance(x, type), render_keys)),
                        )
                    ),
                ),
            ),
        ]
        return cond_then(obj, rules)

    return _target_render_keys_func


# That las rule is pretty ugly. We can make it better by using a feature based rule
# Here are some ideas:


def if_then(cond, then, obj):
    """
    Intent is to be used with ``functools.partial``, ``map`` and ``itertools.chain``

    >>> from functools import partial
    >>> from itertools import chain
    >>> my_if_then = partial(if_then, lambda x: x % 2 == 0, lambda x: x * 2)
    >>> f = lambda x: chain.from_iterable(map(my_if_then, x))
    >>> next(f([1, 2, 3, 4]))
    4
    >>> list(f([1, 2, 3, 4]))  # get all matches
    [4, 8]

    """
    if cond(obj):
        yield then(obj)


def if_feature_then_obj(feature, cond, then, obj):
    feat = feature(obj)
    if cond(feat):
        yield then(obj)


def if_feature_then_feature(feature, cond, then, obj):
    feat = feature(obj)
    if cond(feat):
        yield then(feat)


def if_feature_then_feature_and_obj(feature, cond, then, obj):
    feat = feature(obj)
    if cond(feat):
        yield then(obj, feat)


# -----------------------------------------------------------------------------
# Now let's try a different way: The user brings both cond and rule in a function
# and we just chain them together. This is a bit more flexible than the previous
# approach, but doesn't allow us to reuse cond and then logic as much.


def rule_applier(obj, rules, render_keys, sentinel=None):
    """Applies rules to obj and returns the first non-sentinel value

    """
    for rule in rules:
        if (result := rule(obj, render_keys)) is not sentinel:
            return result


def rule1(obj, render_keys):
    if obj in render_keys:
        return OBJECT, (obj, render_keys[obj])


def rule2(obj, render_keys):
    if name_of_obj(obj) in render_keys:
        return NAME_OF_OBJ, (name_of_obj(obj), render_keys[name_of_obj(obj)])


def rule3(obj, render_keys):
    if (
        type_ := first_element_matching_type(
            SUBTYPE, (obj, filter(lambda x: isinstance(x, type), render_keys))
        )
    ) is not None:
        return type_, name_of_obj(type_)


rules = [rule1, rule2, rule3]
