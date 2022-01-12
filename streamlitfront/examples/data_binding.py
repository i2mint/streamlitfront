import os


def foo(state, text: str, options: list = []):
    return text, options


def bar(state, a: str = 'boo'):
    return a


funcs = [foo, bar]

if __name__ == '__main__':
    from streamlitfront.base import dispatch_funcs
    from streamlitfront.page_funcs import DataBindingExploPageFunc

    print('file: {}'.format(os.path.realpath(__file__)))

    app = dispatch_funcs(funcs, configs=dict(page_factory=DataBindingExploPageFunc))

    app()
