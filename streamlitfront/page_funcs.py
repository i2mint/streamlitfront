"""
Functions to create pages
"""

import streamlit as st
from i2 import Sig
from typing import Mapping

from streamlitfront.base import (
    BasePageFunc,
    _get_dflt_element_factory_for_annot,
)
from streamlitfront.util import build_factory, Command, NodeGetter


# TODO: Extract the page setup (view_title, etc.) and make it injectable.

{int: st.number_input, float: st.number_input, str: st.text_input, bool: st.checkbox}


def get_func_elements_commands(
    func,
    state=None,
    dflt_element_factory=st.text_input,
    element_factory_for_annot: Mapping = None,
    **configs,
):
    state = state or {}
    element_factory_for_annot = (
        element_factory_for_annot or _get_dflt_element_factory_for_annot()
    )
    sig = Sig(func)
    NodeGetter(state['views'])

    func_args_specs = {name: {} for name in sig.names}
    for name in sig.names:
        # d = func_args_specs[name]
        inferred_type = infer_type(sig, name)
        form_element = _get_dflt_element_factory_for_annot(inferred_type)

        element_factory, factory_kwargs = build_element_factory(
            name,
            inferred_type,
            element_factory_for_annot,
            missing,
            dflt_element_factory,
        )

        if name in sig.defaults:
            dflt = sig.defaults[name]
            if dflt is not None:
                # TODO: type-to-element conditions must be in configs
                if isinstance(dflt, (list, tuple, set)):
                    factory_kwargs['options'] = dflt
                else:
                    factory_kwargs['value'] = dflt

        yield name, Command(element_factory, **factory_kwargs)


def get_func_args_specs(
    func,
    dflt_element_factory=st.text_input,
    element_factory_for_annot: Mapping = None,
    **configs,
):
    element_factory_for_annot = (
        element_factory_for_annot or _get_dflt_element_factory_for_annot()
    )
    sig = Sig(func)
    func_args_specs = {name: {} for name in sig.names}
    for name in sig.names:
        d = func_args_specs[name]
        inferred_type = infer_type(sig, name)
        element_factory, factory_kwargs = build_element_factory(
            name,
            inferred_type,
            element_factory_for_annot,
            missing,
            dflt_element_factory,
        )
        if name in sig.defaults:
            dflt = sig.defaults[name]
            if dflt is not None:
                # TODO: type-to-element conditions must be in configs
                if isinstance(dflt, (list, tuple, set)):
                    factory_kwargs['options'] = dflt
                else:
                    factory_kwargs['value'] = dflt

        d['element_factory'] = (element_factory, factory_kwargs)

    return func_args_specs


class ExperimentalViewFunc(BasePageFunc):
    def __call__(self, state):
        self.prepare_view(state)
        # input_view_commands = mk_input_view_commands(self.func)
        # view = NodeGetter(state['views'])
        commands = get_func_elements_commands(self.func)

        func_inputs = {}
        for argname, command in commands:
            func_inputs[argname] = command()

        submit = st.button('Submit')
        if submit:
            st.write(self.func(**func_inputs))


from streamlitfront.base import (
    infer_type,
    build_element_factory,
    _get_dflt_element_factory_for_annot,
    missing,
)


def special_get_func_args_specs(
    func,
    dflt_element_factory=st.text_input,
    element_factory_for_annot: Mapping = None,
    **configs,
):
    element_factory_for_annot = (
        element_factory_for_annot or _get_dflt_element_factory_for_annot()
    )
    sig = Sig(func)
    func_args_specs = {name: {} for name in sig.names}
    for name in sig.names:
        d = func_args_specs[name]
        inferred_type = infer_type(sig, name)
        element_factory, factory_kwargs = build_element_factory(
            name,
            inferred_type,
            element_factory_for_annot,
            missing,
            dflt_element_factory,
        )
        if name in sig.defaults:
            dflt = sig.defaults[name]
            if dflt is not None:
                # TODO: type-to-element conditions must be in configs
                if isinstance(dflt, (list, tuple, set)):
                    factory_kwargs['options'] = dflt
                else:
                    factory_kwargs['value'] = dflt

        d['element_factory'] = (element_factory, factory_kwargs)

    return func_args_specs


class DataAccessPageFunc(BasePageFunc):
    def prepare_view(self, state):
        if self.view_title:
            st.markdown(f'''## **{self.view_title}**''')
        st.write(
            'Current value stored in state for this function is:',
            state[self.view_title],
        )

    def __call__(self, state):
        self.prepare_view(state)
        args_specs = get_func_args_specs(self.func)
        func_inputs = {}
        for argname, spec in args_specs.items():
            if spec['element_factory'][0] is None:
                func_inputs[argname] = state
            else:
                if 'options' in spec['element_factory'][1]:
                    pass  # TODO: find some way to access the data from another input we want
                element_factory, kwargs = spec['element_factory']
                func_inputs[argname] = element_factory(**kwargs)
        submit = st.button('Submit')
        if submit:
            state[self.view_title] = self.func(**func_inputs)
            st.write(state[self.view_title])


class DataBindingExploPageFunc(DataAccessPageFunc):
    def __call__(self, state):
        self.prepare_view(state)
        args_specs = get_func_args_specs(self.func)
        int_args = dict(zip(range(len(args_specs)), args_specs))
        func_inputs = {}
        for idx, argname in int_args.items():
            # only works under the assumptions that the first argument for every function will be to pass the state
            # and the options for the selectbox are the argument directly before it is a string of comma separated
            # values
            if idx == 0:
                func_inputs[argname] = state
            else:
                if func_inputs[int_args[idx - 1]]:
                    if args_specs[argname]['element_factory'][0] is None:
                        func_inputs[argname] = state
                    else:
                        if 'options' in args_specs[argname]['element_factory'][1]:
                            options = func_inputs[int_args[idx - 1]].split(', ')
                            args_specs[argname]['element_factory'][1][
                                'options'
                            ] = options
                        element_factory, kwargs = args_specs[argname]['element_factory']
                        func_inputs[argname] = element_factory(**kwargs)
        submit = st.button('Submit')
        if submit:
            state[self.view_title] = self.func(**func_inputs)
            st.write(
                'New value stored in state for this function is:',
                state[self.view_title],
            )


class ArgsPageFunc(BasePageFunc):
    def __call__(self, state):
        self.prepare_view(state)
        args_specs = get_func_args_specs(self.func)
        # func_inputs = dict(self.sig.defaults, **state['page_state'][self.func])
        positional_inputs = []
        keyword_inputs = {}
        for argname, spec in args_specs.items():
            element_factory, kwargs = spec['element_factory']
            if isinstance(element_factory, dict):
                args = element_factory['base'](**kwargs)
                if args:
                    for idx in range(args):
                        if len(element_factory) == 3:
                            positional_inputs.append(
                                build_factory(element_factory, 'input', idx)
                            )
                        else:
                            key = build_factory(element_factory, 'key', idx)
                            value = build_factory(element_factory, 'value', idx)
                            keyword_inputs[key] = value
            else:
                keyword_inputs[argname] = element_factory(**kwargs)
        submit = st.button('Submit')
        if submit:
            st.write(
                f'positional inputs are {positional_inputs} and keyword inputs are {keyword_inputs}'
            )
            # state[self.view_title] = self.func(*positional_inputs, **keyword_inputs)
            # st.write(state[self.view_title])
            # state['page_state'][self.func].clear()


class StatePageFunc(BasePageFunc):
    def __call__(self, state):
        if self.view_title:
            st.markdown(f'''## **{self.view_title}**''')
        st.write(
            'Current value stored in state for this function is:',
            state[self.view_title],
        )
        args_specs = get_func_args_specs(self.func)
        func_inputs = {}
        for argname, spec in args_specs.items():
            if spec['element_factory'][0] is None:
                func_inputs[argname] = state
            else:
                element_factory, kwargs = spec['element_factory']
                func_inputs[argname] = element_factory(**kwargs)
        submit = st.button('Submit')
        if submit:
            state[self.view_title] = self.func(**func_inputs)
            st.write(
                'New value stored in state for this function is:',
                state[self.view_title],
            )


from i2 import name_of_obj
from front.py2pydantic import func_to_pyd_input_model_cls, pydantic_model_from_type
import streamlit as st
import streamlit_pydantic as sp  # pip install streamlit-pydantic


class SimplePageFuncPydanticWrite(BasePageFunc):
    def __call__(self, state):
        self.prepare_view(state)
        mymodel = func_to_pyd_input_model_cls(self.func)
        name = name_of_obj(self.func)
        data = sp.pydantic_form(key=f'my_form_{name}', model=mymodel)
        # data = sp.pydantic_input(key=f"my_form_{name}", model=mymodel)

        if data:
            # print(f"--------st.write(self.func(**dict(data)))")
            # print(f"{Sig(self.func)}")
            # print(f"{dict(data)}")
            st.write(self.func(**dict(data)))


class SimplePageFuncPydanticWithOutput(BasePageFunc):
    def __call__(self, state):
        self.prepare_view(state)
        mymodel = func_to_pyd_input_model_cls(self.func)
        mytype = self.func.__annotations__['return']
        output_model = pydantic_model_from_type(mytype)

        name = (
            self.func.__name__
        )  # check in sig, dag, lined a better way, i2, may be displayed name: name_of_obj

        data = sp.pydantic_input(key=f'my_form_{name}', model=mymodel)

        if data:
            func_result = self.func(**data)

            instance = output_model(result=func_result)

            st.write(instance)
            sp.pydantic_output(instance)


# DFLT_CONFIGS = {"page_factory": SimplePageFuncPydanticWrite}
