import streamlit as st
from dataclasses import dataclass
from front.elements import InputBase
from front.types import Map
from front.util import normalize_map
from streamlitfront.elements.js import mk_element_factory
from collections.abc import Callable
from front import APP_KEY, RENDERING_KEY, ELEMENT_KEY
from streamlitfront.base import mk_app


def dummy(my_dict):
    return my_dict


@dataclass
class NestedSelect(InputBase):
    options: Map = None
    # item_template: ItemTemplate = None

    def __post_init__(self):
        super().__post_init__()
        self.options = normalize_map(self.options)
        # self.item_template = normalize_map(self.item_template)
        # if isinstance(self.item_template, Path):
        #     with self.item_template.open() as f:
        #         self.item_template = f.read()

    def render(self):
        # st_multiselect = mk_element_factory("st_multiselect")
        # level_1 = st_multiselect(options=self.options)
        # value = st_multiselect(options=self.options[level_1])
        # return value
        with st.form('first_form2'):
            level_1 = st.selectbox(label='l1', options=self.options)
            change = st.form_submit_button('Select')
            level_2 = st.selectbox(label='l2', options=self.options[level_1])
            submit = st.form_submit_button('Submit')
            value = self.options[level_1][level_2]
            return value


if __name__ == '__main__':
    app = mk_app(
        [dummy],
        config={
            APP_KEY: {'title': 'Nested Chooser'},
            RENDERING_KEY: {
                Callable: {
                    'execution': {
                        'inputs': {
                            'my_dict': {
                                ELEMENT_KEY: NestedSelect,
                                'options': {
                                    'level_0_a': {'level_1_a': 'aa', 'level_2': 'bb'},
                                    'level_0_b': {'level_1_b': 'cc', 'level_2': 'dd'},
                                },
                            }
                        }
                    }
                }
            },
        },
    )
    app()
