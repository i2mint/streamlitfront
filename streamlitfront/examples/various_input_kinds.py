"""And example containing different kinds of inputs"""

import os
from types import MethodType


def foo(a: int = 0, b: int = 0, c=0):
    """This is foo. It computes something"""
    return (a * b) + c


class Klass:
    def __init__(self, greeting='hello', confuser_x: float = 3.14):
        self.greeting = greeting
        self.confuser_x = confuser_x

    def bar(self, x):
        """bar greets its input"""
        return f'{self.greeting} {x}'

    # def konfuser(self, a: int = 0):
    #     return (a ** 2) * self.confuser_x


def i_am_confused(self, a: int = 0):
    return (a ** 2) * self.confuser_x


klass_instance = Klass()

# inject_method(klass_instance, 'konfuser', confuser)
klass_instance.konfuser = MethodType(i_am_confused, klass_instance)

funcs = [foo, klass_instance.bar, klass_instance.konfuser]


if __name__ == '__main__':
    from streamlitfront.base import dispatch_funcs

    print('file: {}'.format(os.path.realpath(__file__)))
    app = dispatch_funcs(funcs)
    app()
