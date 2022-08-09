from meshed.dag import DAG
from front import APP_KEY, RENDERING_KEY, ELEMENT_KEY, NAME_KEY

from streamlitfront.examples.util import Graph
from streamlitfront.base import mk_app


def b(a: int):
    return 2 ** a


def d(c: int):
    return 10 - (5 ** c)


def result(b, d):
    return b * d


dag = DAG((b, d, result))

if __name__ == '__main__':
    # Have special element to indicate removal of field in recursive mapping merge

    app = mk_app(
        [dag],
        config={
            APP_KEY: {'title': 'DAG App'},
            RENDERING_KEY: {
                DAG: {
                    # Here, we add a new home made element. Note that this "Graph" element
                    # is not part of streamlitfront (defined in the "examples" module).
                    # Yet, it can be renderized by just referencing it in the configuration
                    # along with its parameters.
                    # You can do exactly the same at every level of the tree by defining
                    # your own elements and include them at the right place in the configuration.
                    'graph': {
                        ELEMENT_KEY: Graph,
                        NAME_KEY: 'Flow',
                        'use_container_width': True,
                    },
                    'description': {'content': ''},
                }
            },
        },
    )
    app()
