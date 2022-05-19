import streamlit as st
from front.elements import FuncViewBase, TextInputBase, IntInputBase, FloatInputBase, AppBase

from streamlitfront.session_state import get_state

# from front.elements import NumberInput

# def render_number_input(self):
#     return st.number_input

# setattr(NumberInput, 'render', )

def default_hash_func(item):
    return id(item)


class DfltDict(dict):
    def __missing__(self, k):
        return default_hash_func


# TODO: No particulars should be here. Should figure out how to inject particulars
#  when a particular app requires it. dflt_hash_funcs is for GENERAL defaults.
#  If the key is not found, will return default_hash_func anyway.
dflt_hash_funcs = DfltDict(
    {
        'abc.WfStoreWrapped': default_hash_func,
        'qcoto.dacc.Dacc': default_hash_func,
        'abc.DfSimpleStoreWrapped': default_hash_func,
        'builtins.dict': default_hash_func,
        'haggle.dacc.KaggleDatasetInfoReader': default_hash_func,
    }
)

class App(AppBase):
    def render(self):
        state = get_state(hash_funcs=dflt_hash_funcs)  # TODO: get from configs

        # Page setup
        st.set_page_config(layout='wide')

        # Make page objects
        views = {
            view.name: view.render
            for view in self.children
        }
        state['views'] = views

        # TODO: The above is static: Should the above be done only once, and cached?
        #   Perhaps views should be cached in state?

        # Setup navigation
        with st.sidebar:
            st.title(self.title)
            view_key = st.radio(options=tuple(views.keys()), label='Select your view')
        # view_key = _get_view_key(tuple(views.keys()), label='Select your view')

        # Display the selected page with the session state
        # This is the part that actually runs the functionality that pages specifies
        view_runner = views[view_key]  # gets the page runner
        view_runner(state)  # runs the page with the state

        # Mandatory to avoid rollbacks with widgets, must be called at the end of your app
        state.sync()



class FuncView(FuncViewBase):
    def render(self, state):
        st.markdown(f'''## **{self.name}**''')
        func_inputs = {}
        for child in self.children:
            func_inputs[child.param.name] = child.render()
        submit = st.button('Submit')
        if submit:
            st.write(self.func(**func_inputs))


class TextInput(TextInputBase):
    def render(self):
        return st.text_input(
            label=self.label,
            value=self.init_value,
        )


class IntInput(IntInputBase):
    def render(self):
        return st.number_input(
            label=self.label,
            value=self.init_value,
            min_value=self.min_value,
            max_value=self.max_value,
            format=self.format,
        )


class FloatInput(FloatInputBase):
    def render(self):
        return st.number_input(
            label=self.label,
            value=self.init_value,
            min_value=self.min_value,
            max_value=self.max_value,
            format=self.format,
            step=self.step,
        )


class FloatSliderInput(FloatInputBase):
    def render(self):
        return st.slider(
            label=self.label,
            value=self.init_value,
            min_value=self.min_value,
            max_value=self.max_value,
            format=self.format,
            step=self.step,
        )


# class TextOutput(FrontComponentBase):
#     def render(self):
#         pass


# class NumberOutput(FrontComponentBase):
#     def render(self):
#         pass
