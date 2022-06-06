
# streamlitfront
Generate streamlit frontends from python functions


To install:	```pip install streamlitfront```


# Example

Write a module like this:

```python
# render_functions.py

from streamlitfront import mk_app

def foo(a: int = 1, b: int = 2, c=3):
    """This is foo. It computes something"""
    return (a * b) + c


def bar(x, greeting="hello"):
    """bar greets its input"""
    return f"{greeting} {x}"


def confuser(a: int, x: float = 3.14):
    return (a ** 2) * x


funcs = [foo, bar, confuser]

if __name__ == '__main__':
    app = mk_app(funcs)
    app()
    
    # ... and you get a browser based app that exposes foo, bar, and confuser

```

Execute `streamlit run render_functions.py` in terminal and ...

![image](https://user-images.githubusercontent.com/1906276/121604989-61874d80-ca00-11eb-9e1b-e3ac28e09418.png)

![image](https://user-images.githubusercontent.com/1906276/121605028-7f54b280-ca00-11eb-93f7-f4c936ae9d54.png)

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

- obj

    You can define a wrapper to transform the initial object into an ouput of your choice to be rendered:
    
    ```python
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


- rendering

    You can define the way elements are rendered in the GUI.
    For instance, you can choose to render a text input instead of a number input for a specific parameter of a specific function:
    
    ```python
    from front.elements import InputComponentFlag
    from streamlitfront import mk_app
    
    if __name__ == '__main__':
        config = {
            'rendering': {
                'Foo': {
                    'a': InputComponentFlag.TEXT
                }
            }
        }
        app = mk_app(funcs, config=config)
        app()
    ```
    
Obviously, you can combine the three types of configuration:
    
```python
from front.elements import InputComponentFlag
from streamlitfront import mk_app

if __name__ == '__main__':
    config = {
        'app': {
            'title': 'Another application name'
        },
        'obj': {
            'trans': trans
        },
        'rendering': {
            'Foo': {
                'a': InputComponentFlag.TEXT
            }
        }
    }
    app = mk_app(funcs, config=config)
    app()
```

You can also overwrite the whole configuration by setting the ``convention`` parameter. Be careful though, by overwritting the default convention, you have to make sure that all configuations are defined. Otherwise, the application would crash or behave unexpectedly.
    
```python
from front.elements import InputComponentFlag, ContainerFlag
from streamlitfront import mk_app

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
                'container': ContainerFlag.VIEW,
                'inputs': {
                    float: {
                        'component': InputComponentFlag.FLOAT_SLIDER,
                        'format': '%.2f',
                        'step': 0.01,
                    },
                    Any: InputComponentFlag.TEXT,
                },
            },
        },
    }
    app = mk_app(funcs, convention=convention)
    app()
```

# Old Example (using dispatch_funcs)

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



