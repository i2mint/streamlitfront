"""
Same as take_04_model_run, but where the dispatch is not as manual.
"""

# This is what we want our "dispatchable" wrapper to look like

# There should be real physical stores for those types (FVs, FittedModel) that need them
from typing import Any, Mapping, Tuple

import numpy as np
from sklearn.preprocessing import MinMaxScaler

FVs = Any
FittedModel = Any

# ---------------------------------------------------------------------------------------
# The function(ality) we want to dispatch:
def apply_model(fitted_model: FittedModel, fvs: FVs, method="transform"):
    method_func = getattr(fitted_model, method)
    return method_func(list(fvs))


# ---------------------------------------------------------------------------------------
# The stores that will be used -- here, all stores are just dictionaries, but the
# contract is with the typing.Mapping (read-only here) interface.
# As we grow up, we'll use other mappings, such as:
# - server side RAM (as done here, simply)
# - server side persistence (files or any DB or file system thanks to the dol package)
# - computation (when you want the request for a key to actually launch a process that
#   will generate the value for you (some say you should be obvious to that detail))
# - client side RAM (when we figure that out)

mall = dict(
    fvs=dict(
        train_fvs_1=np.array([[1], [2], [3], [5], [4], [2], [1], [4], [3]]),
        train_fvs_2=np.array([[1], [10], [5], [3], [4]]),
        test_fvs=np.array([[1], [5], [3], [10], [-5]]),
    ),
    fitted_model=dict(
        fitted_model_1=MinMaxScaler().fit(
            [[1], [2], [3], [5], [4], [2], [1], [4], [3]]
        ),
        fitted_model_2=MinMaxScaler().fit([[1], [10], [5], [3], [4]]),
    ),
    model_results=dict(),
)

# ---------------------------------------------------------------------------------------
# dispatchable function:

from streamlitfront.examples.crude.crude_util import auto_key

from i2 import Sig
from i2.wrapper import Ingress, wrap
from inspect import Parameter


def prepare_for_crude_dispatch(func, store_for_param=None, output_store_name=None):
    """Wrap func into something that is ready for CRUDE dispatch."""

    ingress = None
    if store_for_param is not None:
        sig = Sig(func)
        crude_params = [x for x in sig.names if x in store_for_param]

        def kwargs_trans(outer_kw):
            def gen():
                for store_name in crude_params:
                    store_key = outer_kw[store_name]
                    yield store_name, store_for_param[store_name][store_key]

            return dict(gen())

        save_name_param = Parameter(
            name="save_name",
            kind=Parameter.KEYWORD_ONLY,
            default="",
            annotation=str,
        )

        ingress = Ingress(
            inner_sig=sig,
            kwargs_trans=kwargs_trans,
            outer_sig=(
                sig.ch_annotations(**{name: str for name in crude_params})
                + [save_name_param]
            ),
        )

        egress = None
        if output_store_name:

            def egress(func_output):
                print(f"{list(store_for_param[output_store_name])=}")
                store_for_param[output_store_name] = func_output
                print(f"{list(store_for_param[output_store_name])=}")
                return func_output

    wrapped_f = wrap(func, ingress, egress)

    return wrapped_f


f = prepare_for_crude_dispatch(apply_model, mall)
assert all(
    f("fitted_model_1", "test_fvs") == np.array([[0.0], [1.0], [0.5], [2.25], [-1.5]])
)

# Some type information (just for the reader!)
StoreName = str
KT = str
VT = Any
StoreType = Mapping[KT, VT]
Mall = Mapping[StoreName, StoreType]


def simple_mall_dispatch_core_func(
    key: KT, action: str, store_name: StoreName, mall: Mall
):
    if not store_name:
        # if store_name empty, list the store names (i.e. the mall keys)
        return list(mall)
    else:  # if not, get the store
        store = mall[store_name]

    if action == "list":
        key = key.strip()  # to handle some invisible whitespace that would screw things
        return list(filter(lambda k: key in k, store))
    elif action == "get":
        return store[key]

# TODO: the function doesn't see updates made to mall. Fix.
# Just the partial (with mall set), but without mall arg visible (or will be dispatched)
def explore_mall(key: KT, action: str, store_name: StoreName):
    return simple_mall_dispatch_core_func(key, action, store_name, mall=mall)


# Attempt to do this wit i2.wrapper
# from functools import partial
# from i2.wrapper import remove_params_ingress_factory, wrap
#
# without_mall_param = partial(
#     wrap, ingress=partial(remove_params_ingress_factory, params_to_remove="mall")
# )
# mall_exploration_func = without_mall_param(
#     partial(simple_mall_dispatch_core_func, mall=mall)
# )
# mall_exploration_func.__name__ = "explore_mall"

if __name__ == "__main__":
    from streamlitfront.base import dispatch_funcs
    from functools import partial

    dispatchable_apply_model = prepare_for_crude_dispatch(
        apply_model, store_for_param=mall, output_store_name="model_results"
    )
    # extra, to get some defaults in:
    dispatchable_apply_model = partial(
        dispatchable_apply_model,
        fitted_model='fitted_model_1',
        fvs='test_fvs',
    )
    app = dispatch_funcs([dispatchable_apply_model, explore_mall])
    app()
