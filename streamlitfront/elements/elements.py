"""Here are implemented the elements for streamlitfront.

Not the use of the ``implement_component`` function to create a class that implements a
specific abstract elements class defined in front.
"""

from dataclasses import dataclass
from functools import partial
from typing import Any, Callable, Iterable
import streamlit as st
from pydantic import ValidationError
from front.elements import (
    implement_component,
    BooleanInputBase,
    ExecContainerBase,
    FileUploaderBase,
    FloatInputBase,
    FrontContainerBase,
    InputBase,
    IntInputBase,
    KwargsInputBase,
    MultiSourceInputBase,
    OutputBase,
    SelectBoxBase,
    TextInputBase,
    TextSectionBase,
    ELEMENT_KEY,
)
from front.types import FrontElementName
from i2 import Sig
from stogui import pipeline_maker

from streamlitfront.elements.js import mk_element_factory
from streamlitfront.data_binding import BoundData


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
        views = {view.name: view for view in self.children}
        # st.session_state["views"] = views

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
    def __init__(
        self,
        obj: Callable,
        inputs: dict,
        output: dict,
        name: FrontElementName = None,
        auto_submit: bool = False,
        on_submit: Callable[[Any], None] = None,
        use_expander: bool = True,
    ):
        super().__init__(
            obj=obj,
            inputs=inputs,
            output=output,
            name=name,
            auto_submit=auto_submit,
            on_submit=on_submit,
        )
        self.use_expander = use_expander

    def render(self):
        if self.use_expander:
            with st.expander(self.name, True):
                self._render_section_content()
        else:
            self._render_section_content()

    def _render_section_content(self):
        inputs = self._render_inputs()
        if self.auto_submit or st.button('Submit'):
            try:
                self._submit(inputs)
            except ValidationError as e:
                st.error(e)

    def _noneable(self, input_instance: InputBase) -> InputBase:
        # input_render = input_instance.render
        input_render = getattr(input_instance, 'render')

        def noneable_render():
            none_value = input_instance.none_value
            input_instance.disabled = none_value
            # if none_value:
            #     input_instance.view_value = input_instance._dflt_view_value
            result = input_render()
            is_none = st.checkbox(
                label='None', key=input_instance.none_key, value=none_value
            )
            return None if is_none else result

        # input.render = noneable_render
        setattr(input_instance, 'render', noneable_render)
        return input_instance


class TextOutput(OutputBase):
    def render(self):
        st.caption(self.name)
        st.write(self.output)


class MultiSourceInput(MultiSourceInputBase):
    def render(self):
        with st.container():
            options = tuple(x.name for x in self.input_components)
            # source = st.radio(self.name, options)
            source = st.selectbox(self.name, options)
            input_component = next(x for x in self.input_components if x.name == source)
            return input_component()


# def store_input_value_in_state(input_value, component: InputBase):
#     st.session_state[component.input_key] = input_value


implement_input_component = partial(
    implement_component,
    # input_value_callback=store_input_value_in_state,
    label='name',
    key='view_key',
    value='view_value',
)

TextInput = implement_input_component(TextInputBase, st.text_input)
BooleanInput = implement_input_component(BooleanInputBase, st.checkbox)
IntInput = implement_input_component(IntInputBase, st.number_input)
IntSliderInput = implement_input_component(IntInputBase, st.slider)
FloatInput = implement_input_component(FloatInputBase, st.number_input)
FloatSliderInput = implement_input_component(FloatInputBase, st.slider)
SelectBox = implement_input_component(
    SelectBoxBase, st.selectbox, options='_options', index='_preselected_index'
)


# class SelectBox(SelectBoxBase):
#     def render(self):
#         return st.selectbox(
#             label=self.name,
#             options=self._options,
#             index=self._preselected_index,
#         )


@dataclass
class FileUploader(FileUploaderBase):
    display_label: bool = True

    def render(self):
        label_visibility = 'visible' if self.display_label else 'collapsed'
        return st.file_uploader(
            label=self.name,
            label_visibility=label_visibility,
            type=self.type,
            accept_multiple_files=self.accept_multiple_files,
        )


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


@dataclass
class SuccessNotification(OutputBase):
    message: str = 'Success!'

    def render(self):
        return st.success(self.message)


class HiddenOutput(OutputBase):
    def render(self):
        pass


@dataclass
class KwargsInput(KwargsInputBase):
    def render(self):
        exec_section = ExecSection(
            obj=self.get_kwargs,
            inputs=self.inputs,
            output={ELEMENT_KEY: HiddenOutput},
            auto_submit=True,
            on_submit=self._return_kwargs,
            use_expander=False,
        )
        exec_section()
        return self.value()


@dataclass
class PipelineMaker(InputBase):
    items: Iterable = None
    steps: Iterable = None
    serializer: Callable = None

    def render(self):
        return pipeline_maker(
            items=self.items, steps=self.steps, serializer=self.serializer,
        )
