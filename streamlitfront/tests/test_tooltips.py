"""Docs of a function flow into streamlit's ``help=`` (streamlitfront#26)."""

from streamlit.testing.v1 import AppTest

_SCRIPT = '''
from streamlitfront import mk_app

def foo(a: int = 1, b: str = "x"):
    """Summary line.

    :param a: the a
    :param b: the b
    """
    return a

mk_app([foo])()
'''


def test_docs_become_help():
    at = AppTest.from_string(_SCRIPT)
    at.run()
    assert not at.exception
    assert at.number_input[0].help == "the a"
    assert at.text_input[0].help == "the b"
    assert any(m.help == "Summary line." for m in at.markdown)
