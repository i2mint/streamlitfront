"""Pytest configuration for the in-package tests.

``common.py`` and ``use_case_test_old.py`` drive a real browser through selenium; they
cannot even be imported without the optional e2e dependencies (``tests/test_requirements.txt``),
so they are left out of collection when those are missing instead of breaking it.
"""

from importlib.util import find_spec


def _importable(name: str) -> bool:
    try:
        return find_spec(name) is not None
    except ImportError:  # a parent package is missing
        return False


_E2E_MODULES = ("selenium", "webdriver_manager", "strand")
_E2E_FILES = ("common.py", "use_case_test_old.py")

collect_ignore = (
    []
    if all(map(_importable, _E2E_MODULES))
    and _importable("front.tests.test_use_case")
    else list(_E2E_FILES)
)


def pytest_addoption(parser):
    parser.addoption("--headless", action="store_true", default=False)


def pytest_generate_tests(metafunc):
    option_value = metafunc.config.option.headless
    if "headless" in metafunc.fixturenames and option_value is not None:
        metafunc.parametrize("headless", [option_value])
