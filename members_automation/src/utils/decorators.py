import functools
import logging
import time
import warnings

import numpy as np
import pandas as pd


def timer(func):
    def wrapped(*args, **kwargs):
        before = time.time()
        result = func(*args, **kwargs)
        after = time.time()
        print(f"Elapsed time: {np.round(after - before, 2)}")
        return result

    return wrapped


def shape_logger(func):
    """This is a decorator which logs the input and output shape of
    the pd.DataFrame to the function it wraps."""

    @functools.wraps(func)
    def wrapped(df: pd.DataFrame, *args, **kwargs) -> pd.DataFrame:
        input_shape = df.shape
        output = func(df, *args, **kwargs)
        output_shape = df.shape
        logging.basicConfig(level=logging.DEBUG)
        logging.info(
            f"Input shape {input_shape} transformed into output shape"
            f" {output_shape} by function {func.__name__}"
        )
        return output

    return wrapped


def deprecated(func):
    """This is a decorator to mark functions as deprecated. It will raise
    a warning when the function is used."""

    @functools.wraps(
        func
    )  # ensures docstrings and __name__ of wrapped function are preserved
    def wrapped(*args, **kwargs):
        warnings.simplefilter("always", DeprecationWarning)  # turn off filter
        warnings.warn(
            "Call to deprecated function {}.".format(func.__name__),
            category=DeprecationWarning,
            stacklevel=2,
        )
        warnings.simplefilter("default", DeprecationWarning)  # reset filter
        return func(*args, **kwargs)

    return wrapped
