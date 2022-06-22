from typing import Any, Mapping
from front.elements import (
    ElementTreeMakerBase,
    FrontElementBase,
    APP_CONTAINER,
    VIEW_CONTAINER,
    SECTION_CONTAINER,
    EXEC_SECTION_CONTAINER,
    TEXT_INPUT_COMPONENT,
    INT_INPUT_COMPONENT,
    INT_INPUT_SLIDER_COMPONENT,
    FLOAT_INPUT_COMPONENT,
    FLOAT_INPUT_SLIDER_COMPONENT,
    GRAPH_COMPONENT
)
import streamlit as st

from streamlitfront.elements.elements import (
    App,
    DagExecSection,
    FloatInput,
    FloatSliderInput,
    IntInput,
    IntSliderInput,
    Section,
    TextInput,
    View,
    Graph
)


class ElementTreeMaker(ElementTreeMakerBase):
    """Tree maker class for streamlitfront. Defines the streamlitfront-speceific
    element mapping and state management.
    """

    @property
    def _element_mapping(cls) -> Mapping[int, FrontElementBase]:
        return {
            APP_CONTAINER: App,
            VIEW_CONTAINER: View,
            SECTION_CONTAINER: Section,
            EXEC_SECTION_CONTAINER: DagExecSection,
            TEXT_INPUT_COMPONENT: TextInput,
            # TEXT_OUTPUT_COMPONENT: TextOutput,
            INT_INPUT_COMPONENT: IntInput,
            INT_INPUT_SLIDER_COMPONENT: IntSliderInput,
            FLOAT_INPUT_COMPONENT: FloatInput,
            FLOAT_INPUT_SLIDER_COMPONENT: FloatSliderInput,
            GRAPH_COMPONENT: Graph,
        }

    def _get_stored_value(cls, key: str) -> Any:
        return st.session_state[key] if key in st.session_state else None
