import os
import pandas as pd
import numpy as np
from src.utils.pandas.transformations import cross_join


def get_date_from_environment() -> str:
    """
    Returns: string with date calculated from current run_id
    """
    return f"{os.environ['DATE']} 8:00:00"


def get_stock_date_from_environment() -> str:
    """
    Returns: string with date calculated from current run_id
    """
    return f"{os.environ['DATE_DATA']} 8:00:00"


def create_week_mapping(n_weeks: int, week_start: int=0, current_date: str=None) -> pd.DataFrame:
    """
    Creates a table that maps each week id to start and end date of the week
    Parameters
    ----------
    n_weeks number of weeks to expand from current date

    Returns
    -------

    """
    if current_date is None:
        current_date = get_date_from_environment()
    df_dict = {
            "start_date": [pd.to_datetime(current_date)],
            "end_date": [pd.to_datetime(current_date) + pd.to_timedelta(7, "days")]}
    df_weeks = pd.DataFrame({"week": np.arange(week_start, n_weeks)})
    df_weeks = cross_join(df_weeks, pd.DataFrame(df_dict))
    df_weeks["week_start_date"] = df_weeks["start_date"] + pd.to_timedelta(df_weeks["week"]*7, "days")
    df_weeks["week_end_date"] = df_weeks["end_date"] + pd.to_timedelta(df_weeks["week"]*7, "days")
    df_weeks = df_weeks.drop(columns=["start_date", "end_date"])
    return df_weeks


def intersect_date_range(
        df_in: pd.DataFrame,
        col_start: str,
        col_end: str,
        col_start_right: str,
        col_end_right: str
) -> pd.DataFrame:
    df = df_in.copy()
    df[col_start] = np.max([df[col_start], df[col_start_right]], axis=0)
    df[col_end] = np.min([df[col_end], df[col_end_right]], axis=0)
    df = df[df[col_start] < df[col_end]]
    return df
