"""``on_value_change`` runs as the widget's callback, i.e. *before* the rerun it triggers, so a
dependent input built eagerly from the bound value is updated by a single interaction
(i2mint/streamlitfront#7: the user had to select twice). Runs the app headlessly with ``AppTest``.
"""

import copy

import pytest

pytest.importorskip("streamlit.testing.v1")
from streamlit.testing.v1 import AppTest

from streamlitfront import spec_maker


@pytest.fixture(autouse=True)
def _isolate_default_convention():
    """Building an app writes its inputs into the shared default convention (i2mint/front#39)."""
    saved = copy.deepcopy(spec_maker.DFLT_CONVENTION_DICT)
    yield
    spec_maker.DFLT_CONVENTION_DICT.clear()
    spec_maker.DFLT_CONVENTION_DICT.update(saved)


APP = """
import streamlit as st
from front import APP_KEY, RENDERING_KEY, ELEMENT_KEY
from front.data_binding import ValueNotSet
from streamlitfront import mk_app, binder as b
from streamlitfront.elements import SelectBox, TextInput

data = {"A": ["a1", "a2"], "B": ["b1", "b2", "b3"]}

def pick(band: str, member: str):
    return member

def on_select_band(band):
    b.members.set(data[band])

if b.members() is ValueNotSet:
    b.selected_band.set("A")
    b.members.set(data["A"])

mk_app(
    [pick],
    config={
        APP_KEY: {"title": "t"},
        RENDERING_KEY: {
            "pick": {
                "execution": {
                    "inputs": {
                        "band": {
                            ELEMENT_KEY: SelectBox,
                            "options": list(data),
                            "value": b.selected_band,
                            "on_value_change": on_select_band,
                        },
                        # NB: called now, i.e. read when the config is built, before any render
                        "member": {ELEMENT_KEY: SelectBox, "options": b.members()},
                    }
                }
            }
        },
    },
)()
"""


def _selects(at):
    return {s.label: s for s in at.selectbox}


def test_one_selection_updates_a_dependent_input():
    at = AppTest.from_string(APP, default_timeout=30).run()
    assert not at.exception
    assert list(_selects(at)["Member"].options) == ["a1", "a2"]

    _selects(at)["Band"].select("B").run()

    assert not at.exception
    assert _selects(at)["Band"].value == "B"
    assert list(_selects(at)["Member"].options) == ["b1", "b2", "b3"]


MULTI_APP = """
from front import APP_KEY, RENDERING_KEY, ELEMENT_KEY
from streamlitfront import mk_app, binder as b
from streamlitfront.elements import MultiSelectBox

def pick(members: list):
    return members

def on_pick(values):
    b.picked.set(values)

mk_app(
    [pick],
    config={
        APP_KEY: {"title": "t"},
        RENDERING_KEY: {"pick": {"execution": {"inputs": {"members": {
            ELEMENT_KEY: MultiSelectBox,
            "options": ["m1", "m2", "m3"],
            "on_value_change": on_pick,
        }}}}},
    },
)()
"""


def test_multiselect_on_value_change_receives_the_selected_list():
    at = AppTest.from_string(MULTI_APP, default_timeout=30).run()
    assert not at.exception
    at.multiselect[0].select("m2").run()
    assert not at.exception
    selected = list(at.multiselect[0].value)
    assert "m2" in selected
    assert at.session_state["picked"] == selected
    at.run()  # a plain rerun must not replace it with a single option
    assert at.session_state["picked"] == selected
