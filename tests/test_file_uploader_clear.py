"""A file uploader is emptied after a successful submit, so the next upload doesn't start
from the previous selection (i2mint/front#24). Runs the app headlessly with ``AppTest``.
"""

import copy

import pytest

pytest.importorskip("streamlit.testing.v1")
from streamlit.testing.v1 import AppTest

from streamlitfront import spec_maker



@pytest.fixture(autouse=True)
def _isolate_default_convention():
    """Building an app writes its inputs into the shared default convention (i2mint/front#39);
    undo that so the apps of these tests don't see each other."""
    saved = copy.deepcopy(spec_maker.DFLT_CONVENTION_DICT)
    yield
    spec_maker.DFLT_CONVENTION_DICT.clear()
    spec_maker.DFLT_CONVENTION_DICT.update(saved)


APP = """
import streamlit as st
from front import APP_KEY, RENDERING_KEY, ELEMENT_KEY
from streamlitfront import mk_app
from streamlitfront.elements import FileUploader, MultiSourceInput, TextOutput

def count_bytes(data: list) -> int:
    if not data or not sum(len(f.getvalue()) for f in data):
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
    """A submit whose function raises submitted nothing, so nothing is cleared."""
    at = _run_app()
    at.button[0].click().run()
    assert at.exception  # ValueError from the function propagates, as before
    at = _run_app()
    at.file_uploader[0].upload("a.txt", b"").run()  # selected, but empty: it raises
    assert _names(at) == ["a.txt"]
    at.button[0].click().run()
    assert at.exception
    assert _names(at) == ["a.txt"]


KWARGS_APP = """
from front import APP_KEY, RENDERING_KEY, ELEMENT_KEY
from i2 import Sig
from streamlitfront import mk_app
from streamlitfront.elements import FileUploader, KwargsInput, TextOutput

def sum_kwargs(kwargs: dict) -> int:
    return sum(len(f.getvalue()) for f in kwargs["data"])

def inner(data: list): ...

class Files(FileUploader):
    def render(self):
        return super().render() or []

mk_app(
    [sum_kwargs],
    config={
        APP_KEY: {"title": "t"},
        RENDERING_KEY: {
            "sum_kwargs": {
                "execution": {
                    "inputs": {
                        "kwargs": {
                            ELEMENT_KEY: KwargsInput,
                            "func_sig": Sig(inner),
                            "inputs": {
                                "data": {
                                    ELEMENT_KEY: Files,
                                    "accept_multiple_files": True,
                                    **EXTRA,
                                }
                            },
                        }
                    },
                    "output": {ELEMENT_KEY: TextOutput},
                }
            }
        },
    },
)()
"""


def _run_kwargs_app(**uploader_spec):
    script = KWARGS_APP.replace("EXTRA", repr(uploader_spec))
    at = AppTest.from_string(script, default_timeout=30).run()
    assert not at.exception
    return at


def test_uploader_inside_a_kwargs_input_is_emptied_after_submit():
    """streamlitfront#14: the uploader lives in the nested section of a KwargsInput."""
    at = _run_kwargs_app()
    at.file_uploader[0].upload("a.txt", b"12345").run()
    assert _names(at) == ["a.txt"]
    at.button[0].click().run()
    assert not at.exception
    assert _output(at) == ["`5`"]
    assert _names(at) == []
    assert len(at.file_uploader) == 1  # replaced, not added
    at.file_uploader[0].upload("b.txt", b"67").run()
    assert _names(at) == ["b.txt"]


def test_clear_after_submit_false_keeps_a_kwargs_input_selection():
    at = _run_kwargs_app(clear_after_submit=False)
    at.file_uploader[0].upload("a.txt", b"12345").run()
    at.button[0].click().run()
    assert _output(at) == ["`5`"]
    assert _names(at) == ["a.txt"]
