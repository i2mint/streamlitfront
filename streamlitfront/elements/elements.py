"""Here are implemented the elements for streamlitfront.

Not the use of the ``implement_component`` function to create a class that implements a
specific abstract elements class defined in front.
"""

from functools import partial
import os
from typing import Any
import streamlit as st
import streamlit.components.v1 as components
from front.elements import (
    implement_component,
    ExecContainerBase,
    FileUploaderBase,
    FloatInputBase,
    FrontContainerBase,
    InputBase,
    IntInputBase,
    MultiSourceInputContainerBase,
    OutputBase,
    TextInputBase,
    TextSectionBase,
)
from front.util import get_value


class App(FrontContainerBase):
    """Implementation of the app root container for streamlitfront."""

    def render(self):
        # Page setup
        st.set_page_config(layout='wide')

        # Make page objects
        views = {view.name: view.render for view in self.children}
        st.session_state['views'] = views

        # TODO: The above is static: Should the above be done only once, and cached?
        #   Perhaps views should be cached in state?

        # Setup navigation
        with st.sidebar:
            st.title(self.name)
            view_key = st.radio(options=tuple(views.keys()), label='Select your view')
        # view_key = _get_view_key(tuple(views.keys()), label='Select your view')

        # Display the selected page with the session state
        # This is the part that actually runs the functionality that pages specifies
        view_runner = views[view_key]  # gets the page runner
        view_runner()  # runs the page with the state


class View(FrontContainerBase):
    def render(self):
        st.markdown(f'''## **{self.name}**''')
        self._render_children()


class Section(FrontContainerBase):
    def render(self):
        with st.expander(self.name, True):
            self._render_children()


class TextSection(TextSectionBase):
    def __init__(
        self, content: str, kind: str = 'text', obj: Any = None, name=None, **kwargs
    ):
        super().__init__(content, kind, obj, name, **kwargs)
        self.kind = self.kind if self.kind in ['markdown', 'code', 'latex'] else 'text'

    # def __post_init__(self):
    #     super().__post_init__()
    #     self.kind = self.kind if self.kind in ['markdown', 'code', 'latex'] else 'text'

    def render(self):
        with st.expander(self.name, True):

            if self.kind == 'code':
                st_element_factory = st.code
            getattr(st, self.kind)(self.content, **self.kwargs)


class ExecSection(ExecContainerBase):
    def render(self):
        with st.expander(self.name, True):
            inputs = {}
            for input_component in self.input_components:
                inputs[input_component.obj.name] = input_component.render()
            submit = st.button('Submit')
            # output_key = f'{self.dag.__name__}_output'
            if submit:
                # state = get_state_with_hash_funcs()
                output = self.obj(**inputs)
                st.session_state[f'{self.obj.__name__}_output'] = output
                self.output_component.render_output(output)


class TextOutput(OutputBase):
    def render(self):
        st.caption(self.name)
        st.write(self.output)


class MultiSourceInputContainer(MultiSourceInputContainerBase):
    def render(self):
        with st.container():
            options = tuple(x.name for x in self.children)
            # source = st.radio(self.name, options)
            source = st.selectbox(self.name, options)
            input_component = next(x for x in self.children if x.name == source)
            return input_component.render()


def store_input_value_in_state(input_value, component: InputBase):
    st.session_state[component.input_key] = input_value


implement_input_component = partial(
    implement_component,
    input_value_callback=store_input_value_in_state,
    label='name',
    value='init_value',
)
implement_float_input_component = partial(
    implement_input_component, base_cls=FloatInputBase
)

TextInput = implement_input_component(TextInputBase, st.text_input)
# TextOutput = implement_component(OutputBase, st.write)
IntInput = implement_input_component(IntInputBase, st.number_input)
IntSliderInput = implement_input_component(IntInputBase, st.slider)
FloatInput = implement_float_input_component(component_factory=st.number_input)
FloatSliderInput = implement_float_input_component(component_factory=st.slider)
FileUploader = implement_input_component(FileUploaderBase, st.file_uploader)


class AudioRecorder(InputBase):
    def render(self):
        # # Design move app further up and remove top padding
        # st.markdown('''<style>.css-1egvi7u {margin-top: -3rem;}</style>''',
        #     unsafe_allow_html=True)
        # # Design change st.Audio to fixed height of 45 pixels
        # st.markdown('''<style>.stAudio {height: 45px;}</style>''',
        #     unsafe_allow_html=True)
        # # Design change hyperlink href link color
        # st.markdown('''<style>.css-v37k9u a {color: #ff4c4b;}</style>''',
        #     unsafe_allow_html=True)  # darkmode
        # st.markdown('''<style>.css-nlntq9 a {color: #ff4c4b;}</style>''',
        #     unsafe_allow_html=True)  # lightmode
        # st.caption(self.name)

        # save_name = st.text_input(self.name, self.name)
        # save_name = save_name or self.name
        # if st.checkbox(f'Show audio recorder', True):

        parent_dir = os.path.dirname(os.path.abspath(__file__))
        build_dir = os.path.join(parent_dir, 'js', 'st_audiorec')
        st_audiorec = components.declare_component('st_audiorec', path=build_dir)
        audio_data_url = st_audiorec()
        # if audio_data_url:
        #     st.success(f'The audio has been successfully saved under "{save_name}"')
        return audio_data_url
