from functools import partial
from front import BoundData as BoundDataBase
import streamlit as st
# from i2.util import insert_name_based_objects_in_scope

BoundData = partial(BoundDataBase, state=st.session_state)

# create_bound_data = partial(
#     insert_name_based_objects_in_scope,
#     factory=BoundData, scope=globals()
# )
