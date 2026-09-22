# streamlitfront.util

Utils

### Functions

| [`attr_or_key`](#streamlitfront.util.attr_or_key)(obj, k)                              | Get data for `k` by doing obj.k, or obj[k] if k not an attribute of obj           |
|---------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------|
| [`attr_or_key_with_dotpaths`](#streamlitfront.util.attr_or_key_with_dotpaths)(obj, k)                | Get k-data from obj hwere k is a path of keys and attributes leading to the data. |
| [`build_element_commands`](#streamlitfront.util.build_element_commands)(name, inferred_type, ...) | Build the element factory for each argument to allow for user input               |
| [`build_element_factory`](#streamlitfront.util.build_element_factory)(name, inferred_type, ...)  | Build the element factory for each argument to allow for user input               |
| [`build_element_factory_helper`](#streamlitfront.util.build_element_factory_helper)(...)                | Helper to build the element factory for VP and VK arguments                       |
| [`build_factory`](#streamlitfront.util.build_factory)(element_factory, kind, idx)        | Build the factory for user input for VP and VK inputs                             |
| [`func_name`](#streamlitfront.util.func_name)(func)                                  | The func._\_name_\_ of a callable func, or makes and returns one if that fails.   |
| [`incremental_str_maker`](#streamlitfront.util.incremental_str_maker)([str_format])              | Make a function that will produce a (incrementally) new string at every call.     |
| [`signature_defaults`](#streamlitfront.util.signature_defaults)(sig)                          | Return `sig.defaults` without the params whose default is `i2`'s `NotSet`.        |
| `unnamed_page`()                                                                                  |                                                                                   |

### Classes

| [`Command`](#streamlitfront.util.Command)(func, \*args, \*\*kwargs)   |                                                                                                                                                                                               |
|--------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| [`NodeGetter`](#streamlitfront.util.NodeGetter)(src[, item_getter])      | A accessing nested (i.e. tree-like) data as data['a', 'b', 'c'] instead of data['a']['b']['c'] This is the base to be able to define other path-based ways to see nested data. For example::. |
| [`Objdict`](#streamlitfront.util.Objdict)                             | A dict, whose keys can be access as if they were attributes.                                                                                                                                  |

### *class* streamlitfront.util.Command(func, \*args, \*\*kwargs)

Bases: `Command`

### *class* streamlitfront.util.NodeGetter(src, item_getter=<function attr_or_key_with_dotpaths>)

Bases: [`object`](https://docs.python.org/3/builtins/functions.html#object)

A accessing nested (i.e. tree-like) data as data[‘a’, ‘b’, ‘c’]
instead of data[‘a’][‘b’][‘c’]
This is the base to be able to define other path-based ways to see nested data.
For example:

```default
data['a.b.c'.split('.')]
```

```pycon
>>> d = {
...     'a': 'simple',
...     'b': {'is': 'nested'},
...     'c': {'is': 'nested', 'and': 'has', 'a': [1, 2, 3]}
... }
>>> g = NodeGetter(d)
>>>
>>> assert g['a'] == 'simple'
>>> assert g['b', 'is'] == 'nested'
>>> assert g['c', 'a'] == [1, 2, 3]
>>> assert g['c', 'a', 1] == 2
>>>
>>> assert d['c']['a'][1] == 2  # it's to avoid accessing it this way.
>>> # But can also expand on this and do things like:
>>> assert g['b.is'.split('.')] == 'nested'
>>> assert g['c/a'.split('/')] == [1, 2, 3]
>>> # ... or subclass/wrap NodeGetter to do it automatically, given a protocol
>>>
>>> def int_if_possible(x):
...     try:
...         return int(x)
...     except ValueError:
...         return x
>>> p = lambda k: map(int_if_possible, k.split('.'))
>>> assert g[p('c.a.1')] == 2
```

### *class* streamlitfront.util.Objdict

Bases: [`dict`](https://docs.python.org/3/builtins/stdtypes.html#dict)

A dict, whose keys can be access as if they were attributes.

```pycon
>>> s = Objdict()
```

Write it as you do with attributes or dict keys,
get it as an attribute and a dict keys.

```pycon
>>> s.foo = 'bar'
>>> assert s.foo == 'bar'
>>> assert s['foo'] == 'bar'
>>> s['hello'] = 'world'
>>> assert s.hello == 'world'
>>> assert s['hello'] == 'world'
>>> hasattr(s, 'hello')
True
```

And you can still do dict stuff with it…

```pycon
>>> list(s)
['foo', 'hello']
>>> list(s.items())
[('foo', 'bar'), ('hello', 'world')]
>>> s.get('key not there', 'nope')
'nope'
>>> s.clear()
>>> assert len(s) == 0
```

#### NOTE
You can use anything that’s a valid dict key as a key

```pycon
>>> s['strings with space'] = 1
>>> s[42] = 'meaning of life'
>>> s[('tuples', 1, None)] = 'weird'
>>> list(s)
['strings with space', 42, ('tuples', 1, None)]
```

But obviously, the only ones you’ll be able to access are those that are
valid attribute names.

### streamlitfront.util.attr_or_key(obj, k)

Get data for `k` by doing obj.k, or obj[k] if k not an attribute of obj

```pycon
>>> d = {'a': 1, 2: 'b', '__class__': 'do I win?'}
>>> attr_or_key(d, 'a')
1
>>> attr_or_key(d, 2)
'b'
>>> attr_or_key(d, '__class__')
<class 'dict'>
```

That last one shows that `attr_or_key` will also look in attributes to find
the data of `k`. In fact, it looks there first, before using [k].
That’s why we got the dict type returned, and not the ‘do I win?’ string.
Because `d` has an attribute called `__class__` (like… well… all python
objects do).

### streamlitfront.util.attr_or_key_with_dotpaths(obj, k)

Get k-data from obj hwere k is a path of keys and attributes leading to the data.

```pycon
>>> attr_or_key_with_dotpaths({'a': {'b': 3}}, 'a.b')
3
```

### streamlitfront.util.build_element_commands(name, inferred_type, element_factory_for_annot, missing, dflt_element_factory)

Build the element factory for each argument to allow for user input

### streamlitfront.util.build_element_factory(name, inferred_type, element_factory_for_annot, missing, dflt_element_factory)

Build the element factory for each argument to allow for user input

### streamlitfront.util.build_element_factory_helper(element_factory_for_annot, inferred_type, missing, args)

Helper to build the element factory for VP and VK arguments

### streamlitfront.util.build_factory(element_factory, kind, idx)

Build the factory for user input for VP and VK inputs

### streamlitfront.util.func_name(func)

The func._\_name_\_ of a callable func, or makes and returns one if that fails.
To make one, it calls unamed_func_name which produces incremental names to reduce the chances of clashing

### streamlitfront.util.incremental_str_maker(str_format='{:03.f}')

Make a function that will produce a (incrementally) new string at every call.

### streamlitfront.util.signature_defaults(sig)

Return `sig.defaults` without the params whose default is `i2`’s `NotSet`.

`NotSet` in a signature means “no value given”, not a real default, so a widget
must not be prefilled with it, nor typed after it.

* **Return type:**
  [`dict`](https://docs.python.org/3/builtins/stdtypes.html#dict)

```pycon
>>> from i2.deco import NotSet
>>> def foo(a, b=NotSet, c=3): ...
>>> signature_defaults(Sig(foo))
{'c': 3}
```
