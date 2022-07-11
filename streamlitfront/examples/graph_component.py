import streamlit as st
from meshed import DAG
from front.types import FrontElementName
from front.elements import FrontComponentBase


class Graph(FrontComponentBase):
    def __init__(
        self, obj: DAG, name: FrontElementName = None, use_container_width: bool = False
    ):
        super().__init__(obj=obj, name=name)
        self.use_container_width = use_container_width

    def render(self):
        with st.expander(self.name, True):
            dag: DAG = self.obj
            st.graphviz_chart(
                figure_or_dot=dag.dot_digraph(),
                use_container_width=self.use_container_width,
            )
