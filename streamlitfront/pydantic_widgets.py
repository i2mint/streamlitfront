"""Native-Streamlit rendering of pydantic v2 models — input forms and output.

A minimal, self-contained replacement for the small subset of the
(unmaintained, pydantic-v1-only) ``streamlit_pydantic`` package that
streamlitfront actually used.

``streamlit_pydantic`` 0.6.0 — its last release — imports
``pydantic.BaseSettings``, which was removed in pydantic v2, and there is no
v2-compatible release. Rather than pin the whole ecosystem to pydantic v1,
the three helpers used by streamlitfront are reimplemented here against the
pydantic v2 API (``model.model_fields``) and native ``streamlit`` widgets.

Public API (drop-in for the old ``import streamlit_pydantic as sp``):

- :func:`pydantic_input` — render one widget per model field, return a
  validated model instance (or ``None`` on validation error).
- :func:`pydantic_form` — same, wrapped in an ``st.form`` with a submit
  button; returns the instance on submit, ``None`` otherwise.
- :func:`pydantic_output` — render a model instance.
"""

from typing import Optional, Type, Union, get_args, get_origin

import streamlit as st
from pydantic import BaseModel, ValidationError


def _unwrap_optional(annotation):
    """Return ``X`` for an ``Optional[X]`` / ``Union[X, None]`` annotation, else the annotation."""
    if get_origin(annotation) is Union:
        non_none = [a for a in get_args(annotation) if a is not type(None)]
        if len(non_none) == 1:
            return non_none[0]
    return annotation


def _widget_for_field(field_name, field_info, *, key):
    """Render the Streamlit widget that best matches a pydantic field's type."""
    annotation = _unwrap_optional(field_info.annotation)
    has_default = not field_info.is_required()
    default = field_info.default if has_default else None

    if annotation is bool:
        return st.checkbox(field_name, value=bool(default) or False, key=key)
    if annotation is int:
        return st.number_input(
            field_name, value=int(default) if default is not None else 0, step=1, key=key
        )
    if annotation is float:
        return st.number_input(
            field_name, value=float(default) if default is not None else 0.0, key=key
        )
    # str, Any, and everything else fall back to a text field.
    return st.text_input(
        field_name, value=str(default) if default is not None else "", key=key
    )


def _collect_field_values(model: Type[BaseModel], *, key: str) -> dict:
    """Render a widget per model field and return ``{field_name: widget_value}``."""
    return {
        name: _widget_for_field(name, info, key=f"{key}_{name}")
        for name, info in model.model_fields.items()
    }


def _instantiate(model: Type[BaseModel], values: dict) -> Optional[BaseModel]:
    """Build a model instance from collected values, surfacing errors via ``st.error``."""
    try:
        return model(**values)
    except ValidationError as error:
        st.error(str(error))
        return None


def pydantic_input(key: str, model: Type[BaseModel]) -> Optional[BaseModel]:
    """Render an input widget per field of ``model``; return a validated instance.

    Returns ``None`` if the current widget values fail validation.
    """
    values = _collect_field_values(model, key=key)
    return _instantiate(model, values)


def pydantic_form(
    key: str, model: Type[BaseModel], *, submit_label: str = "Submit"
) -> Optional[BaseModel]:
    """Like :func:`pydantic_input`, wrapped in an ``st.form`` with a submit button.

    Returns the validated model instance once the form is submitted, otherwise
    ``None`` (so callers can guard with ``if data:``).
    """
    with st.form(key=key):
        values = _collect_field_values(model, key=key)
        submitted = st.form_submit_button(submit_label)
    if not submitted:
        return None
    return _instantiate(model, values)


def pydantic_output(instance: BaseModel) -> None:
    """Render a pydantic model instance as JSON."""
    st.json(instance.model_dump())
