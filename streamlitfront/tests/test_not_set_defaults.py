"""``i2``'s ``NotSet`` sentinel in a signature means "required / no default".

See i2mint/i2#48: once ``i2.FuncFactory`` shows ``NotSet`` defaults, widgets must not
be prefilled with the sentinel, nor typed after it. These tests use
``i2.deco.NotSet`` directly, so they pass with any i2 version.
"""

from i2 import Sig
from i2.deco import NotSet

from streamlitfront import base, page_funcs


def foo(a: int, b, c: str = "hi", d=2):
    return a, b, c, d


# ``foo`` with ``NotSet`` defaults, as a re-landed i2#88 ``FuncFactory`` would show.
# Defined separately since ``Sig.__call__`` sets ``__signature__`` in place.
def foo_with_not_set(a: int = NotSet, b=NotSet, c: str = "hi", d=2):
    return a, b, c, d


def test_infer_type_ignores_not_set():
    for name in "abcd":
        assert base.infer_type(Sig(foo_with_not_set), name) is base.infer_type(
            Sig(foo), name
        )


def test_func_args_specs_are_not_prefilled_with_not_set():
    for get_specs in (
        base.get_func_args_specs,
        page_funcs.get_func_args_specs,
        page_funcs.special_get_func_args_specs,
    ):
        assert get_specs(foo_with_not_set) == get_specs(foo)
        _, factory_kwargs = get_specs(foo_with_not_set)["a"]["element_factory"]
        assert "value" not in factory_kwargs
