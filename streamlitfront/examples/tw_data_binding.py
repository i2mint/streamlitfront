import os


def foo(text: str, integer: int, floating: float = 1.0):
    """C'est foo"""
    return text, integer, floating


def bar(a: str = 'boo'):
    """About bar"""
    return a


funcs = [foo, bar]

from streamlitfront.base import (
    get_state,
    _get_view_key,
    get_pages_specs,
    dflt_hash_funcs,
)

import streamlit as st


def pages_app(funcs, configs):
    state = get_state(hash_funcs=dflt_hash_funcs)  # TODO: get from configs

    # Page setup
    st.set_page_config(layout='wide')

    # Make page objects
    views = get_pages_specs(funcs, **configs)
    state['views'] = views

    # TODO: The above is static: Should the above be done only once, and cached?
    #   Perhaps views should be cached in state?

    # Setup navigation
    view_key = _get_view_key(tuple(views.keys()), label='Select your view')

    # Display the selected page with the session state
    # This is the part that actually runs the functionality that pages specifies
    view_runner = views[view_key]  # gets the page runner
    view_runner(state)  # runs the page with the state

    # Mandatory to avoid rollbacks with widgets, must be called at the end of your app
    state.sync()


if __name__ == '__main__':
    from streamlitfront.base import dispatch_funcs
    from streamlitfront.page_funcs import ExperimentalViewFunc

    print('file: {}'.format(os.path.realpath(__file__)))

    app = dispatch_funcs(funcs, configs=dict(page_factory=ExperimentalViewFunc))

    app()
