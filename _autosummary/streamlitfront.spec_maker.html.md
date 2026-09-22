# streamlitfront.spec_maker

The streamlit spec maker — front’s `SpecMakerBase` bound to streamlit elements.

Provides the default convention mapping front element roles to the concrete
streamlit element classes from [`streamlitfront.elements`](streamlitfront.elements.html.md#module-streamlitfront.elements).

### Classes

| [`SpecMaker`](#streamlitfront.spec_maker.SpecMaker)()   | Concrete implementation of front.spec_maker_base.SpecMakerBase for streamlitfront.   |
|----------------------------------------------------------------|--------------------------------------------------------------------------------------|

### *class* streamlitfront.spec_maker.SpecMaker

Bases: `SpecMakerBase`

Concrete implementation of front.spec_maker_base.SpecMakerBase for
streamlitfront.

```pycon
>>> spec_maker = SpecMaker()
>>> spec = spec_maker.mk_spec({})
>>>
>>> spec.app_spec
{'title': 'My Streamlit Front Application'}
>>> assert spec.obj_spec
>>> assert spec.rendering_spec
```
