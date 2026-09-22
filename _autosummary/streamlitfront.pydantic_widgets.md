# streamlitfront.pydantic_widgets

Native-Streamlit rendering of pydantic v2 models — input forms and output.

A minimal, self-contained replacement for the small subset of the
(unmaintained, pydantic-v1-only) `streamlit_pydantic` package that
streamlitfront actually used.

`streamlit_pydantic` 0.6.0 — its last release — imports
`pydantic.BaseSettings`, which was removed in pydantic v2, and there is no
v2-compatible release. Rather than pin the whole ecosystem to pydantic v1,
the three helpers used by streamlitfront are reimplemented here against the
pydantic v2 API (`model.model_fields`) and native `streamlit` widgets.

Public API (drop-in for the old `import streamlit_pydantic as sp`):

- [`pydantic_input()`](#streamlitfront.pydantic_widgets.pydantic_input) — render one widget per model field, return a
  validated model instance (or `None` on validation error).
- [`pydantic_form()`](#streamlitfront.pydantic_widgets.pydantic_form) — same, wrapped in an `st.form` with a submit
  button; returns the instance on submit, `None` otherwise.
- [`pydantic_output()`](#streamlitfront.pydantic_widgets.pydantic_output) — render a model instance.

### Functions

| [`pydantic_form`](#streamlitfront.pydantic_widgets.pydantic_form)(key, model, \*[, submit_label])   | Like [`pydantic_input()`](#streamlitfront.pydantic_widgets.pydantic_input), wrapped in an `st.form` with a submit button.   |
|--------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------|
| [`pydantic_input`](#streamlitfront.pydantic_widgets.pydantic_input)(key, model)                      | Render an input widget per field of `model`; return a validated instance.                                               |
| [`pydantic_output`](#streamlitfront.pydantic_widgets.pydantic_output)(instance)                       | Render a pydantic model instance as JSON.                                                                               |

### streamlitfront.pydantic_widgets.pydantic_form(key, model, , submit_label='Submit')

Like [`pydantic_input()`](#streamlitfront.pydantic_widgets.pydantic_input), wrapped in an `st.form` with a submit button.

Returns the validated model instance once the form is submitted, otherwise
`None` (so callers can guard with `if data:`).

* **Return type:**
  [`Optional`](https://docs.python.org/3/library/typing.html#typing.Optional)[`BaseModel`]

### streamlitfront.pydantic_widgets.pydantic_input(key, model)

Render an input widget per field of `model`; return a validated instance.

Returns `None` if the current widget values fail validation.

* **Return type:**
  [`Optional`](https://docs.python.org/3/library/typing.html#typing.Optional)[`BaseModel`]

### streamlitfront.pydantic_widgets.pydantic_output(instance)

Render a pydantic model instance as JSON.

* **Return type:**
  [`None`](https://docs.python.org/3/builtins/constants.html#None)
