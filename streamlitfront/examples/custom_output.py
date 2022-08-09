import streamlit as st
from collections.abc import Callable
from dataclasses import dataclass
from front import APP_KEY, RENDERING_KEY, ELEMENT_KEY, NAME_KEY
from front.elements import OutputBase

from streamlitfront.base import mk_app
from streamlitfront.examples.util import SourceCodeSection


def foo(a: int = 1, b: int = 2, c=3):
    """This is foo. It computes something"""
    return (a * b) + c


@dataclass
class HitTheOutputValue(OutputBase):
    value_to_hit: int = 100
    margin: int = 20

    def render(self):
        template = f'{self.name}: {self.output}. {{0}}'
        if self.output == self.value_to_hit:
            st.success(template.format('You hit it! Congratulations!'))
            st.balloons()
        elif abs(self.output - self.value_to_hit) <= self.margin:
            st.warning(template.format("You're warm..."))
        else:
            st.info(template.format("It's freezing here."))
            st.snow()


if __name__ == '__main__':
    app = mk_app(
        [foo],
        config={
            APP_KEY: {'title': 'My Custom Output'},
            RENDERING_KEY: {
                'foo': {
                    NAME_KEY: 'Hit the value',
                    'description': {
                        'content': '''
                            Try to hit the secret output value by playing with the inputs. \n 
                            Hint: It is the answer to the ultimate question of life, the universe, and everything.
                        ''',
                    },
                    'execution': {
                        'output': {
                            ELEMENT_KEY: HitTheOutputValue,
                            'value_to_hit': 42,
                            'margin': 10,
                        },
                    },
                    'code': {ELEMENT_KEY: SourceCodeSection,},
                }
            },
        },
    )
    app()
