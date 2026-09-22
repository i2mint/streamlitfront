# streamlitfront.elements.elements

Here are implemented the elements for streamlitfront.

Not the use of the `implement_component` function to create a class that implements a
specific abstract elements class defined in front.

### Classes

| [`App`](#streamlitfront.elements.elements.App)([obj, name, display])                         | Implementation of the app root container for streamlitfront.   |
|----------------------------------------------------------------------------------------------------|----------------------------------------------------------------|
| [`AudioRecorder`](#streamlitfront.elements.elements.AudioRecorder)([obj, name, display, ...])          |                                                                |
| [`ExecSection`](#streamlitfront.elements.elements.ExecSection)(obj, inputs, output[, name, ...])     |                                                                |
| [`FileUploader`](#streamlitfront.elements.elements.FileUploader)([obj, name, display, ...])           |                                                                |
| [`HiddenOutput`](#streamlitfront.elements.elements.HiddenOutput)([obj, name, display])                |                                                                |
| [`KwargsInput`](#streamlitfront.elements.elements.KwargsInput)([obj, name, display, input_key, ...]) |                                                                |
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

### *class* streamlitfront.elements.elements.FileUploader(obj=None, name=None, display=True, input_key=None, value=ValueNotSet, on_value_change=None, bound_data_factory=None, is_noneable=False, disabled=False, type=None, accept_multiple_files=False, display_label=True)

Bases: `FileUploaderBase`

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
