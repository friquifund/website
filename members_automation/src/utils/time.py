import pandas as pd
import datetime
import numpy as np
from datetime import datetime


def get_diff_time_hours(time1, time2):
    """
    Gets the time difference between two timestamps, calculated as time2 - time1 in hours
    Parameters
    ----------
    time1
    time2

    Returns
    -------

    """
    return np.floor((time2 - time1).total_seconds() / 3600)


def get_current_time(localize_utc=True):
    """
    Calculates the current timestamp of the machine
    Returns Time in UTC, localized to UTC
    -------

    """
    date_now = datetime.datetime.utcnow()
    date_now = date_now.replace(microsecond=0)
    date_now = pd.to_datetime(date_now)
    if localize_utc:
        date_now = date_now.tz_localize("UTC")

    return date_now


def dt_floor_with_offset(series: pd.Series, offset: int, frequency: str):
    series = series - pd.DateOffset(minutes=offset)
    series = series.dt.floor(frequency)
    series = series + pd.DateOffset(minutes=offset)

    return series


def nano_to_minutes(nano: int) -> float:
    """
    transforms nano time to minutes
    Parameters
    ----------
    nano

    Returns
    -------

    """
    return nano / (60 * 10e8)


def transform_time_window_to_minutes(time_window: str) -> int:
    """
    Transforms time window string to minutes
    Parameters
    ----------
    time_window

    Returns
    -------

    """
    time_delta_nano = pd.tseries.frequencies.to_offset(time_window).nanos
    minutes = int(nano_to_minutes(time_delta_nano))
    return minutes


def get_run_id_folder() -> str:
    return datetime.today().strftime("%Y-%m-%d_%H-%M-%S")
