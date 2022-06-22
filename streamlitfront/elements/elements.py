"""Here are implemented the elements for streamlitfront.

Not the use of the ``implement_component`` function to create a class that implements a
specific abstract elements class defined in front.
"""

from functools import partial
from numpy import isin
import streamlit as st
from front.elements import (
    DagContainerBase,
    InputBase,
    TextInputBase,
    IntInputBase,
    FloatInputBase,
    NamedContainerBase,
    GraphBase,
    implement_component,
)

# from streamlitfront.session_state import get_state


class App(NamedContainerBase):
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


class View(NamedContainerBase):
    def render(self):
        st.markdown(f'''## **{self.name}**''')
        self._render_children()


class Section(NamedContainerBase):
    def render(self):
        with st.expander(self.name, True):
            self._render_children()


class DagExecSection(DagContainerBase):
    def render(self):
        with st.expander(self.name, True):
            inputs = {}
            for child in self.children:
                inputs[child.label] = child.render()
            submit = st.button('Submit')
            # output_key = f'{self.dag.__name__}_output'
            if submit:
                # state = get_state_with_hash_funcs()
                output = self.dag(**inputs)
                st.session_state[f'{self.dag.__name__}_output'] = output
                st.write(output)


def store_input_value_in_state(input_value, component: InputBase):
    st.session_state[component.input_key] = input_value


implement_component_with_input_value_callback = partial(
    implement_component, input_value_callback=store_input_value_in_state
)
implement_component_with_init_value = partial(
    implement_component_with_input_value_callback, value='init_value'
)
implement_float_input_component = partial(
    implement_component_with_init_value, base_cls=FloatInputBase
)

TextInput = implement_component_with_init_value(TextInputBase, st.text_input)
# TextOutput = implement_component(TextOutputBase, st.write)
IntInput = implement_component_with_init_value(IntInputBase, st.number_input)
IntSliderInput = implement_component_with_init_value(IntInputBase, st.slider)
FloatInput = implement_float_input_component(component_factory=st.number_input)
FloatSliderInput = implement_float_input_component(component_factory=st.slider)
Graph = implement_component(GraphBase, st.graphviz_chart)
