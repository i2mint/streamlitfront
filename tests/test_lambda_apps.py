"""A lambda can be served: its widgets keep their state across Streamlit reruns
(i2mint/streamlitfront#6). Runs the app headlessly with ``AppTest``."""

import pytest

pytest.importorskip("streamlit.testing.v1")
from streamlit.testing.v1 import AppTest

APP = """
from streamlitfront import mk_app
mk_app([lambda res: res, lambda a, b=1: a])()
"""


def test_lambda_input_and_output_survive_the_rerun():
    at = AppTest.from_string(APP, default_timeout=30).run()
    assert not at.exception
    at.text_input[0].set_value("hello").run()  # (each interaction reruns the script)
    at.button[0].click().run()
    assert not at.exception
    assert [m.value for m in at.markdown][-1] == "hello"
    assert at.text_input[0].value == "hello"


def test_lambda_names_are_stable_and_distinct_across_reruns():
    from streamlitfront.util import name_lambdas

    def run():
        return [o.__name__ for o in name_lambdas([lambda: 1, lambda: 2])]

    assert run() == run() == ["lambda_1", "lambda_2"]


def test_partial_of_a_lambda_has_a_stable_name_across_reruns():
    from functools import partial

    from streamlitfront.util import name_lambdas

    def run():
        objs = [lambda: 1, partial(lambda res, k=1: res, k=2), partial(lambda: 3)]
        return [o.__name__ for o in name_lambdas(objs)]

    assert run() == run() == ["lambda_1", "lambda_2", "lambda_3"]
