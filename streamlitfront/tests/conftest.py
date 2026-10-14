"""Pytest configuration for the in-package tests.

``common.py`` and ``use_case_test_old.py`` drive a real browser through selenium; they
cannot even be imported without the optional e2e dependencies (``tests/test_requirements.txt``),
so they are left out of collection when those are missing instead of breaking it.
"""

from importlib.util import find_spec

_E2E_MODULES = ("selenium", "webdriver_manager", "strand", "dill", "front")
_E2E_FILES = ("common.py", "use_case_test_old.py")

collect_ignore = (
    []
    if all(find_spec(name) for name in _E2E_MODULES)
    else list(_E2E_FILES)
)


def pytest_addoption(parser):
    parser.addoption("--headless", action="store_true", default=False)


def pytest_generate_tests(metafunc):
    option_value = metafunc.config.option.headless
    if "headless" in metafunc.fixturenames and option_value is not None:
        metafunc.parametrize("headless", [option_value])
