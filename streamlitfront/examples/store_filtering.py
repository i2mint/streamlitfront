"""This app demos filtering the keys of a store"""

import re
from pyckup import grab
from dol import filt_iter

from front import APP_KEY, RENDERING_KEY, ELEMENT_KEY

from streamlitfront.elements import FloatSliderInput
from streamlitfront.base import mk_app


# TODO: have front (output) elements for iterables (example: paged iteration)
# TODO: Currying functionality in front


def filter_store(store: str, filt: str, flags=0):
    if isinstance(store, str):
        store_url = store
        store = grab(store_url)
    else:
        raise TypeError(f"store can only be str at this point: {store}")
    if isinstance(filt, str):
        filt = re.compile(filt, flags).search
    else:
        raise TypeError(f"filt can only be str at this point: {filt}")

    return filt_iter(store, filt=filt)


# filter_store(
#     '/Users/thorwhalen/Dropbox/_odata/sound/guns', filt='machine'
# )


if __name__ == "__main__":
    app = mk_app(
        [filter_store],
        # config={
        #     APP_KEY: {"title": "My app"},
        #     RENDERING_KEY: {
        #         # 'foo': {
        #         #     'execution': {'inputs': {'a': {ELEMENT_KEY: TextInput,}},}
        #         # },
        #         "proportion": {
        #             "execution": {
        #                 "inputs": {
        #                     "p": {
        #                         ELEMENT_KEY: FloatSliderInput,
        #                     }
        #                 },
        #             }
        #         }
        #     },
        # },
    )
    app()
