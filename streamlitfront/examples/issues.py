import io
import os
from py2store import ZipReader, filt_iter
import pandas as pd
import streamlit as st
from streamlitfront.session_state import _get_state

# store = state_dict[store_name]
# option = st.selectbox(message, [extra] + list(store.keys()), index=dflt_index)


class C:
    def __init__(self):
        self.val = 1

    def increment(self):
        st.write(self.val)
        self.val += 1
        return self.val


c = C()
my_incrementer = c.increment


def display_selectbox(store):
    _keys = filt_iter(store, filt=lambda k: k.endswith('.csv'))
    st.selectbox('Choose a file', list(_keys))


def dacc(zip_path: type(lambda a: a), file: str):  # file: list = []):
    s = ZipReader(zip_path)
    annots_df = pd.read_csv(io.BytesIO(s[file]))
    display_selectbox(s)
    return annots_df


def foo(state: type(_get_state()), word: str):
    return word


funcs = [my_incrementer, foo]

if __name__ == '__main__':
    from streamlitfront.base import dispatch_funcs

    print('file: {}'.format(os.path.realpath(__file__)))

    app = dispatch_funcs(funcs)

    app()
