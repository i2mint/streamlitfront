import os
import streamlit.components.v1 as components


def mk_element_factory(element_name):
    parent_dir = os.path.dirname(os.path.abspath(__file__))
    build_dir = os.path.join(parent_dir, element_name)
    return components.declare_component(element_name, path=build_dir)
