import streamlit as st
from typing import Any, Mapping
from collections.abc import Callable
from front import SpecMakerBase, APP_KEY, RENDERING_KEY, ELEMENT_KEY

from streamlitfront.elements import (
    App,
    ExecSection,
    FloatInput,
    IntInput,
    TextInput,
    TextOutput,
    TextSection,
    View,
)


def get_stored_value(key: str) -> Any:
    return st.session_state[key] if key in st.session_state else None


DFLT_CONVENTION_DICT = {
    APP_KEY: {'title': 'My Streamlit Front Application'},
    RENDERING_KEY: {
        ELEMENT_KEY: App,
        Callable: {
            ELEMENT_KEY: View,
            'description': {ELEMENT_KEY: TextSection,},
            'execution': {
                ELEMENT_KEY: ExecSection,
                'stored_value_getter': get_stored_value,
                'inputs': {
                    int: {ELEMENT_KEY: IntInput,},
                    float: {ELEMENT_KEY: FloatInput,},
                    Any: {ELEMENT_KEY: TextInput,},
                },
                'output': {ELEMENT_KEY: TextOutput,},
            },
        },
    },
}

from dol.sources import AttrContainer


class SpecMaker(SpecMakerBase):
    @property
    def _dflt_convention(cls) -> Mapping:
        return DFLT_CONVENTION_DICT
