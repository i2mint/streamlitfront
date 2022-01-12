
# streamlitfront
Generate streamlit frontends from python functions


To install:	```pip install streamlitfront```


# Example

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



