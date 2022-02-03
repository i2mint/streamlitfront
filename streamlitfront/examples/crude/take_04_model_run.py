"""
An example of how to transform (manually) a function that runs some data through a model
(both too complex to enter directly and explicitly in forms) into a streamlit
dispatchable function that uses a store (a Mapping) to manage complex data.
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
def apply_model(fvs: FVs, fitted_model: FittedModel, method="transform"):
    method_func = getattr(fitted_model, method)
    return method_func(list(fvs))


# really, should be a str from a list of options, given by list(fvs_store)
FVsKey = str
# really, should be a str from a list of options, given by list(fitted_model_store)
FittedModelKey = str
Result = Any
ResultKey = str

mall = dict(
    fvs=dict(  # Mapping[FVsKey, FVs]
        train_fvs_1=np.array([[1], [2], [3], [5], [4], [2], [1], [4], [3]]),
        train_fvs_2=np.array([[1], [10], [5], [3], [4]]),
        test_fvs=np.array([[1], [5], [3], [10], [-5]]),
    ),
    fitted_model=dict(  # Mapping[FittedModelKey, FittedModel]
        fitted_model_1=MinMaxScaler().fit(
            [[1], [2], [3], [5], [4], [2], [1], [4], [3]]
        ),
        fitted_model_2=MinMaxScaler().fit([[1], [10], [5], [3], [4]]),
    ),
    model_results=dict(),  # Mapping[ResultKey, Result]
)

# ---------------------------------------------------------------------------------------
# dispatchable function:


def auto_key(*args, **kwargs):
    """
    >>> auto_key(1,2,c=3,d=4)
    '1,2,c=3,d=4'
    >>> auto_key(1,2)
    '1,2'
    >>> auto_key(c=3,d=4)
    'c=3,d=4'
    >>> auto_key()
    ''
    """
    args_str = ",".join(map(str, args))
    kwargs_str = ",".join(map(lambda kv: f"{kv[0]}={kv[1]}", kwargs.items()))
    return ",".join(filter(None, [args_str, kwargs_str]))


def apply_model_using_stores(
    fvs: FVsKey,
    fitted_model: FittedModelKey,
    method: str = "transform",
    save_name: str = '',  # TODO: Have streamlit populate automatically with auto_key
):
    # get the inputs
    fvs_value = mall["fvs"][fvs]
    fitted_model_value = mall["fitted_model"][fitted_model]
    # compute the function
    result = apply_model(fvs_value, fitted_model_value, method=method)
    # store the outputs
    save_name = save_name or auto_key(fvs=fvs, fitted_model=fitted_model)
    mall["model_results"][save_name] = result
    return result  # or not


assert list(mall["model_results"]) == []
t = apply_model_using_stores(fvs="test_fvs", fitted_model="fitted_model_1")
assert list(mall["model_results"]) == ["fvs=test_fvs,fitted_model=fitted_model_1"]
assert all(t == np.array([[0.0], [1.0], [0.5], [2.25], [-1.5]]))
mall["model_results"].clear()


if __name__ == "__main__":
    from streamlitfront.base import dispatch_funcs

    app = dispatch_funcs([apply_model_using_stores])
    app()
