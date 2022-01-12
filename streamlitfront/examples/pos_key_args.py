import os
from typing import Dict, Iterable
import pandas as pd


def add_ints(*nums_to_add: Iterable[int]):
    return sum(nums_to_add)


def add_floats(*nums_to_add: Iterable[float]):
    return sum(nums_to_add)


def add_strs(*strs_to_add: Iterable[str]):
    return ' '.join(strs_to_add)


def add_bools(*bools_to_add: Iterable[bool]):
    return sum(list(map(int, bools_to_add)))


def make_a_table_of_ints(col_name: str = 'integers', **keys_and_values: Dict[str, int]):
    return pd.Series(data=keys_and_values, name=col_name)


def make_a_table_of_floats(
    col_name: str = 'floats', **keys_and_values: Dict[str, float]
):
    return pd.Series(data=keys_and_values, name=col_name)


def make_a_table_of_strs(col_name: str = 'strings', **keys_and_values: Dict[str, str]):
    return pd.Series(data=keys_and_values, name=col_name)


def make_a_table_of_bools(
    col_name: str = 'booleans', **keys_and_values: Dict[str, bool]
):
    return pd.Series(data=keys_and_values, name=col_name)


funcs = [
    add_ints,
    add_floats,
    add_strs,
    add_bools,
    make_a_table_of_ints,
    make_a_table_of_floats,
    make_a_table_of_strs,
    make_a_table_of_bools,
]

if __name__ == '__main__':
    from streamlitfront.base import dispatch_funcs
    from streamlitfront.page_funcs import ArgsPageFunc

    print('file: {}'.format(os.path.realpath(__file__)))

    app = dispatch_funcs(funcs, configs={'page_factory': ArgsPageFunc})

    app()
