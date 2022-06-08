from typing import Any, Mapping
from front.elements import (
    ElementTreeMakerBase,
    FrontElementBase,
    CONTAINER_APP,
    CONTAINER_VIEW,
    COMPONENT_TEXT,
    COMPONENT_INT,
    COMPONENT_INT_SLIDER,
    COMPONENT_FLOAT,
    COMPONENT_FLOAT_SLIDER,
)
import streamlit as st

from streamlitfront.elements.elements import (
    App,
    FloatInput,
    FloatSliderInput,
    IntInput,
    IntSliderInput,
    TextInput,
    FuncView,
)


class ElementTreeMaker(ElementTreeMakerBase):
    """Tree maker class for streamlitfront. Defines the streamlitfront-speceific
    element mapping and state management.
    """

    @property
    def _element_mapping(cls) -> Mapping[int, FrontElementBase]:
        return {
            CONTAINER_APP: App,
            CONTAINER_VIEW: FuncView,
            COMPONENT_TEXT: TextInput,
            COMPONENT_INT: IntInput,
            COMPONENT_INT_SLIDER: IntSliderInput,
            COMPONENT_FLOAT: FloatInput,
            COMPONENT_FLOAT_SLIDER: FloatSliderInput,
        }

    def _get_stored_value(cls, key: str) -> Any:
        return st.session_state[key] if key in st.session_state else None
