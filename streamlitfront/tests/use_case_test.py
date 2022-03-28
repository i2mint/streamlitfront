import pickle
from xml.etree.ElementPath import prepare_child
import pytest
from i2 import Sig
import dill
from front.tests.test_use_case import base_test_use_case, TEST_USE_CASE_PARAMETER_NAMES, TEST_USE_CASE_PARAMETERS
from streamlitfront.run_app import run_app
from streamlitfront.tests.common import (
    compute_output, select_func, send_input,
    dispatch_funcs_with_selenium,
)

def mk_ui_func(func, funcs, dom):
    sig = Sig(func)

    @sig
    def ui_func(*args, **kwargs):
        def send_inputs():
            kw = sig.kwargs_from_args_and_kwargs(args, kwargs)
            for idx, param in enumerate(sig):
                input_ = kw.get(param)
                if input_ is not None:
                    annotation = sig.annotations.get(param)
                    if annotation:
                        input_ = annotation(input_)
                    send_input(input_, idx, dom)

        func_idx = funcs.index(func)
        select_func(func_idx, dom)
        send_inputs()
        return compute_output(func, dom)

    return ui_func


@pytest.mark.parametrize(
    TEST_USE_CASE_PARAMETER_NAMES,
    TEST_USE_CASE_PARAMETERS
)
def test_use_case(headless, use_case, func_src, kwargs):
    from meshed.makers import code_to_dag
    from front.dag import crudify_func_nodes
    from front.tests.util import get_var_nodes_to_crudify

    dag = code_to_dag(use_case, func_src=func_src)
    dispatch_func_src = dict(func_src)
    var_nodes_to_crudify = get_var_nodes_to_crudify(dispatch_func_src.values())
    front_dag_kwargs = dict(kwargs)
    if var_nodes_to_crudify:
        mall = dict()
        for k, v in kwargs.items():
            if k in var_nodes_to_crudify:
                store_key = str(v)
                mall[f'{k}_store'] = {store_key: v}
                front_dag_kwargs[k] = store_key
        crudified_dag = crudify_func_nodes(var_nodes_to_crudify, dag, mall=mall)
        # assert crudified_dag(**front_dag_kwargs) == dag(**kwargs)
        dispatch_func_src = {func_node.name: func_node.func for func_node in crudified_dag.func_nodes}
    dispatch_funcs = list(dispatch_func_src.values())
    with dispatch_funcs_with_selenium(dispatch_funcs, headless=headless) as dom:
        front_func_src = {
            node_name: mk_ui_func(func, dispatch_funcs, dom)
            for node_name, func in dispatch_func_src.items()
        }
        front_dag = code_to_dag(use_case, func_src=front_func_src)
        assert front_dag(**front_dag_kwargs) == dag(**kwargs)
    


    # funcs = list(func_src.values())
    # dispatch_funcs = prepare_to_dispatch(funcs)
    # with dispatch_funcs_with_selenium(dispatch_funcs, headless) as dom:
    #     base_test_use_case(
    #         use_case=use_case,
    #         func_src=func_src,
    #         inputs=inputs,
    #         mk_front_func=mk_ui_func,
    #         funcs=funcs,
    #         dom=dom,
    #     )
