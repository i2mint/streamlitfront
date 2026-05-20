"""Tests for :mod:`streamlitfront.pydantic_widgets`.

The widget functions need a Streamlit run context, so they're exercised
through ``streamlit.testing.v1.AppTest`` — a real (headless) app run. The
pure helpers are tested directly.
"""

from typing import Optional

from streamlit.testing.v1 import AppTest

from streamlitfront.pydantic_widgets import _unwrap_optional


# ----------------------------------------------------------------------------
# Pure-helper unit tests


def test_unwrap_optional():
    assert _unwrap_optional(Optional[int]) is int
    assert _unwrap_optional(int) is int
    # A non-Optional Union is left untouched.
    union = _unwrap_optional(eval("int | str"))
    assert union == eval("int | str")


# ----------------------------------------------------------------------------
# AppTest-based integration tests

_INPUT_SCRIPT = """
import streamlit as st
from pydantic import BaseModel
from streamlitfront.pydantic_widgets import pydantic_input

class Person(BaseModel):
    age: int
    name: str = "anon"
    active: bool = False

person = pydantic_input("person", Person)
if person is not None:
    st.text(f"{person.name}:{person.age}:{person.active}")
"""


def test_pydantic_input_renders_and_builds_instance():
    """Each field gets a widget; editing widgets rebuilds a validated instance."""
    at = AppTest.from_string(_INPUT_SCRIPT)
    at.run()
    assert not at.exception

    # One widget per field, of the type matching the annotation.
    assert len(at.number_input) == 1  # age: int
    assert len(at.text_input) == 1  # name: str
    assert len(at.checkbox) == 1  # active: bool

    # Defaults flow through to a valid instance immediately.
    assert at.text[0].value == "anon:0:False"

    # Edit the widgets; the instance should reflect the new values.
    at.number_input[0].set_value(42).run()
    at.text_input[0].set_value("alice").run()
    at.checkbox[0].set_value(True).run()
    assert not at.exception
    assert at.text[0].value == "alice:42:True"


_FORM_SCRIPT = """
import streamlit as st
from pydantic import BaseModel
from streamlitfront.pydantic_widgets import pydantic_form

class Coords(BaseModel):
    x: int
    y: int = 5

result = pydantic_form("coords", Coords)
st.text("submitted" if result is not None else "pending")
if result is not None:
    st.text(f"{result.x},{result.y}")
"""


def test_pydantic_form_returns_none_until_submitted():
    """The form yields None before submit, an instance after submit."""
    at = AppTest.from_string(_FORM_SCRIPT)
    at.run()
    assert not at.exception
    # Before submitting, the form returns None.
    assert at.text[0].value == "pending"

    # Fill in and submit the form.
    at.number_input[0].set_value(3)
    at.number_input[1].set_value(9)
    at.button[0].click().run()
    assert not at.exception
    assert at.text[0].value == "submitted"
    assert at.text[1].value == "3,9"


_OUTPUT_SCRIPT = """
from pydantic import BaseModel
from streamlitfront.pydantic_widgets import pydantic_output

class Result(BaseModel):
    value: int
    label: str

pydantic_output(Result(value=7, label="seven"))
"""


def test_pydantic_output_renders_instance():
    """pydantic_output renders the instance without error."""
    at = AppTest.from_string(_OUTPUT_SCRIPT)
    at.run()
    assert not at.exception
    assert len(at.json) == 1
