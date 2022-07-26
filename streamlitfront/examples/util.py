from dataclasses import dataclass
from functools import partial
import streamlit as st
from meshed import DAG
from front.types import FrontElementName
from front.elements import FrontComponentBase

from streamlitfront.elements.elements import TextSection


@dataclass
class Graph(FrontComponentBase):
    use_container_width: bool = False

    def render(self):
        with st.expander(self.name, True):
            dag: DAG = self.obj
            st.graphviz_chart(
                figure_or_dot=dag.dot_digraph(),
                use_container_width=self.use_container_width,
            )


def get_code_of_current_file():
    with open(__file__, 'r') as f:
        return f.read()


SourceCodeSection = partial(
    TextSection,
    name='Source Code',
    kind='code',
    language='python',
    content=get_code_of_current_file(),
)
