from functools import partial
from front.types import BoundData as BoundDataBase
import streamlit as st


BoundData = partial(BoundDataBase, state=st.session_state)
