"""An opt-in "Clear all" button resets a view's fields to their defaults
(i2mint/streamlitfront#29). Runs the app headlessly with ``AppTest``."""

import pytest

pytest.importorskip("streamlit.testing.v1")
from streamlit.testing.v1 import AppTest

APP = """
from front import RENDERING_KEY
from streamlitfront import mk_app
def greet(who: str = "world", times: int = 1):
    return (who + " ") * times
mk_app([greet], config={RENDERING_KEY: {"greet": {"execution": {"clear_button_label": "Clear all"}}}})()
"""

NO_CLEAR = APP.replace('"clear_button_label": "Clear all"', '"auto_submit": False')


def _button(at, label):
    return next((b for b in at.button if b.label == label), None)


def test_clear_all_restores_defaults():
    at = AppTest.from_string(APP, default_timeout=30).run()
    assert not at.exception
    at.text_input[0].set_value("moon").run()
    at.number_input[0].set_value(4).run()
    assert at.text_input[0].value == "moon"
    _button(at, "Clear all").click().run()
    assert not at.exception
    assert at.text_input[0].value == "world"
    assert at.number_input[0].value == 1


def test_no_clear_button_by_default():
    at = AppTest.from_string(NO_CLEAR, default_timeout=30).run()
    assert _button(at, "Clear all") is None
