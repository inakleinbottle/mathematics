from inspect import isclass
from functools import wraps
import warnings

from . import plane
from . import ifs

__all__ = []
_warned = set()


def _final_api(func):
    __all__.append(func.__name__)
    return func


def _experimental_api(func):
    __all__.append(func.__name__)

    @wraps(func)
    def wrapper(*args, **kwargs):
        if func.__name__ not in _warned:
            warnings.warn(
                f"{func.__name__} is marked as experimental, use with care.",
                ImportWarning,
                stacklevel=2
                )


def api(mode="final"):
    """
    Utility decorator to expose functions and classes in the external API
    :param mode:
    :return:
    """
    func = None
    if callable(mode):
        func = mode
        mode = "final"
    elif isclass(mode):
        func = mode
        mode = "final"

    if mode == "final" and func is None:
        return _final_api
    elif mode == "final" and func is not None:
        return _final_api(func)
    elif mode == "experimental" and func is None:
        return _experimental_api
    elif mode == "experimental" and func is not None:
        return _experimental_api(func)
    else:
        raise ValueError("Invalid mode")
