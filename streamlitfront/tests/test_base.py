import pytest
from streamlitfront.base import func_to_page_name


def double_func(x: int) -> int:
    return 2 * x


def test_func_to_page_name():
    result = func_to_page_name(double_func)
    expected = 'Double Func'
    assert result == expected
