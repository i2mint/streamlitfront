"""Utils for CRUDE"""


def auto_key(*args, **kwargs) -> str:
    """Make a str key from arguments.

    >>> auto_key(1,2,c=3,d=4)
    '1,2,c=3,d=4'
    >>> auto_key(1,2)
    '1,2'
    >>> auto_key(c=3,d=4)
    'c=3,d=4'
    >>> auto_key()
    ''
    """
    args_str = ",".join(map(str, args))
    kwargs_str = ",".join(map(lambda kv: f"{kv[0]}={kv[1]}", kwargs.items()))
    return ",".join(filter(None, [args_str, kwargs_str]))
