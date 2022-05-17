from typing import Mapping
from front.elements import ElementTreeMakerBase, FrontElementBase, ContainerFlag, InputComponentFlag

from streamlitfront.elements.elements import App, FloatInput, IntInput, TextInput, FuncView


class ElementTreeMaker(ElementTreeMakerBase):
    @property
    def _component_mapping(cls) -> Mapping[InputComponentFlag, FrontElementBase]:
        return {
            InputComponentFlag.TEXT: TextInput,
            InputComponentFlag.INT: IntInput,
            InputComponentFlag.FLOAT: FloatInput,
        }

    @property
    def _container_mapping(cls) -> Mapping[ContainerFlag, FrontElementBase]:
        return {
            ContainerFlag.APP: App,
            ContainerFlag.VIEW: FuncView,
        }
