"""This app demos filtering the keys of a store"""

import re
from pyckup import grab
from dol import filt_iter
from i2 import Pipe
from front import APP_KEY, RENDERING_KEY, ELEMENT_KEY

from streamlitfront.elements import FloatSliderInput
from streamlitfront.base import mk_app
from streamlitfront.elements import TextOutput


# TODO: Being able to use Pipe to do pre and post processing in front elements
# TODO: have front (output) elements for iterables (example: paged iteration)
# TODO: Currying functionality in front


def filter_store(store: str, filt: str, flags: int = 0):
    if isinstance(store, str):
        store_url = store
        store = grab(store_url)
    else:
        raise TypeError(f'store can only be str at this point: {store}')
    if isinstance(filt, str):
        filt = re.compile(filt, flags).search
    else:
        raise TypeError(f'filt can only be str at this point: {filt}')

    return filt_iter(store, filt=filt)


# filter_store(
#     '/Users/thorwhalen/Dropbox/_odata/sound/guns', filt='machine'
# )

# class list_then_text_output(TextOutput):
#     preprocess()
from i2 import wrap
from i2.deco import postprocess


def list_keys(store_, max_keys: int = 100):
    from itertools import islice

    n = len(store_)
    first_keys = '\n\r'.join(islice(store_, 0, max_keys))
    import pandas as pd

    return pd.DataFrame(store_)
    return f'----- {n} keys. Below, the first {min(n, max_keys)} ----- \n\r{first_keys}'


from lined import LineParametrized

f = wrap(filter_store, egress=list_keys)
f.__name__ = 'filter_store'

if __name__ == '__main__':
    app = mk_app(
        # [filter_store],
        [wrap(filter_store, egress=list_keys)],
        # [LineParametrized(filter_store, list_keys)],
        # [postprocess(list)(filter_store)],
        config={
            APP_KEY: {'title': 'My app'},
            RENDERING_KEY: {
                'filter_store': {
                    'execution': {'output': TextOutput},
                    # 'execution': {'output': Pipe(list, TextOutput)},
                },
            },
        },
    )
    app()
