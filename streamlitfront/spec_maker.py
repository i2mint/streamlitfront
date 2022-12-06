from front.spec_maker_base import BASE_DFLT_CONVENTION
from front.util import deep_merge
import streamlit as st
from typing import Any, Literal, Mapping
from collections.abc import Callable
from front import SpecMakerBase, APP_KEY, RENDERING_KEY, ELEMENT_KEY, DEFAULT_INPUT_KEY

from streamlitfront.elements import (
    App,
    BooleanInput,
    ExecSection,
    FloatInput,
    IntInput,
    KwargsInput,
    SelectBox,
    TextInput,
    TextOutput,
    TextSection,
    View,
)
from streamlitfront.data_binding import BoundData


DFLT_CONVENTION_DICT = deep_merge(
    BASE_DFLT_CONVENTION,
    {
        APP_KEY: {'title': 'My Streamlit Front Application'},
        RENDERING_KEY: {
            ELEMENT_KEY: App,
            Callable: {
                ELEMENT_KEY: View,
                'description': {ELEMENT_KEY: TextSection,},
                'execution': {
                    ELEMENT_KEY: ExecSection,
                    'inputs': {
                        bool: {ELEMENT_KEY: BooleanInput,},
                        int: {ELEMENT_KEY: IntInput,},
                        float: {ELEMENT_KEY: FloatInput,},
                        Literal: {ELEMENT_KEY: SelectBox,},
                        'kwargs': {ELEMENT_KEY: KwargsInput,},
                        Any: {ELEMENT_KEY: TextInput,},
                        DEFAULT_INPUT_KEY: {'bound_data_factory': BoundData},
                    },
                    'output': {ELEMENT_KEY: TextOutput,},
                },
            },
        },
    },
)


class SpecMaker(SpecMakerBase):
    """Concrete implementation of front.spec_maker_base.SpecMakerBase for
    streamlitfront.

    >>> spec_maker = SpecMaker()
    >>> spec = spec_maker.mk_spec({})
    >>>
    >>> spec.app_spec
    {'title': 'My Streamlit Front Application'}
    >>> assert spec.obj_spec
    >>> assert spec.rendering_spec
    """

    @property
    def _dflt_convention(cls) -> Mapping:
        return DFLT_CONVENTION_DICT
