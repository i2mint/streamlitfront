"""Tools made with streamlitfront"""

from typing import Iterable, Tuple, KT, VT
from streamlitfront.base import mk_app, Map
from front import RENDERING_KEY

from i2 import name_of_obj

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


def _find_val(val, render_keys: dict):
    """Make a static configs that has a one to one relationship with objects"""
    # TODO: raise specific error with more info instead of assert:
    assert set(objs) == set(objs), f"Some of your objects weren't unique"

    for obj in objs:
        if obj in render_keys:
            yield OBJECT, (obj, render_keys[obj])
        elif name_of_obj(obj) in render_keys:
            yield NAME_OF_OBJ, (name_of_obj(obj), render_keys[name_of_obj(obj)])
        elif (
            type_ := first_element_matching_type(
                SUBTYPE, (obj, filter(lambda x: isinstance(x, type), render_keys))
            )
        ) is not None:
            yield type_, name_of_obj(type_)
        else:
            # TODO: More significant error (perhaps list ALL the objects that are not
            #  mapped and suggest what to do about it (given the specific objects and
            #  render keys).
            raise ValueError(f"Object couldn't be mapped to a render_keys key: {obj}")


# TODO: Extract routing logic (the if/elifs) and expose control to interface
def _find_render_keys(objs, render_keys: dict):
    """Make a static configs that has a one to one relationship with objects"""
    # TODO: raise specific error with more info instead of assert:
    assert set(objs) == set(objs), f"Some of your objects weren't unique"

    for obj in objs:
        if obj in render_keys:
            yield OBJECT, (obj, render_keys[obj])
        elif name_of_obj(obj) in render_keys:
            yield NAME_OF_OBJ, (name_of_obj(obj), render_keys[name_of_obj(obj)])
        elif (
            type_ := first_element_matching_type(
                SUBTYPE, (obj, filter(lambda x: isinstance(x, type), render_keys))
            )
        ) is not None:
            yield type_, name_of_obj(type_)
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


def mk_specs(objs, configs, convention):
    # configs = merge(configs, convention)  # is it simply a (deep) ChainMap?
    render_keys = _find_render_keys(objs, configs[RENDERING_KEY])
    render_keys = _map_render_keys(objs, render_keys)
    return dict(configs, **dict(RENDERING_KEY=render_keys))


def app_maker(
    objs: Iterable,
    config: Map = None,
    convention: Map = None,
    static_config=True,
    allow_config_excess=False,
):
    specs = mk_specs(config, convention)
    return mk_app(objs, specs, convention)
