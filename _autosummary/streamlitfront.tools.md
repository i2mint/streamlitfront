# streamlitfront.tools

Tools made with streamlitfront

### Module Attributes

| [`Rules`](#streamlitfront.tools.Rules)   | typical use is to define rules and apply to objs like so   |
|----------------------------------------------------------|------------------------------------------------------------|

### Functions

| [`alt_mk_render_keys`](#streamlitfront.tools.alt_mk_render_keys)(objs, render_keys, resolver)   | Make a static render_keys that has a one-to-one relationship with objects             |
|----------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------|
| `app_maker`(objs[, config, convention, ...])                                                       |                                                                                       |
| `cond_then`(obj, rules)                                                                            |                                                                                       |
| [`first_element_matching_type`](#streamlitfront.tools.first_element_matching_type)(obj, types)           | returns the first type found that obj is an instance of                               |
| `html_img_wrap`(output)                                                                            |                                                                                       |
| `html_img_wrap_w_output_display`(output)                                                           |                                                                                       |
| `identity`(x)                                                                                      |                                                                                       |
| `if_feature_then_feature`(feature, cond, then, obj)                                                |                                                                                       |
| `if_feature_then_feature_and_obj`(feature, ...)                                                    |                                                                                       |
| `if_feature_then_obj`(feature, cond, then, obj)                                                    |                                                                                       |
| [`if_then`](#streamlitfront.tools.if_then)(cond, then, obj)                          | Intent is to be used with `functools.partial`, `map` and `itertools.chain`            |
| [`lines_to_html_paragraphs`](#streamlitfront.tools.lines_to_html_paragraphs)(output)                  | Converts a string with newlines to a string with html paragraphs                      |
| `mk_output_renderer`(\*output_trans[, name])                                                       |                                                                                       |
| [`mk_render_keys`](#streamlitfront.tools.mk_render_keys)(objs, render_keys[, ...])          | Make a static render_keys that has a one-to-one relationship with objects             |
| [`mk_specs`](#streamlitfront.tools.mk_specs)(objs, configs)                           | Make a static configs that has a one-to-one relationship with objects                 |
| [`mk_target_render_keys_func`](#streamlitfront.tools.mk_target_render_keys_func)()                      | Will use mk_find_render_keys to make a function equivalent to target_render_keys_func |
| [`render_edits`](#streamlitfront.tools.render_edits)(render_key_edits)                    | Convert render_key_edits to edits for dol.paths.apply_edits                           |
| `render_edits_gen`(render_key[, output_trans, ...])                                                |                                                                                       |
| `render_html`(output)                                                                              |                                                                                       |
| `rule1`(obj, render_keys)                                                                          |                                                                                       |
| `rule2`(obj, render_keys)                                                                          |                                                                                       |
| `rule3`(obj, render_keys)                                                                          |                                                                                       |
| [`rule_applier`](#streamlitfront.tools.rule_applier)(obj, rules, render_keys[, sentinel]) | Applies rules to obj and returns the first non-sentinel value                         |
| `target_render_keys_func`(obj, render_keys)                                                        |                                                                                       |
| `text_to_html`(output)                                                                             |                                                                                       |
| `trans_output`(config, key, output_trans)                                                          |                                                                                       |
| `validate_config`(configs, funcs, \*[, ...])                                                       |                                                                                       |

### Classes

| `ConditionalTrans`()   |    |
|------------------------|----|

### streamlitfront.tools.Rules

typical use is to define rules and apply to objs like so

```text
from functools import partial
singular_find_render_keys = partial(mk_find_render_keys, rules=rules)  # fix rules
find_render_keys = partial(map, singular_find_render_keys)  # apply to iterable
```

alias of [`Iterable`](https://docs.python.org/3/library/collections.abc.html#collections.abc.Iterable)[[`tuple`](https://docs.python.org/3/builtins/stdtypes.html#tuple)[[`Callable`](https://docs.python.org/3/library/collections.abc.html#collections.abc.Callable)[[`Obj`], [`bool`](https://docs.python.org/3/builtins/functions.html#bool)], [`Callable`](https://docs.python.org/3/library/collections.abc.html#collections.abc.Callable)[[`Obj`], `Output`]]]

### streamlitfront.tools.alt_mk_render_keys(objs, render_keys, resolver)

Make a static render_keys that has a one-to-one relationship with objects

# >>> find_render_keys = lambda objs, render_keys:
# >>> dict(mk_render_keys([1, 2, 3], {1: ‘a’, 2: ‘b’, 3: ‘c’}))
# {1: ‘a’, 2: ‘b’, 3: ‘c’}

### streamlitfront.tools.first_element_matching_type(obj, types)

returns the first type found that obj is an instance of

### streamlitfront.tools.if_then(cond, then, obj)

Intent is to be used with `functools.partial`, `map` and `itertools.chain`

```pycon
>>> from functools import partial
>>> from itertools import chain
>>> my_if_then = partial(if_then, lambda x: x % 2 == 0, lambda x: x * 2)
>>> f = lambda x: chain.from_iterable(map(my_if_then, x))
>>> next(f([1, 2, 3, 4]))
4
>>> list(f([1, 2, 3, 4]))  # get all matches
[4, 8]
```

### streamlitfront.tools.lines_to_html_paragraphs(output)

Converts a string with newlines to a string with html paragraphs

```pycon
>>> lines_to_html_paragraphs('hello\nworld')
'<p>hello</p>\n<p>world</p>'
```

### streamlitfront.tools.mk_render_keys(objs, render_keys, find_render_keys=<function \_find_render_keys>)

Make a static render_keys that has a one-to-one relationship with objects

# >>> find_render_keys = lambda objs, render_keys:
# >>> dict(mk_render_keys([1, 2, 3], {1: ‘a’, 2: ‘b’, 3: ‘c’}))
# {1: ‘a’, 2: ‘b’, 3: ‘c’}

### streamlitfront.tools.mk_specs(objs, configs)

Make a static configs that has a one-to-one relationship with objects

### streamlitfront.tools.mk_target_render_keys_func()

Will use mk_find_render_keys to make a function equivalent to
target_render_keys_func

### streamlitfront.tools.render_edits(render_key_edits)

Convert render_key_edits to edits for dol.paths.apply_edits

### streamlitfront.tools.rule_applier(obj, rules, render_keys, sentinel=None)

Applies rules to obj and returns the first non-sentinel value
