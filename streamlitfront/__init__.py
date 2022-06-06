"""
Dispatching python functions as webservices, docker containers, and GUIs

Consider these three functions:

>>> def foo(a: int = 0, b: int = 0, c=0):
...     'This is foo. It computes something'
...     return (a * b) + c
>>> def bar(x, greeting='hello'):
...     'bar greets its input'
...     return f'{greeting} {x}'
>>> def confuser(a: int = 0, x: float = 3.14):
...     return (a ** 2) * x


Doing this:

>>> from streamlitfront import dispatch_funcs
>>> app = dispatch_funcs([foo, bar, confuser])

Gets you a deployable app that allows the user to operate with these three functions.
You simply have to do:

>>> app()  # doctest: +SKIP

to launch a server that will serve the app.

The ellipses (`...`) are there to indicate that we may want to specify particulars
(convention and configurations).

"""


from streamlitfront.base import dispatch_funcs, mk_app
from streamlitfront.util import run_streamlit, data_files
