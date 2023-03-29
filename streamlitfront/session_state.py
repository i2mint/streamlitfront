"""
Session state management
"""

import streamlit as st

try:
    from streamlit.legacy_caching.hashing import _CodeHasher
except ModuleNotFoundError:
    from warnings import warn

    warn(
        'Use streamlit 1.11.1 if you want to use the old and deprecated dispatch_funcs function.'
    )

from streamlitfront.util import Objdict


def display_state_values(state, key):
    st.write('Current value of ' + str(key) + ':', state[key])


class PageState(Objdict):
    """To hold page states"""


class _SessionState:
    def __init__(self, hash_funcs):
        """Initialize SessionState instance."""
        self.__dict__['_state'] = {
            'data': {},
            'hash': None,
            'hasher': _CodeHasher(hash_funcs),
            'is_rerun': False,
        }

    def __call__(self, **kwargs):
        """Initialize state data once."""
        for item, value in kwargs.items():
            if item not in self._state['data']:
                self._state['data'][item] = value

    def __getitem__(self, item):
        """Return a saved state value, None if item is undefined."""
        return self._state['data'].get(item, None)

    def __getattr__(self, item):
        """Return a saved state value, None if item is undefined."""
        return self._state['data'].get(item, None)

    def __setitem__(self, item, value):
        """Set state value."""
        self._state['data'][item] = value

    def __setattr__(self, item, value):
        """Set state value."""
        self._state['data'][item] = value

    def clear(self):
        """Clear session state and request a rerun."""
        self._state['data'].clear()
        st.experimental_rerun()

    def has_valid(self, *k, is_valid=bool):
        """Checks that k exists and is valid.
        Validity can be specified by a function (default: bool).

        This says it all (sorta):

        # TODO: Review and remove if no longer relevant:

        # >>> s = State(a=0, b=False, c=None, d='', e=1, f=True, h='hi')
        # >>> list(filter(s.has_valid, list(s) + ['i', 'j']))
        # ['e', 'f', 'h']
        #
        # But here's the slower presentation:
        #
        # >>> s = State(a=1)
        # >>> s.has_valid('a')
        # True
        # >>> s['a'] = 0
        # >>> s.has_valid('a')
        # False
        #
        # 'a' is 0, which evaluates to False,
        # (since the default is_valid function is `bool`).
        # But if we use another custom is_valid function, it becomes valid.
        #
        # >>> s.has_valid('a', is_valid=lambda x: x is not None)
        # True
        #
        # But what ever your is_valid function, if a key doesn't exist,
        # it won't be valid.
        #
        # >>> just_care_about_key_existence = lambda x: True
        # >>> s.has_valid('b', is_valid=just_care_about_key_existence)
        # False
        #
        # That's why the method is called HAS_valid.
        # It needs to HAVE the key, and the value needs to be valid.
        #
        # You can also check the conjunctive validity of several keys.
        # Conjunctive is a pedantic way of saying "and".
        #
        # >>> s = State(a=1, b=False, c=None)
        # >>> s.has_valid('a', 'b')
        # False
        # >>> s['b'] = 2
        # >>> s.has_valid('a', 'b')
        # True
        #
        # Note that `is_valid` is a keyword-only argument.
        # If you don't specify it as a keyword argument, it will think it's a
        # key to validate. Silly it!
        #
        # >>> s.has_valid('a', 'b', 'c', just_care_about_key_existence)
        # False
        # >>> s.has_valid('a', 'b', 'c', is_valid=just_care_about_key_existence)
        # True

        """
        # return all((key in self and is_valid(self[key])) for key in k)
        return all(
            (key in self and is_valid(self._state['data'].get(key, None))) for key in k
        )

    def sync(self):
        """Rerun the app with all state values up to date from the beginning to fix rollbacks."""

        # Ensure to rerun only once to avoid infinite loops
        # caused by a constantly changing state value at each run.
        #
        # Example: state.value += 1
        if self._state['is_rerun']:
            self._state['is_rerun'] = False

        elif self._state['hash'] is not None:
            if self._state['hash'] != self._state['hasher'].to_bytes(
                self._state['data'], None
            ):
                self._state['is_rerun'] = True
                st.experimental_rerun()

        self._state['hash'] = self._state['hasher'].to_bytes(self._state['data'], None)


_session_state = None


def get_state(hash_funcs=None):
    global _session_state
    if not _session_state:
        _session_state = _SessionState(hash_funcs)
    return _session_state
