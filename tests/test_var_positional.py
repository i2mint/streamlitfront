"""A ``*args`` parameter gets a "+" button: one more field per press, and the
function is called with what was entered (i2mint/streamlitfront#28)."""

import pytest

pytest.importorskip("streamlit.testing.v1")
from streamlit.testing.v1 import AppTest

APP = """
from streamlitfront import mk_app
def add_nums(*nums_to_add: int):
    return sum(nums_to_add)
def tag(prefix: str, *names: str):
    return prefix + ",".join(names)
mk_app([add_nums, tag])()
"""


def _plus(at):
    return next(b for b in at.button if b.key and b.key.endswith("_plus"))


def _minus(at):
    return next(b for b in at.button if b.key and b.key.endswith("_minus"))


def test_plus_adds_a_field_per_press_and_submit_calls_the_function():
    at = AppTest.from_string(APP, default_timeout=30).run()
    assert not at.exception
    assert len(at.number_input) == 0
    for _ in range(3):
        _plus(at).click().run()
    assert len(at.number_input) == 3
    for field, v in zip(at.number_input, (1, 2, 3)):
        field.set_value(v)
    at.run()
    _minus(at).click().run()
    assert len(at.number_input) == 2
    next(b for b in at.button if b.label == "Submit").click().run()
    assert not at.exception
    assert any(m.value == "`3`" for m in at.markdown)


def test_no_press_means_no_extra_arguments():
    at = AppTest.from_string(APP, default_timeout=30).run()
    next(b for b in at.button if b.label == "Submit").click().run()
    assert not at.exception
