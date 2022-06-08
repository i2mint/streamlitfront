def pytest_addoption(parser):
    parser.addoption('--headless', action='store_true', default=False)


def pytest_generate_tests(metafunc):
    option_value = metafunc.config.option.headless
    if 'headless' in metafunc.fixturenames and option_value is not None:
        metafunc.parametrize('headless', [option_value])
