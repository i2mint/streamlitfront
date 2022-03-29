import dill
from sys import argv
from typing import Callable, Iterable, Union
import streamlit.bootstrap
from streamlitfront.base import Map, dflt_convention, dispatch_funcs


def run_app(
    funcs: Union[Iterable[Callable], bytes],
    configs: Map = None,
    convention: Map = dflt_convention,
):
    _funcs = dill.loads(funcs) if isinstance(funcs, bytes) else funcs
    kwargs = dict(configs=configs, convention=convention,)
    streamlit.bootstrap.run(
        __file__,
        args=[dill.dumps(_funcs), dill.dumps(kwargs)],
        command_line='',
        flag_options={},
    )


if __name__ == '__main__':
    funcs = dill.loads(argv[1])
    kwargs = dill.loads(argv[2])
    app = dispatch_funcs(funcs, **kwargs)
    app()
