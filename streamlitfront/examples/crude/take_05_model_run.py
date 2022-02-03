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


"""
from i2 import Sig
def kwargs_trans(outer_kw):
    return dict(
        w=outer_kw['w'] * 2,
        x=outer_kw['w'] * 3,
        # need to pop you (inner func has no you argument)
        y=outer_kw['x'] + outer_kw.pop('you'),
        # Note that no z is mentioned: This means we're just leaving it alone
    )

ingress = Ingress(
    inner_sig=signature(f),
    kwargs_trans=kwargs_trans,
    outer_sig=Sig(f).ch_names(y='you')  # need to give the outer sig a you
    # You could also express it this way (though you'd loose the annotations)
    # outer_sig=lambda w, /, x, you=2, *, z=3: None
)
assert ingress(2, x=3, you=4) == ((4,), {'x': 6, 'y': 7, 'z': 3})

wrapped_f = wrap(f, ingress)
assert wrapped_f(2, x=3, you=4) == '(w:=4) + (x:=6) * (y:=7) ** (z:=3) == 2062'

"""

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
                    store = store_for_param[store_name]
                    store_key = outer_kw[store_name]
                    yield store_name, store[store_key]

            return dict(gen())

        ingress = Ingress(
            inner_sig=Sig(func),
            kwargs_trans=kwargs_trans,
            outer_sig=Sig(func).ch_annotations(**{name: str for name in crude_params})
            # + [
            #     Parameter(
            #         name="save_name",
            #         kind=Parameter.KEYWORD_ONLY,
            #         default="",
            #         annotation=str,
            #     )
            # ]
            # You could also express it this way (though you'd loose the annotations)
            # outer_sig=lambda w, /, x, you=2, *, z=3: None
        )

        # egress = None
        # if output_store_name:
        #     def egress(func_output):
        #         store_for_param[output_store_name]
    wrapped_f = wrap(func, ingress)

    return wrapped_f


def prepare_for_dispatch_00(func):
    """Wrap func into something that is ready for dispatch.
    In real live, apply_model_using_stores will be made automatically by wrapping
    apply_model.
    Here is manual, but we're pretending that this wrapping happens automatically...
    """
    # apply_model_using_stores will be made automatically by wrapping apply_model
    # Here we're just pretending that this wrapping happens automatically
    if func.__name__ == "apply_model":

        def apply_model_using_stores(
            fitted_model,
            fvs,
            method: str = "transform",
            # TODO: Have streamlit populate automatically with auto_key:
            save_name: str = "",
        ):
            # make a name if not given explicitly
            save_name = save_name or auto_key(fitted_model=fitted_model, fvs=fvs)
            # get the inputs
            fitted_model = mall["fitted_model"][fitted_model]
            fvs = mall["fvs"][fvs]
            # compute the function
            result = apply_model(fitted_model, fvs, method=method)
            # store the outputs
            mall["model_results"][save_name] = result

            return result  # or not

        # # just a sanity check
        assert list(mall["model_results"]) == []
        t = apply_model_using_stores(fitted_model="fitted_model_1", fvs="test_fvs")
        print(list(mall["model_results"]))
        assert list(mall["model_results"]) == [
            "fitted_model=fitted_model_1,fvs=test_fvs"
        ]
        assert all(t == np.array([[0.0], [1.0], [0.5], [2.25], [-1.5]]))
        mall["model_results"].clear()

        return apply_model_using_stores
    else:
        raise ValueError(f"Can't dispatch {func}")


if __name__ == "__main__":
    from streamlitfront.base import dispatch_funcs

    app = dispatch_funcs([prepare_for_crude_dispatch(apply_model)])
    app()
