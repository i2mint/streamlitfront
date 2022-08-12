"""Here are implemented the elements for streamlitfront.

Not the use of the ``implement_component`` function to create a class that implements a
specific abstract elements class defined in front.
"""

from dataclasses import dataclass
from functools import partial
from typing import Any, Iterable
from i2.signatures import Sig, call_forgivingly
import streamlit as st
from streamlit.components.v1 import html
from pydantic import ValidationError
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
    SelectBoxBase,
    TextInputBase,
    TextSectionBase,
)

from streamlitfront.elements.js import mk_element_factory
from streamlitfront.types import BoundData


class App(FrontContainerBase):
    """Implementation of the app root container for streamlitfront."""

    def render(self):
        # Page setup
        st.set_page_config(layout='wide')
        # html('''
        #     <script type="text/javascript">
        #         function iframeLoaded() {
        #             var iframes = document.querySelectorAll('iframe');
        #             for (const iframe of iframes) {
        #                 iframe.height = "";
        #                 iframe.height = iframe.contentWindow.document.body.scrollHeight + "px";
        #             }
        #         }
        #     </script>
        # ''')

        # Make page objects
        views = {view.name: view.render for view in self.children}
        st.session_state['views'] = views

        # TODO: The above is static: Should the above be done only once, and cached?
        #   Perhaps views should be cached in state?

        # Setup navigation
        with st.sidebar:
            st.title(self.name)
            view_key = st.radio(options=tuple(views.keys()), label='Select a view')

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
        if self.content:
            with st.expander(self.name, True):
                getattr(st, self.kind)(self.content, **self.kwargs)


class ExecSection(ExecContainerBase):
    def render(self):
        with st.expander(self.name, True):
            inputs = self._render_inputs()
            if self.auto_submit or st.button('Submit'):
                try:
                    self._submit(inputs)
                except ValidationError as e:
                    st.error(e)


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

TextInput = implement_input_component(TextInputBase, st.text_input)
IntInput = implement_input_component(IntInputBase, st.number_input)
IntSliderInput = implement_input_component(IntInputBase, st.slider)
FloatInput = implement_input_component(FloatInputBase, st.number_input)
FloatSliderInput = implement_input_component(FloatInputBase, st.slider)
# SelectBox = implement_input_component(SelectBoxBase, st.selectbox)


class SelectBox(SelectBoxBase):
    def render(self):
        options = list(getattr(self.options, 'value', self.options))
        preselected_index = (
            options.index(self.value.value)
            if self.value and self.value.value in options
            else 0
        )
        value = st.selectbox(label=self.name, options=options, index=preselected_index)
        # if self.value:
        #     self.value.value = value
        if self.on_value_change:
            call_forgivingly(self.on_value_change, value)
        return value


@dataclass
class FileUploader(FileUploaderBase):
    display_label: bool = True

    def render(self):
        label = self.name if self.display_label else ''
        return st.file_uploader(label=label, type=self.type)


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

        st_audiorec = mk_element_factory('st_audiorec')
        audio_data = st_audiorec()
        # print(audio_data)
        # audio_data = bytes(audio_data, 'utf-8') if audio_data else None
        # st.audio(audio_data)
        return audio_data
