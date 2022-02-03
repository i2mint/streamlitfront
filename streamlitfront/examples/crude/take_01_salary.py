"""A simple app to demo the use of Mappings to handle complex type"""
from typing import Mapping

ComplexType = float  # just pretend it's complex!


def func(salary: ComplexType, n_months: int = 12):
    return salary * n_months


SalaryKey = str  # or some type that will resolve in store-fed key selector
SalaryMapping = Mapping[SalaryKey, ComplexType]

salary_store: SalaryMapping
salary_store = {"sylvain": 10000, "christian": 2000, "thor": 50000}


def store_wrapped_func(salary: SalaryKey, n_months: int = 12):
    salary = salary_store[salary]
    return func(salary, n_months)


assert store_wrapped_func("sylvain", 6) == 60000


if __name__ == "__main__":
    from streamlitfront.base import dispatch_funcs

    app = dispatch_funcs([func, store_wrapped_func])
    app()
