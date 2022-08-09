# import os


# def foo(state, text: str, options: list = []):
#     return text, options


# def bar(state, a: str = 'boo'):
#     return a


# funcs = [foo, bar]

# if __name__ == '__main__':
#     from streamlitfront.base import dispatch_funcs
#     from streamlitfront.page_funcs import DataBindingExploPageFunc

#     print('file: {}'.format(os.path.realpath(__file__)))

#     app = dispatch_funcs(funcs, configs=dict(page_factory=DataBindingExploPageFunc))

#     app()

from datetime import datetime
from dateutil.relativedelta import relativedelta
from front import APP_KEY, RENDERING_KEY, ELEMENT_KEY, OBJ_KEY, NAME_KEY
from collections.abc import Callable

from streamlitfront.base import mk_app
from streamlitfront.types import BoundData
from streamlitfront.elements.elements import SelectBox, TextInput, TextSection


data = {
    'Pink Floyd': {
        'David Gilmour': 'Guitar',
        'Roger Waters': 'Bass Guitar',
        'Syd Barrett': 'Guitar',
        'Richard Wright': 'Keyboards',
        'Nick Mason': 'Drums',
    },
    'The Doors': {
        'Jim Morrison': 'Lead vocalist',
        'Ray Manzarek': 'Keyboards',
        'Robby Krieger': 'Guitar',
        'John Densmore': 'Drums',
    },
    'The Beatles': {
        'John Lennon': 'Guitar',
        'Paul McCartney': 'Bass Guitar',
        'George Harrison': 'Guitar',
        'Ringo Starr': 'Drums',
    },
}

data_with_no_band = dict(
    member_item for members in data.values() for member_item in members.items()
)

intruments = {instrument for instrument in data_with_no_band.values()}


def get_instrument_from_band_and_member(band: str, member: str):
    return data[band][member]


def get_instrument_from_member_only(member: str):
    return data_with_no_band[member]


def get_members_from_instrument(instrument: str):
    return [
        f'{m} ({band})'
        for band, members in data.items()
        for m, i in members.items()
        if i == instrument
    ]


# TODO: Discuss about the underlying functionnal generality of BoundData
# selected_band = BoundData(id='selected_band')
members_of_selected_band = BoundData(id='members_of_selected_band')
output_instrument = BoundData(id='output_instrument')


def on_select_band(band):
    # selected_band.value = band
    members_of_selected_band.value = list(data[band])


def set_output_instrument(output):
    output_instrument.value = output


if __name__ == '__main__':
    app = mk_app(
        [
            get_instrument_from_band_and_member,
            get_instrument_from_member_only,
            get_members_from_instrument,
        ],
        config={
            APP_KEY: {'title': 'Data Binding'},
            # OBJ_KEY: {'trans': crudify},
            RENDERING_KEY: {
                'get_instrument_from_band_and_member': {
                    NAME_KEY: 'From an input to another',
                    'description': {
                        'content': 'Select a band and see how the list of members is updated.'
                    },
                    'execution': {'on_submit': set_output_instrument},
                },
                'get_instrument_from_member_only': {
                    NAME_KEY: 'From a screen to another',
                    'description': {
                        'content': 'Select a band from the previous page ("From an input to another") and see how the list of members (of this page) is updated.'
                    },
                    'execution': {'on_submit': set_output_instrument},
                },
                'get_members_from_instrument': {
                    NAME_KEY: 'From an output to an input',
                    'description': {
                        'content': 'Submit any other screen and see that the output is automatically selected from the "Instrument" select box.'
                    },
                },
                Callable: {
                    'execution': {
                        'inputs': {
                            str: {ELEMENT_KEY: SelectBox,},
                            'band': {
                                'options': list(data),
                                # 'value': selected_band,
                                'on_value_change': on_select_band,
                            },
                            'member': {'options': members_of_selected_band},
                            'instrument': {
                                'options': intruments,
                                'value': output_instrument,
                            },
                        }
                    }
                },
            },
        },
    )
    app()
