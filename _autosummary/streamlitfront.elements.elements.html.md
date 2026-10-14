# streamlitfront.elements.elements

Here are implemented the elements for streamlitfront.

Not the use of the `implement_component` function to create a class that implements a
specific abstract elements class defined in front.

### Functions

| [`implement_input_component`](#streamlitfront.elements.elements.implement_input_component)(base_cls, ...)   | `implement_component` for the input widgets, with `on_change` wired as a widget callback.   |
|---------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------|

### Classes

| [`App`](#streamlitfront.elements.elements.App)([obj, name, display])                         | Implementation of the app root container for streamlitfront.   |
|----------------------------------------------------------------------------------------------------|----------------------------------------------------------------|
| [`AudioRecorder`](#streamlitfront.elements.elements.AudioRecorder)([obj, name, display, ...])          |                                                                |
| [`ExecSection`](#streamlitfront.elements.elements.ExecSection)(obj, inputs, output[, name, ...])     |                                                                |
| [`FileUploader`](#streamlitfront.elements.elements.FileUploader)([obj, name, display, ...])           |                                                                |
| [`HiddenOutput`](#streamlitfront.elements.elements.HiddenOutput)([obj, name, display])                |                                                                |
| [`KwargsInput`](#streamlitfront.elements.elements.KwargsInput)([obj, name, display, input_key, ...]) |                                                                |
| [`MultiSelectorBase`](#streamlitfront.elements.elements.MultiSelectorBase)([obj, name, display, ...])      | A selector whose view value is a *list* of options.            |
| [`MultiSourceInput`](#streamlitfront.elements.elements.MultiSourceInput)([obj, name, display, ...])       |                                                                |
| [`Section`](#streamlitfront.elements.elements.Section)([obj, name, display])                     |                                                                |
| [`SuccessFailureNotification`](#streamlitfront.elements.elements.SuccessFailureNotification)([obj, name, ...])      |                                                                |
| [`SuccessNotification`](#streamlitfront.elements.elements.SuccessNotification)([obj, name, display, ...])    |                                                                |
| [`TextOutput`](#streamlitfront.elements.elements.TextOutput)([obj, name, display])                  |                                                                |
| [`TextSection`](#streamlitfront.elements.elements.TextSection)(content[, kind, obj, name])           |                                                                |
| [`View`](#streamlitfront.elements.elements.View)([obj, name, display])                        |                                                                |

### *class* streamlitfront.elements.elements.App(obj=None, name=None, display=True, \*\*kwargs)

Bases: `FrontContainerBase`

Implementation of the app root container for streamlitfront.

#### render()

Render the element with the concrete UI framework; must be overridden.

### *class* streamlitfront.elements.elements.AudioRecorder(obj=None, name=None, display=True, input_key=None, value=ValueNotSet, on_value_change=None, bound_data_factory=None, is_noneable=False, disabled=False)

Bases: `InputBase`

#### render()

Render the element with the concrete UI framework; must be overridden.

### *class* streamlitfront.elements.elements.ExecSection(obj, inputs, output, name=None, display=True, auto_submit=False, on_submit=None, use_expander=True, submit_button_label='Submit', authentification=False)

Bases: `ExecContainerBase`

#### render()

Render the element with the concrete UI framework; must be overridden.

### *class* streamlitfront.elements.elements.FileUploader(obj=None, name=None, display=True, input_key=None, value=ValueNotSet, on_value_change=None, bound_data_factory=None, is_noneable=False, disabled=False, type=None, accept_multiple_files=False, clear_after_submit=True, display_label=True)

Bases: `FileUploaderBase`

#### clear()

Empty the uploader, now and on the following runs.

Streamlit keeps an uploader’s files for as long as its widget key lives and
offers no other way to empty it. So: move to a new key, and draw a fresh
uploader in the slot of the old one right away, so that this run’s output and
everything else drawn stay in place (no rerun).

#### render()

Render the element with the concrete UI framework; must be overridden.

### *class* streamlitfront.elements.elements.HiddenOutput(obj=None, name=None, display=True)

Bases: `OutputBase`

#### render()

Render the element with the concrete UI framework; must be overridden.

### *class* streamlitfront.elements.elements.KwargsInput(obj=None, name=None, display=True, input_key=None, value=ValueNotSet, on_value_change=None, bound_data_factory=None, is_noneable=False, disabled=False, inputs=None, func_sig=None)

Bases: `KwargsInputBase`

#### render()

Render the element with the concrete UI framework; must be overridden.

### *class* streamlitfront.elements.elements.MultiSelectorBase(obj=None, name=None, display=True, input_key=None, value=ValueNotSet, on_value_change=None, bound_data_factory=None, is_noneable=False, disabled=False, options=None)

Bases: `SelectorBase`

A selector whose view value is a *list* of options.

`SelectorBase.pre_render` is single-choice logic: it looks the view value up among the
options, finds no list there, and “corrects” it to the first option – calling
`on_value_change` with that one item on every render. Here the options are only resolved;
the value is the widget’s (`on_value_change` runs as its callback, with the list).

#### pre_render()

Resolve the options and pre-select the current view value (or the first option).

### *class* streamlitfront.elements.elements.MultiSourceInput(obj=None, name=None, display=True, input_key=None, value=ValueNotSet, on_value_change=None, bound_data_factory=None, is_noneable=False, disabled=False, \*\*kwargs)

Bases: `MultiSourceInputBase`

#### render()

Render the element with the concrete UI framework; must be overridden.

### *class* streamlitfront.elements.elements.Section(obj=None, name=None, display=True, \*\*kwargs)

Bases: `FrontContainerBase`

#### render()

Render the element with the concrete UI framework; must be overridden.

### *class* streamlitfront.elements.elements.SuccessFailureNotification(obj=None, name=None, display=True, success='Success!', failure='Failure!', post_render_sleep=0)

Bases: `OutputBase`

#### render()

Render the element with the concrete UI framework; must be overridden.

### *class* streamlitfront.elements.elements.SuccessNotification(obj=None, name=None, display=True, message='Success!')

Bases: `OutputBase`

#### render()

Render the element with the concrete UI framework; must be overridden.

### *class* streamlitfront.elements.elements.TextOutput(obj=None, name=None, display=True)

Bases: `OutputBase`

#### render()

Render the element with the concrete UI framework; must be overridden.

### *class* streamlitfront.elements.elements.TextSection(content, kind='text', obj=None, name=None, \*\*kwargs)

Bases: `TextSectionBase`

#### render()

Render the element with the concrete UI framework; must be overridden.

### *class* streamlitfront.elements.elements.View(obj=None, name=None, display=True, \*\*kwargs)

Bases: `FrontContainerBase`

#### render()

Render the element with the concrete UI framework; must be overridden.

### streamlitfront.elements.elements.implement_input_component(base_cls, component_factory, \*\*input_mapping)

`implement_component` for the input widgets, with `on_change` wired as a widget callback.

`implement_component` *calls* every callable attribute it forwards, and `on_change` is a
method: left alone, it would run during the render (before the widget even exists) and
streamlit would get `None`. So an input’s `on_value_change` would only take effect on the
*next* run, and a dependent input built from the state it sets needed a second interaction
(i2mint/streamlitfront#7). Here the widget gets `on_change` itself, so streamlit runs it
before the rerun the interaction triggers.
