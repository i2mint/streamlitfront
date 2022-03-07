from contextlib import contextmanager
from functools import partial
from random import randint, uniform, choice
import string
from sys import platform
from numbers import Number
import pytest
from time import sleep
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from strand import run_process
from streamlitfront.run_app import run_app
from i2 import Sig
from i2.wrapper import wrap

STREAMLIT_APP_URL = 'http://localhost:8501'


def foo(a: int = 0, b: int = 0, c=0):
    """This is foo. It computes something"""
    return (a * b) + c


def bar(x: str, greeting="hello"):
    """bar greets its input"""
    return f"{greeting} {x}"


def confuser(a: int = 0, x: float = 3.14):
    return (a ** 2) * x


@contextmanager
def dispatch_funcs(funcs, headless):
    """
    Dispatches the functions in a streamlit application and build a selenium object
    representing the root of the DOM for the application.
    """
    with run_process(func=run_app, func_kwargs={'funcs':funcs}, is_ready=3) as proc:
        options = ChromeOptions()
        # options.add_argument('--no-sandbox')
        options.add_argument('--window-size=1920,1080')
        if headless:
            options.add_argument('--headless')
        # options.add_argument('--disable-gpu')
        # options.add_argument('--allow-running-insecure-content')
        dom = Chrome(options=options)
        dom.get(STREAMLIT_APP_URL)
        try:
            yield dom
        finally:
            dom.close()


def give_a_chance_to_render_element(func):
    """
    Gives a chance to the application to render the element by trying up to three times
    with 1 second of interval to find it before raising an error.
    """
    # @wrap(func)
    def wrapper(*args, **kwargs):
        def _try_to_find_element(intent_nb):
            try:
                return func(*args, **kwargs)
            except NoSuchElementException:
                if intent_nb < 3:
                    sleep(1)
                    return _try_to_find_element(intent_nb + 1)
                raise
        return _try_to_find_element(1)
    return wrapper


# def wait_to_render(cls):
#     for attr, val in cls.__dict__.items():
#         if callable(val) and attr.startswith('find_element'):
#             setattr(cls, attr, give_a_chance_to_render_element(val))
#     return cls


# WebElement = wait_to_render(WebElement)


rdm_int = partial(randint, a=-100, b=100)
rdm_float = partial(uniform, a=-100.0, b=100.0)

def rdm_str():
    nb_char = randint(5, 15)
    return ''.join(choice(string.ascii_letters + string.digits) for _ in range(nb_char))


@pytest.mark.parametrize(
    'spec',
    [
        ({
            foo: [
                (rdm_int(),),
                (rdm_int(), rdm_int()),
                (rdm_int(), rdm_int(), rdm_int()),
            ]
        }),
        ({
            foo: [(rdm_int(), rdm_int(), rdm_int())],
            bar: [
                (rdm_str(),),
                (rdm_str(), rdm_str()),
            ],
        }),
        ({
            foo: [(rdm_int(), rdm_int(), rdm_int())],
            bar: [(rdm_str(), rdm_str())],
            confuser: [
                (rdm_int(),),
                (rdm_int(), rdm_float()),
            ]
        })
    ],
)
def test_dispatch_funcs(headless, spec: dict):
    def test_func(func_idx, func):
        @give_a_chance_to_render_element
        def find_element_by_css_selector(css_selector, parent=None):
            parent = parent or dom
            return parent.find_element(By.CSS_SELECTOR, css_selector)

        def select_func(idx):
            radio_button = find_element_by_css_selector(
                f'.block-container .stRadio label:nth-child({idx + 1})'
            )
            radio_button.click()

        def test_inputs(inputs):
            def send_input(input_, index):
                def get_input_type():
                    if isinstance(input_, Number):
                        return 'number'
                    if isinstance(input_, str):
                        return 'text'

                input_type = get_input_type()
                input_el = find_element_by_css_selector(
                    f".element-container:nth-child({index + 2}) input[type='{input_type}']"
                )
                input_el.click()
                select_all_first_key = Keys.COMMAND if platform == "darwin" else Keys.CONTROL
                input_el.send_keys(select_all_first_key, 'a')
                input_el.send_keys(str(input_))

            def compute_output(func):
                def get_output(previous_output=None, intent_nb=1):
                    output_el = find_element_by_css_selector(
                        f'.element-container:nth-child({nb_args + 3}) .stMarkdown p'
                    )
                    if output_el.find_elements(By.TAG_NAME, 'code'):
                        output_el = find_element_by_css_selector('code', output_el)
                    output = output_el.text
                    if previous_output and output == previous_output and intent_nb < 3:
                        sleep(1)
                        return get_output(previous_output, intent_nb + 1)
                    return output

                def get_previous_output():
                    if dom.find_elements(
                        By.CSS_SELECTOR, f'.element-container:nth-child({nb_args + 3}) .stMarkdown p'
                    ):
                        return get_output()

                nb_args = len(Sig(func))
                previous_output = get_previous_output()
                submit_button = find_element_by_css_selector(
                    f'.element-container:nth-child({nb_args + 2}) button'
                )
                submit_button.click()
                return get_output(previous_output)

            for input_idx, input_ in enumerate(inputs):
                send_input(input_, input_idx)
            output = compute_output(func)
            assert output == str(func(*inputs))

        input_spec = spec[func]
        select_func(func_idx)
        for inputs in input_spec:
            test_inputs(inputs)

    funcs = list(spec)
    with dispatch_funcs(funcs, headless) as dom:
        for func_idx, func in enumerate(funcs):
            test_func(func_idx, func)
