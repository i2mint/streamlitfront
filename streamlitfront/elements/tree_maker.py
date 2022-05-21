from typing import Any, Mapping
from front.elements import ElementTreeMakerBase, FrontElementBase, ContainerFlag, InputComponentFlag
import streamlit as st

from streamlitfront.elements.elements import App, FloatInput, FloatSliderInput, IntInput, TextInput, FuncView
from streamlitfront.session_state import get_state


class ElementTreeMaker(ElementTreeMakerBase):
    @property
    def _component_mapping(cls) -> Mapping[InputComponentFlag, FrontElementBase]:
        return {
            InputComponentFlag.TEXT: TextInput,
            InputComponentFlag.INT: IntInput,
            InputComponentFlag.FLOAT: FloatInput,
            InputComponentFlag.FLOAT_SLIDER: FloatSliderInput,
        }

    @property
    def _container_mapping(cls) -> Mapping[ContainerFlag, FrontElementBase]:
        return {
            ContainerFlag.APP: App,
            ContainerFlag.VIEW: FuncView,
        }

    def _get_stored_value(cls, key: str) -> Any:
        return st.session_state[key] if key in st.session_state else None
