# import pytest
# from front.tests.util import rdm_int, rdm_float, rdm_str

# from streamlitfront.tests.common import (
#     compute_output,
#     select_func,
#     send_input,
#     dispatch_funcs_with_selenium,
# )


# def foo(a: int = 0, b: int = 0, c=0) -> int:
#     """This is foo. It computes something"""
#     return (a * b) + c


# def bar(x: str, greeting="hello") -> str:
#     """bar greets its input"""
#     return f"{greeting} {x}"


# def confuser(a: int = 0, x: float = 3.14) -> float:
#     return (a**2) * x


# # def wait_to_render(cls):
# #     for attr, val in cls.__dict__.items():
# #         if callable(val) and attr.startswith('find_element'):
# #             setattr(cls, attr, give_a_chance_to_render_element(val))
# #     return cls


# # WebElement = wait_to_render(WebElement)


# @pytest.mark.parametrize(
#     "spec",
#     [
#         (
#             {
#                 foo: [
#                     (rdm_int(),),
#                     (rdm_int(), rdm_int()),
#                     (rdm_int(), rdm_int(), rdm_int()),
#                 ]
#             }
#         ),
#         (
#             {
#                 foo: [(rdm_int(), rdm_int(), rdm_int())],
#                 bar: [
#                     (rdm_str(),),
#                     (rdm_str(), rdm_str()),
#                 ],
#             }
#         ),
#         (
#             {
#                 foo: [(rdm_int(), rdm_int(), rdm_int())],
#                 bar: [(rdm_str(), rdm_str())],
#                 confuser: [
#                     (rdm_int(),),
#                     (rdm_int(), rdm_float()),
#                 ],
#             }
#         ),
#     ],
# )
# def test_dispatch_funcs(headless, spec: dict):
#     def test_func(func_idx, func):
#         def test_inputs(inputs):
#             for input_idx, input_ in enumerate(inputs):
#                 send_input(input_, input_idx, dom)
#             output = compute_output(func, dom)
#             assert output == func(*inputs)

#         input_spec = spec[func]
#         select_func(func_idx, dom)
#         for inputs in input_spec:
#             test_inputs(inputs)

#     funcs = list(spec)
#     with dispatch_funcs_with_selenium(funcs, headless=headless) as dom:
#         for func_idx, func in enumerate(funcs):
#             test_func(func_idx, func)
