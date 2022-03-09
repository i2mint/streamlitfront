"""
Base for UI generation
"""
from collections import ChainMap
from typing import Callable, Any, Union, Mapping, Iterable
from functools import partial
import typing

import streamlit as st

from i2 import Sig
from streamlitfront.session_state import get_state, _SessionState
from streamlitfront.util import func_name, build_element_factory

# --------------------- types/protocols/interfaces --------------------------------------

Map = Union[None, Mapping, Callable[[], Mapping]]
Configuration = Mapping
Convention = Mapping
PageFunc = Callable[[_SessionState], Any]
PageName = str
PageSpec = Mapping[PageName, PageFunc]
App = Callable
AppMaker = Callable[[Iterable[Callable], Configuration], App]

# ------- configuration/convention/default management -----------------------------------


# TODO: Lots of configs/convention/defaults stuff piling up: Needs it's own module


def func_to_page_name(func, **kwargs):
    return func_name(func).replace('_', ' ').title()


# TODO: Need to enforce SOME structure/content. Use a subclass of util.Objdict instead?
def dflt_convention():
    return dict(
        app_maker=pages_app,
        page_configs=dict(layout='wide'),
        func_to_page_name=func_to_page_name,
    )


def _get_map(mapping: Map) -> Mapping:
    """Get a concrete mapping from a flexible specification (e.g. could be a factory)"""
    if isinstance(mapping, Callable):
        return mapping()  # it's a factory, get the actual mapping
    else:
        return mapping or {}


def _get_configs(configs: Map = None, convention: Map = dflt_convention):
    configs, convention = map(_get_map, (configs, convention))  # get concrete mappings
    configs = ChainMap(configs, convention)  # merge them
    return configs


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


# def func_to_page_name(func: Callable, page_name_for_func: Map = None, **configs) -> str:
#     """Get page name for function.
#     If explicit in  page_name_for_func
#     """
#     page_name_for_func = page_name_for_func or {}
#     func_name_str = page_name_for_func.get(func, None)
#     if func_name_str is not None:
#         return func_name_str
#     else:
#         return mk_func_name(func)

# ---------------------------------------------------------------------------------------
# The main function and raison d'etre of front


def dispatch_funcs(
    funcs: Iterable[Callable], configs: Map = None, convention: Map = dflt_convention,
) -> App:
    """Call this function with target funcs and get an app to run."""
    configs = _get_configs(configs, convention)
    app_maker = configs['app_maker']
    assert isinstance(app_maker, Callable)
    return partial(app_maker, funcs=funcs, configs=configs)


# ---------------------------------------------------------------------------------------

missing = type('Missing', (), {})()


def infer_type(sig, name):
    if name in sig.annotations:
        return sig.annotations[name]
    elif name in sig.defaults:
        dflt = sig.defaults[name]
        if dflt is not None:
            return type(dflt)
    else:
        return missing


def _get_dflt_element_factory_for_annot():
    # _ = _get_state()
    return {
        int: st.number_input,
        float: st.number_input,
        str: st.text_input,
        bool: st.checkbox,
        # TODO: OL: selectbox result is singular; not a list.
        #   In situations where we need a lit of items from a collection of
        #   of possibilities, we can use multiselect (if not too many options).
        #   But even that is not general enough. We should either not handle iterbles
        #   in defaults, or, once we have it, open a list selection widget that would
        #   offer the possibilities (comma separated string, upload csv/excel/pickle
        #   etc.).
        # list: st.selectbox,
        # tuple: st.selectbox,
        # type(lambda df: df) is just function
        # type(
        #     lambda df: df
        # ): st.file_uploader,  # TODO: Find a better way to identify as file_uploader
        # type(_): None,
        # TODO: Below can be computed and injected in dict
        #  ... But is it correct? ONe number input for iterables?
        # typing.Iterable[int]: (st.number_input, int),
        # typing.Iterable[float]: (st.number_input, float),
        # typing.Iterable[str]: (st.number_input, str),
        # typing.Iterable[bool]: (st.number_input, bool),
        # typing.Dict[str, int]: (st.number_input, str, int),
        # typing.Dict[str, float]: (st.number_input, str, float),
        # typing.Dict[str, str]: (st.number_input, str, str),
        # typing.Dict[str, bool]: (st.number_input, str, bool),
    }


#
# TODO: Too messy -- needs some design thinking
# TODO: Basic: Add some more smart mapping
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
                    # TODO: This case seems false (maybe? don't want multiple choice
                    #  when default is a list)
                    # TODO: When we have list defaults, error occurs
                    factory_kwargs['options'] = dflt
                else:
                    factory_kwargs['value'] = dflt

        d['element_factory'] = (element_factory, factory_kwargs)

    return func_args_specs


class BasePageFunc:
    def __init__(self, func: Callable, view_title: str = '', **configs):
        self.func = func
        self.view_title = view_title
        self.configs = configs
        self.sig = Sig(func)

    def prepare_view(self, state):
        if self.view_title:
            st.markdown(f'''## **{self.view_title}**''')

    def __call__(self, state):
        self.prepare_view(state)
        st.write(self.sig)  # Was Sig(self.func)


class SimplePageFunc(BasePageFunc):
    def __call__(self, state):
        self.prepare_view(state)
        args_specs = get_func_args_specs(self.func)
        # func_inputs = dict(self.sig.defaults, **state['page_state'][self.func])
        func_inputs = {}
        for argname, spec in args_specs.items():
            element_factory, kwargs = spec['element_factory']
            func_inputs[argname] = element_factory(**kwargs)
        submit = st.button('Submit')
        if submit:
            st.write(self.func(**func_inputs))
            # state['page_state'][self.func].clear()


DFLT_PAGE_FACTORY = SimplePageFunc  # Try BasePageFunc too

#
# # TODO: Code this!
# def get_page_callbacks(funcs, page_names, page_factory=DFLT_PAGE_FACTORY, **configs):
#     return [
#         page_factory(func, page_name, **configs)
#         for func, page_name in zip(funcs, page_names)
#     ]


# TODO: Get func_page for real
def get_pages_specs(
    funcs: Iterable[Callable],
    func_to_page_name: Callable = func_to_page_name,
    page_factory=DFLT_PAGE_FACTORY,
    **configs,
) -> PageSpec:
    """Get pages specification dict"""
    page_names = [func_to_page_name(func, **configs) for func in funcs]
    page_callbacks = [
        page_factory(func, page_name, **configs)
        for func, page_name in zip(funcs, page_names)
    ]
    return dict(zip(page_names, page_callbacks))


def _get_view_key(
    view_keys,
    container=st.sidebar,
    title='Navigation',
    chooser='radio',  # TODO: make into enum
    **chooser_kwargs,
):
    if title is not None:
        container.title(title)  # title
    input_element = getattr(container, chooser)
    page_key = input_element(options=view_keys, **chooser_kwargs)
    return page_key


def pages_app(funcs, configs):
    # Page setup

    # Note: set_page_config at top: needs to be the first call after importing streamlit
    st.set_page_config(layout='wide')

    state = get_state(hash_funcs=dflt_hash_funcs)  # TODO: get from configs

    # # Experimentation -- to be reviewed if kept #############
    # if 'page_state' not in state:
    #     state['page_state'] = {}
    #     for func in funcs:
    #         state['page_state'][func] = {}
    # full page layout style
    # st.set_page_config(**configs.get('page_config', {}))
    # configs don't work here because the layout call has to be the first call after
    # importing streamlit

    # # Page setup
    # st.set_page_config(layout="wide")

    # Make page objects
    views = get_pages_specs(funcs, **configs)
    state['views'] = views

    # TODO: The above is static: Should the above be done only once, and cached?
    #   Perhaps views should be cached in state?

    # Setup navigation
    view_key = _get_view_key(tuple(views.keys()), label='Select your view')

    # navigation_container = st.sidebar  # container
    # navigation_container.title('Navigation')  # title
    # page_key = navigation_container.radio(  # view component kind
    #     'Select your page',  # label
    #     tuple(pages.keys())  # options
    # )

    # Display the selected page with the session state
    # This is the part that actually runs the functionality that pages specifies
    view_runner = views[view_key]  # gets the page runner
    view_runner(state)  # runs the page with the state

    # Mandatory to avoid rollbacks with widgets, must be called at the end of your app
    state.sync()
