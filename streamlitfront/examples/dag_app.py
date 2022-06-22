from distutils.command.config import config

from streamlitfront.base import mk_app
from front.elements import INT_INPUT_SLIDER_COMPONENT
from meshed.dag import DAG


def b(a: int):
    return 2 ** a


def d(c: int):
    return 10 - (5 ** c)


def result(b, d):
    return b * d


dag = DAG((b, d, result))


app = mk_app(
    [dag],
    config={
        'app': {'title': 'My app'},
        # "rendering": {
        #     "dag": {
        #         'execution': {
        #             "inputs": {
        #                 "c": {
        #                     "component": INT_INPUT_SLIDER_COMPONENT,
        #                 }
        #             },
        #         }
        #     }
        # },
    },
)
app()
