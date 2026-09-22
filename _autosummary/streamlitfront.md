# streamlitfront

Dispatching python functions as webservices, docker containers, and GUIs

Consider these three functions:

```pycon
>>> def foo(a: int = 0, b: int = 0, c=0):
...     'This is foo. It computes something'
...     return (a * b) + c
>>> def bar(x, greeting='hello'):
...     'bar greets its input'
...     return f'{greeting} {x}'
>>> def confuser(a: int = 0, x: float = 3.14):
...     return (a ** 2) * x
```

Doing this:

```pycon
>>> from streamlitfront import dispatch_funcs
>>> app = dispatch_funcs([foo, bar, confuser])
```

Gets you a deployable app that allows the user to operate with these three functions.
You simply have to do:

```pycon
>>> app()
```

to launch a server that will serve the app.

The ellipses (`...`) are there to indicate that we may want to specify particulars
(convention and configurations).

### Modules

| [`base`](streamlitfront.base.md#module-streamlitfront.base)                         | Base for UI generation                                                                      |
|----------------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------|
| [`data_binding`](streamlitfront.data_binding.md#module-streamlitfront.data_binding)         | Streamlit-backed data binding — wires front's `BoundData` / `Binder` to `st.session_state`. |
| [`elements`](streamlitfront.elements.md#module-streamlitfront.elements)                 |                                                                                             |
| [`page_funcs`](streamlitfront.page_funcs.md#module-streamlitfront.page_funcs)             | Functions to create pages                                                                   |
| [`pydantic_widgets`](streamlitfront.pydantic_widgets.md#module-streamlitfront.pydantic_widgets) | Native-Streamlit rendering of pydantic v2 models — input forms and output.                  |
| [`run_app`](streamlitfront.run_app.md#module-streamlitfront.run_app)                   | Launch a streamlit app from a set of functions — the `run_app` entry point.                 |
| [`session_state`](streamlitfront.session_state.md#module-streamlitfront.session_state)       | Session state management                                                                    |
| [`spec_maker`](streamlitfront.spec_maker.md#module-streamlitfront.spec_maker)             | The streamlit spec maker — front's `SpecMakerBase` bound to streamlit elements.             |
| [`tools`](streamlitfront.tools.md#module-streamlitfront.tools)                       | Tools made with streamlitfront                                                              |
| [`util`](streamlitfront.util.md#module-streamlitfront.util)                         | Utils                                                                                       |
