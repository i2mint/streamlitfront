"""A file uploader is emptied after a successful submit, so the next upload doesn't start
from the previous selection (i2mint/front#24). Runs the app headlessly with ``AppTest``.
"""

import pytest

pytest.importorskip("streamlit.testing.v1")
from streamlit.testing.v1 import AppTest

APP = """
import streamlit as st
from front import APP_KEY, RENDERING_KEY, ELEMENT_KEY
from streamlitfront import mk_app
from streamlitfront.elements import FileUploader, MultiSourceInput, TextOutput

def count_bytes(data: list) -> int:
    if not data:
        raise ValueError("no data")
    st.info("drawn by the function")
    return sum(len(f.getvalue()) for f in data)

class Files(FileUploader):
    def render(self):
        return super().render() or []

data_spec = {ELEMENT_KEY: Files, "accept_multiple_files": True, **EXTRA}
if MULTI:
    data_spec = {ELEMENT_KEY: MultiSourceInput, "From files": data_spec}

mk_app(
    [count_bytes],
    config={
        APP_KEY: {"title": "t"},
        RENDERING_KEY: {
            "count_bytes": {
                "execution": {
                    "inputs": {"data": data_spec},
                    "output": {ELEMENT_KEY: TextOutput},
                }
            }
        },
    },
)()
"""


def _run_app(*, multi=False, **uploader_spec):
    script = APP.replace("EXTRA", repr(uploader_spec)).replace("MULTI", repr(multi))
    at = AppTest.from_string(script, default_timeout=30).run()
    assert not at.exception
    return at


def _names(at):
    return [f.name for f in at.file_uploader[0].value]


def _output(at):
    return [m.value for m in at.markdown if m.value.startswith("`")]


@pytest.mark.parametrize("multi", [False, True])
def test_uploader_is_emptied_after_submit_and_output_is_kept(multi):
    at = _run_app(multi=multi)
    at.file_uploader[0].upload("a.txt", b"12345").run()
    assert _names(at) == ["a.txt"]
    at.button[0].click().run()
    assert not at.exception
    assert _names(at) == []
    assert len(at.file_uploader) == 1  # replaced, not added
    assert _output(at) == ["`5`"]
    assert [i.value for i in at.info] == [
        "drawn by the function"
    ]  # nothing redrawn away
    # a new upload starts from a clean selection; the stale output goes away as before
    at.file_uploader[0].upload("b.txt", b"67").run()
    assert _names(at) == ["b.txt"]
    assert _output(at) == []


def test_clear_after_submit_false_keeps_the_selection():
    at = _run_app(clear_after_submit=False)
    at.file_uploader[0].upload("a.txt", b"12345").run()
    at.button[0].click().run()
    assert _names(at) == ["a.txt"]
    assert _output(at) == ["`5`"]


def test_failed_submit_keeps_the_selection():
    """The function raises on empty data; nothing was submitted, so nothing is cleared."""
    at = _run_app()
    at.button[0].click().run()
    assert at.exception  # ValueError from the function propagates, as before
    at.file_uploader[0].upload("a.txt", b"").run()
    assert _names(at) == ["a.txt"]
