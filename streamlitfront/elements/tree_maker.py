from typing import Any, Mapping
from front.elements import (
    ElementTreeMakerBase,
    FrontElementBase,
)
from front.elements import *
import streamlit as st

from streamlitfront.elements import *

MY_COMPONENT = 'MY_COMPONENT'


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
            EXEC_SECTION_CONTAINER: ExecSection,
            MULTI_SOURCE_INPUT_CONTAINER: MultiSourceInputContainer,
            TEXT_INPUT_COMPONENT: TextInput,
            INT_INPUT_COMPONENT: IntInput,
            INT_INPUT_SLIDER_COMPONENT: IntSliderInput,
            FLOAT_INPUT_COMPONENT: FloatInput,
            FLOAT_INPUT_SLIDER_COMPONENT: FloatSliderInput,
            FILE_UPLOADER_COMPONENT: FileUploader,
            AUDIO_RECORDER_COMPONENT: AudioRecorder,
        }

    def _get_stored_value(cls, key: str) -> Any:
        return st.session_state[key] if key in st.session_state else None
