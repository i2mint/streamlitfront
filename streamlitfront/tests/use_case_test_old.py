from functools import partial
import pytest
from i2 import Sig
from front.tests.test_use_case import (
    base_test_use_case,
    TEST_USE_CASE_PARAMETER_NAMES,
    TEST_USE_CASE_PARAMETERS,
)
from streamlitfront.tests.common import (
    compute_output,
    select_func,
    send_input,
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


@pytest.mark.parametrize(TEST_USE_CASE_PARAMETER_NAMES, TEST_USE_CASE_PARAMETERS)
def test_use_case(headless, use_case, func_src, kwargs):
    base_test_use_case(
        use_case=use_case,
        func_src=func_src,
        inputs=kwargs,
        mk_front_func=mk_ui_func,
        run_front_app=partial(dispatch_funcs_with_selenium, headless=headless),
    )
