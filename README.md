
# streamlitfront
Generate streamlit frontends from python functions


To install:	```pip install streamlitfront```


# Example

Define functions in a file named ``render_functions.py``:

```python
def foo(a: int = 1, b: int = 2, c=3):
    """This is foo. It computes something"""
    return (a * b) + c


def bar(x, greeting="hello"):
    """bar greets its input"""
    return f"{greeting} {x}"


def confuser(a: int, x: float = 3.14):
    return (a ** 2) * x


funcs = [foo, bar, confuser]
```

Then add the following to the file (we will be modifying this part):

```python
from streamlitfront import mk_app

if __name__ == '__main__':
    app = mk_app(funcs)
    app()
```

Execute `streamlit run render_functions.py` in terminal and ...

![image](https://user-images.githubusercontent.com/63666082/172496315-86f65258-f59f-4e17-b9bc-c92c69884311.png)

![image](https://user-images.githubusercontent.com/63666082/172496343-a0a876eb-6e6b-4e6b-a890-352c4a21664a.png)

![image](https://user-images.githubusercontent.com/63666082/172496378-40efc696-05d6-4e4e-af9f-da94e0803927.png)

... you can play with your functions!

## Configuration

The default configuration for the application is define by the convention object: ``dflt_convention``. But you can overwrite parts or the entire configuration by setting the ``config`` parameter. The configuration is composed of three parts: app, obj and rendering.

- app

    By default, the application name is "My Front Application", but you can set the title of the application as follow:

    ```python
    from streamlitfront import mk_app
    

    if __name__ == '__main__':
        config = {
            'app': {
                'title': 'Another application name'
            }
        }
        app = mk_app(funcs, config=config)
        app()
    ```

    Execute `streamlit run render_functions.py` in terminal and ...

    ![image](https://user-images.githubusercontent.com/63666082/172715999-6611d981-6e7c-4ea1-8d02-2ec449912bf2.png)

    ... the application name changed!

- obj

    You can define a wrapper to transform the initial object into an output of your choice to be rendered:
    
    ```python
    from typing import Iterable
    from streamlitfront import mk_app
    

    def trans(objs: Iterable):
        return list(reversed(objs))
    

    if __name__ == '__main__':
        config = {
            'obj': {
                'trans': trans
            }
        }
        app = mk_app(funcs, config=config)
        app()
    ```

    Execute `streamlit run render_functions.py` in terminal and ...
    
    ![image](https://user-images.githubusercontent.com/63666082/172716258-3efcfa55-f25c-4ae2-a232-a788f62b541b.png)

    ... the view order has changed !

    Note that the capital letter at the beginning of the view names are gone, because the default transforming is no longer applied.

- rendering

    You can define the way elements are rendered in the GUI.
    For instance, you can choose to render a text input instead of a number input for a specific parameter of a specific function:
    
    ```python
    from front.elements import INT_INPUT_SLIDER_COMPONENT
    from streamlitfront import mk_app
    

    if __name__ == '__main__':
        config = {
            'rendering': {
                'Foo': {
                    'inputs': {
                        'a': {
                            'component': INT_INPUT_SLIDER_COMPONENT,
                            'max_value': 10
                        }
                    }
                }
            }
        }
        app = mk_app(funcs, config=config)
        app()
    ```

    Execute `streamlit run render_functions.py` in terminal and ...

    ![image](https://user-images.githubusercontent.com/63666082/172725124-2a88c95b-8c1f-423e-9e68-0c1b90a5e031.png)

    ... the input ``a`` is a slider now !
    
Obviously, you can combine the three types of configuration:
    
```python
from typing import Iterable
from front.elements import INT_INPUT_SLIDER_COMPONENT
from streamlitfront import mk_app
    

def trans(objs: Iterable):
    return list(reversed(objs))


if __name__ == '__main__':
    config = {
        'app': {
            'title': 'Another application name'
        },
        'obj': {
            'trans': trans
        },
        'rendering': {
            'foo': {
                'inputs': {
                    'a': {
                        'component': INT_INPUT_SLIDER_COMPONENT,
                        'max_value': 10
                    }
                }
            }
        }
    }
    app = mk_app(funcs, config=config)
    app()
```

Execute `streamlit run render_functions.py` in terminal and ...

![image](https://user-images.githubusercontent.com/63666082/172725591-b3a60cf6-b497-4f4d-87d7-ce02ec90dbe4.png)

... all three configurations are applied !

You can also overwrite the whole configuration by setting the ``convention`` parameter. Be careful though, by overwritting the default convention, you have to make sure that all configuations are defined. Otherwise, the application would crash or behave unexpectedly.
    
```python
from typing import Any, Callable, Iterable
from front.elements import VIEW_CONTAINER, FLOAT_INPUT_SLIDER_COMPONENT, TEXT_INPUT_COMPONENT
from streamlitfront import mk_app
    

def trans(objs: Iterable):
    return list(reversed(objs))


if __name__ == '__main__':
    convention = {
        'app': {
            'title': 'Another application name'
        },
        'obj': {
            'trans': trans
        },
        'rendering': {
            Callable: {
                'container': VIEW_CONTAINER,
                'inputs': {
                    float: {
                        'component': FLOAT_INPUT_SLIDER_COMPONENT,
                        'max_value': 10.0,
                        'format': '%.2f',
                        'step': 0.01,
                    },
                    Any: {
                        'component': TEXT_INPUT_COMPONENT,
                    },
                },
            },
        },
    }
    app = mk_app(funcs, convention=convention)
    app()
```

Execute `streamlit run render_functions.py` in terminal and ...

![image](https://user-images.githubusercontent.com/63666082/172726101-a596ea02-bf1c-4c66-b6b4-6569d1176b5c.png)

... the convention is applied !

# Old Example (using deprecated ``dispatch_funcs`` function)

Write a module like this:

```python
# simple.py

def foo(a: int = 0, b: int = 0, c=0):
    """This is foo. It computes something"""
    return (a * b) + c

def bar(x, greeting='hello'):
    """bar greets its input"""
    return f'{greeting} {x}'

def confuser(a: int = 0, x: float = 3.14):
    return (a ** 2) * x

funcs = [foo, bar, confuser]

if __name__ == '__main__':
    from streamlitfront import dispatch_funcs
    app = dispatch_funcs(funcs)
    app()
    
    # ... and you get a browser based app that exposes foo, bar, and confuser

```

Execute `streamlit run simple.py` in terminal and ...

![image](https://user-images.githubusercontent.com/1906276/121604989-61874d80-ca00-11eb-9e1b-e3ac28e09418.png)

![image](https://user-images.githubusercontent.com/1906276/121605028-7f54b280-ca00-11eb-93f7-f4c936ae9d54.png)
