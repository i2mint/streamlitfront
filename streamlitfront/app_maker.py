from typing import Callable
from front.app_maker_base import AppMakerBase
from front.elements import FrontElementBase

from streamlitfront.elements.tree_maker import ElementTreeMaker


class AppMaker(AppMakerBase):
    """App maker class for streamlitfront. Defines ``ElementTreeMaker`` as default tree
    maker
    """

    def __init__(self, element_tree_maker_factory: Callable = ElementTreeMaker):
        super().__init__(element_tree_maker_factory)
