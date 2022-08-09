from dataclasses import dataclass
from pathlib import Path
from typing import List, Union
from meshed import DAG
from collections.abc import Callable
from front import APP_KEY, RENDERING_KEY, ELEMENT_KEY
from front.types import Map
from front.elements import InputBase
from front.util import normalize_map
from know.scrap.data_prep_box import mall

from streamlitfront.base import mk_app
from streamlitfront.elements.js import mk_element_factory


def execute_pipe(pipe):
    pass


ItemTemplate = Union[Map, Path]


@dataclass
class MultiSelect(InputBase):
    options: Map = None
    item_template: ItemTemplate = None

    def __post_init__(self):
        super().__post_init__()
        self.options = normalize_map(self.options)
        self.item_template = normalize_map(self.item_template)
        if isinstance(self.item_template, Path):
            with self.item_template.open() as f:
                self.item_template = f.read()

    def render(self):
        st_multiselect = mk_element_factory('st_multiselect')
        value = st_multiselect(options=self.options, item_template=self.item_template)
        return value


if __name__ == '__main__':
    app = mk_app(
        [execute_pipe],
        config={
            APP_KEY: {'title': 'Pipeline Maker'},
            RENDERING_KEY: {
                Callable: {
                    'execution': {
                        'inputs': {
                            'pipe': {
                                ELEMENT_KEY: MultiSelect,
                                'options': [
                                    {'value': 'blue', 'name': 'Blue'},
                                    {'value': 'white', 'name': 'White'},
                                    {'value': 'red', 'name': 'Red'},
                                ],
                                'item_template': '''
                                    <div>
                                        <strong>{name} &#128512;</strong>
                                    </div>
                                ''',
                            }
                        }
                    }
                }
            },
        },
    )
    app()
