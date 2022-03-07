import pickle
from sys import argv
from typing import Callable, Iterable
import streamlit.bootstrap
from streamlitfront.base import Map, dflt_convention, dispatch_funcs


def run_app(
    funcs: Iterable[Callable], configs: Map = None, convention: Map = dflt_convention
):
    kwargs = dict(configs=configs, convention=convention,)
    streamlit.bootstrap.run(
        __file__,
        args=[pickle.dumps(funcs), pickle.dumps(kwargs)],
        command_line='',
        flag_options={},
    )


if __name__ == '__main__':
    funcs = pickle.loads(argv[1])
    kwargs = pickle.loads(argv[2])
    app = dispatch_funcs(funcs, **kwargs)
    app()
