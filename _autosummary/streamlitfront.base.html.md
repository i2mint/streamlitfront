# streamlitfront.base

Base for UI generation

### Functions

| `default_hash_func`(item)                                                                         |                                                                         |
|---------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------|
| `dflt_convention`()                                                                               |                                                                         |
| [`dispatch_funcs`](#streamlitfront.base.dispatch_funcs)(funcs[, configs, convention])     | DEPRECATED! Call this function with target funcs and get an app to run. |
| `func_to_page_name`(func, \*\*kwargs)                                                             |                                                                         |
| `get_func_args_specs`(func[, ...])                                                                |                                                                         |
| [`get_pages_specs`](#streamlitfront.base.get_pages_specs)(funcs[, func_to_page_name, ...]) | Get pages specification dict                                            |
| `infer_type`(sig, name)                                                                           |                                                                         |
| [`mk_app`](#streamlitfront.base.mk_app)(objs[, config, convention])               | The entrypoint of streamlitfront.                                       |
| `pages_app`(funcs, configs)                                                                       |                                                                         |

### Classes

| `BasePageFunc`(func[, view_title])                        |    |
|-----------------------------------------------------------|----|
| `DFLT_PAGE_FACTORY`                                       |    |
| [`DfltDict`](#streamlitfront.base.DfltDict) |    |
| `SimplePageFunc`(func[, view_title])                      |    |

### *class* streamlitfront.base.DfltDict

Bases: [`dict`](https://docs.python.org/3/builtins/stdtypes.html#dict)

### streamlitfront.base.dispatch_funcs(funcs, configs=None, convention=<function dflt_convention>)

DEPRECATED!
Call this function with target funcs and get an app to run.

* **Return type:**
  [`Callable`](https://docs.python.org/3/library/collections.abc.html#collections.abc.Callable)

### streamlitfront.base.get_pages_specs(funcs, func_to_page_name=<function func_to_page_name>, page_factory=<class 'streamlitfront.base.SimplePageFunc'>, \*\*configs)

Get pages specification dict

* **Return type:**
  [`Mapping`](https://docs.python.org/3/library/collections.abc.html#collections.abc.Mapping)[[`str`](https://docs.python.org/3/builtins/stdtypes.html#str), [`Callable`](https://docs.python.org/3/library/collections.abc.html#collections.abc.Callable)[[`_SessionState`], [`Any`](https://docs.python.org/3/library/typing.html#typing.Any)]]

### streamlitfront.base.mk_app(objs, config=None, convention=None)

The entrypoint of streamlitfront.
Call this function with target objects and get an app to run.

### Example

Render functions

First define a bunch of functions:

```pycon
>>> def foo(a: int = 1, b: int = 2, c=3):
...     return (a * b) + c
>>> def bar(x, greeting="hello"):
...     return f"{greeting} {x}"
>>> def confuser(a: int, x: float = 3.14):
...     return (a ** 2) * x
>>> funcs = [foo, bar, confuser]
```

Then make the app from these functions:

```pycon
>>> app = mk_app(funcs)
```

The default configuration for the application is defined in
`streamlitfront/spec_maker.py` and `front/spec_maker_base.py`. But you can
overwrite parts or the entire configuration by setting the `config` parameter.
The configuration is composed of three parts: app, obj and rendering.

The app configuration:
By default, the application name is “My Front Application”, but you can set the
title of the application as follow:

```pycon
>>> from front import APP_KEY
>>> config = {
...     APP_KEY: {
...         'title': 'Another application name'
...     }
... }
>>> app = mk_app(funcs, config=config)
```

The obj configuration:
You can define a wrapper to transform the initial object into an output of your
choice to be rendered:

```pycon
>>> from front.util import dflt_trans
>>> from front import OBJ_KEY
>>> def trans(objs: Iterable):
...     return dflt_trans(reversed(objs))
>>> config = {
...     OBJ_KEY: {
...         'trans': trans
...     }
... }
>>> app = mk_app(funcs, config=config)
```

The rendering configuration:
You can define the way elements are rendered in the GUI.
For instance, you can choose to render a text input instead of a number input for a
specific parameter of a specific function:

```pycon
>>> from front import ELEMENT_KEY, RENDERING_KEY
>>> from streamlitfront.elements import IntSliderInput
>>> config = {
...     RENDERING_KEY: {
...         'foo': {
...             'execution': {
...                 'inputs': {
...                     'a': {
...                         ELEMENT_KEY: IntSliderInput,
...                         'max_value': 10
...                     }
...                 }
...             }
...         }
...     }
... }
>>> app = mk_app(funcs, config=config)
```

Obviously, you can combine the three types of configuration:

```pycon
>>> config = {
...     APP_KEY: {
...         'title': 'Another application name'
...     },
...     OBJ_KEY: {
...         'trans': trans
...     },
...     RENDERING_KEY: {
...         'foo': {
...             'execution': {
...                 'inputs': {
...                     'a': {
...                         ELEMENT_KEY: IntSliderInput,
...                         'max_value': 10
...                     }
...                 }
...             }
...         }
...     }
... }
>>> app = mk_app(funcs, config=config)
```

You can also overwrite the whole configuration by setting the `convention`
parameter. Be careful though, by overwritting the default convention, you have to
make sure that all configuations are defined. Otherwise, the application would
crash or behave unexpectedly.

```pycon
>>> from collections.abc import Callable
>>> from front import NAME_KEY, DEFAULT_INPUT_KEY
>>> from streamlitfront.elements import (
...     App,
...     ExecSection,
...     FloatSliderInput,
...     IntInput,
...     TextInput,
...     TextOutput,
...     TextSection,
...     View,
... )
>>> from streamlitfront.data_binding import BoundData
>>>
>>> convention = {
...     APP_KEY: {
...         'title': 'Another application name'
...     },
...     OBJ_KEY: {
...         'trans': trans
...     },
...     RENDERING_KEY: {
...         ELEMENT_KEY: App,
...         Callable: {
...             ELEMENT_KEY: View,
...             'description': {
...                 ELEMENT_KEY: TextSection,
...                 NAME_KEY: 'Description',
...                 'content': lambda o: o.__doc__,
...             },
...             'execution': {
...                 ELEMENT_KEY: ExecSection,
...                 NAME_KEY: 'Execution',
...                 'inputs': {
...                     int: {ELEMENT_KEY: IntInput,},
...                     float: {
...                         ELEMENT_KEY: FloatSliderInput,
...                         'format': '%.2f',
...                         'step': 0.01,
...                     },
...                     Any: {ELEMENT_KEY: TextInput,},
...                     DEFAULT_INPUT_KEY: {
...                         NAME_KEY: lambda p: p.name,
...                         'bound_data_factory': BoundData
...                     }
...                 },
...                 'output': {
...                     ELEMENT_KEY: TextOutput,
...                     NAME_KEY: 'Output',
...                 }
...             }
...         }
...     }
... }
>>> app = mk_app(funcs, convention=convention)
```

You can also add new elements to the GUI by defining it first then add it to the
configuration. In the following example, we display the dot graph of a DAG using
our own implementation of the component. It is then referenced in the configuration
with the parameters to intantiate it.

```pycon
>>> from meshed import DAG
>>> from front.types import FrontElementName
>>> from front.elements import FrontComponentBase
>>>
>>> def b(a: int):
...     return 2 ** a
>>> def d(c: int):
...     return 10 - (5 ** c)
>>> def result(b, d):
...     return b * d
>>> dag = DAG((b, d, result))
>>>
>>> class Graph(FrontComponentBase):
...     def __init__(
...         self,
...         obj: DAG,
...         name: FrontElementName = None,
...         use_container_width: bool = False
...     ):
...         super().__init__(obj=obj, name=name)
...         self.use_container_width = use_container_width
...
...     def render(self):
...         with st.expander(self.name, True):
...             dag: DAG = self.obj
...             st.graphviz_chart(
...                 figure_or_dot=dag.dot_digraph(),
...                 use_container_width=self.use_container_width
...             )
>>>
>>> config = {
...     APP_KEY: {'title': 'DAG App'},
...     RENDERING_KEY: {
...         DAG: {
...             'graph': {
...                 ELEMENT_KEY: Graph,
...                 NAME_KEY: 'Flow',
...                 'use_container_width': True
...             }
...         }
...     }
... }
>>> app = mk_app([dag], config=config)
```

* **Parameters:**
  * **objs** (*Map*) – The target objects to crender in the streamlit application.
  * **config** (`Union`[[`None`](https://docs.python.org/3/builtins/constants.html#None), [`Mapping`](https://docs.python.org/3/library/collections.abc.html#collections.abc.Mapping), [`Callable`](https://docs.python.org/3/library/collections.abc.html#collections.abc.Callable)[[], [`Mapping`](https://docs.python.org/3/library/collections.abc.html#collections.abc.Mapping)]]) – The configuration object for the application. Overwrites the
    convention for every value present in the configuration object. See above for more
    details.
  * **config** – The convention object for the application. Defines the default
    configuration. See above for more details.
