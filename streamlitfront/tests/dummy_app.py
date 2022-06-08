from streamlitfront.base import get_pages_specs, get_func_args_specs, BasePageFunc
import streamlit as st
from pydantic import BaseModel
import streamlit_pydantic as sp


def multiple(x: int, word: str) -> str:
    return str(x) + word


class Input(BaseModel):
    x: int
    y: str


def multiple_input(input: Input):
    return input.x * input.y


class SimplePageFunc2(BasePageFunc):
    def __call__(self, state):
        self.prepare_view(state)
        # args_specs = get_func_args_specs(self.func)
        element = sp.pydantic_input('input', Input)
        st.write(element)
        # func_inputs = dict(self.sig.defaults, **state['page_state'][self.func])
        func_inputs = {'input': element}
        st.write(func_inputs)
        # for argname, spec in args_specs.items():
        # st.write(f"argname:{argname}")
        # st.write(f"spec:{spec}")
        # element_factory, kwargs = spec["element_factory"]
        # func_inputs[argname] = element_factory(**kwargs)
        # st.write(f"element_factory:{element_factory}")
        # st.write(f"kwargs:{kwargs}")

        submit = st.button('Submit')
        if submit:
            st.write(self.func(func_inputs['input']))
            # state['page_state'][self.func].clear()


DFLT_PAGE_FACTORY = SimplePageFunc2


if __name__ == '__main__':
    app = get_pages_specs([multiple_input], page_factory=DFLT_PAGE_FACTORY)
    app['Multiple Input'](None)
