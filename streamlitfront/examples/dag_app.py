from streamlitfront.base import mk_app
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
    },
)
app()
