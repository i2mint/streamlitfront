from contextlib import contextmanager
from functools import partial
from inspect import Parameter
from random import choice, randint, uniform
import string
from typing import Any
from i2 import Sig
from numbers import Number
from sys import platform
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from strand import run_process
from streamlitfront.run_app import run_app
from time import sleep
import dill
import pickle

STREAMLIT_APP_URL = 'http://localhost:8501'


@contextmanager
def dispatch_funcs_with_selenium(funcs, headless=False):
    """
    Dispatches the functions in a streamlit application and build a selenium object
    representing the root of the DOM for the application.
    """
    serialize_funcs = False
    try:
        pickle.dumps(funcs)
    except:
        serialize_funcs = True
    _funcs = dill.dumps(funcs) if serialize_funcs else funcs
    with run_process(func=run_app, func_kwargs={'funcs': _funcs}, is_ready=3) as proc:
        options = ChromeOptions()
        # options.add_argument('--no-sandbox')
        options.add_argument('--window-size=1920,1080')
        if headless:
            options.add_argument('--headless')
        # options.add_argument('--disable-gpu')
        # options.add_argument('--allow-running-insecure-content')
        dom = Chrome(service=Service(ChromeDriverManager().install()), options=options)
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


@give_a_chance_to_render_element
def find_element_by_css_selector(css_selector, root):
    return root.find_element(By.CSS_SELECTOR, css_selector)


def select_func(idx, root):
    radio_button = find_element_by_css_selector(
        f".block-container .stRadio div[role='radiogroup'] label:nth-child({idx + 1})",
        root,
    )
    radio_button.click()
    sleep(0.5)


def send_input(input_, idx, root):
    def get_input_type():
        if isinstance(input_, Number):
            return 'number'
        if isinstance(input_, str):
            return 'text'

    input_type = get_input_type()
    input_el = find_element_by_css_selector(
        f".main .element-container:nth-child({idx + 2}) input[type='{input_type}']",
        root,
    )
    input_el.click()
    select_all_first_key = Keys.COMMAND if platform == 'darwin' else Keys.CONTROL
    input_el.send_keys(select_all_first_key, 'a')
    input_el.send_keys(str(input_))


def compute_output(func, root):
    def get_output(previous_output=None, intent_nb=1):
        output_el = find_element_by_css_selector(output_css_selector, root)
        if output_el.find_elements(By.TAG_NAME, 'code'):
            output_el = find_element_by_css_selector('code', output_el)
        output = output_el.text
        return_annot = Sig(func).return_annotation
        if return_annot not in (Parameter.empty, Any):
            output = return_annot(output)
        if previous_output is not None and output == previous_output and intent_nb < 3:
            sleep(1)
            return get_output(previous_output, intent_nb + 1)
        return output

    def get_previous_output():
        if root.find_elements(By.CSS_SELECTOR, output_css_selector):
            return get_output()

    nb_args = len(Sig(func))
    output_css_selector = f'.element-container:nth-child({nb_args + 3}) .stMarkdown p'
    previous_output = get_previous_output()
    submit_button = find_element_by_css_selector(
        f'.element-container:nth-child({nb_args + 2}) button', root
    )
    submit_button.click()
    return get_output(previous_output)
