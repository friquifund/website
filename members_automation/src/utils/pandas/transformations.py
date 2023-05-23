import datetime
import logging
import os
from typing import List, Dict

import numpy as np
import pandas as pd


def series_to_pandas(series_in: pd.Series) -> pd.DataFrame:
    """
    Transforms series to single row pandas
    Parameters
    ----------
    series_in

    Returns
    -------

    """
    return pd.DataFrame([series_in.values], columns=series_in.index)


def apply_function_to_multiple_keys(input_dict: dict, func, keys_to_use: list) -> dict:
    """
    Applies the defined function to multiple keys in the dict.
    Modifies the input dict
    Parameters
    ----------
    input_dict
    func
    keys_to_use
    Returns
    -------

    """
    for in_key in keys_to_use:
        input_dict[in_key] = func(input_dict[in_key])

    return input_dict


def dict_to_series(input_dict: dict) -> pd.Series:
    """
    Transforms a dict to a pdSeries, where the index will be the keys, and the values the row
    Parameters
    ----------
    input_dict

    Returns
    -------

    """
    return pd.Series(index=input_dict.keys(), data=list(input_dict.values()))


def dict_to_pandas(input_dict: dict, index: list = None) -> pd.DataFrame:
    """
    Transforms a dict to a pandas dataframe, where the index will be the keys, and the values the row
    Parameters
    ----------
    input_dict
    index

    Returns
    -------

    """
    return pd.DataFrame(
        [input_dict.values()], columns=list(input_dict.keys()), index=[index]
    )


def pandas_to_dict(df: pd.DataFrame) -> dict:
    """
    Transforms a single dataframe df into a dict with one pair key-value per column of the dataframe
    Parameters
    ----------
    df

    Returns
    -------

    """
    return df.to_dict(orient="records")[0]


def append_string_to_columns(df: pd.DataFrame, string_to_concat: str) -> pd.DataFrame:
    """

    Parameters
    ----------
    df
    string_to_concat

    Returns
    -------

    """
    df.columns = string_to_concat + df.columns
    return df


def select_and_rename(df: pd.DataFrame, mapping: dict) -> pd.DataFrame:
    """
    Selects columns of a dataframe and renames them
    Parameters
    ----------
    df
    mapping

    Returns
    -------

    """
    return df[mapping.keys()].rename(columns=mapping)


def three_sigma_fill_na(df: pd.DataFrame, col: str):
    upper = df[col].mean() + 3 * df[col].std()
    lower = df[col].mean() - 3 * df[col].std()

    df.loc[df[col] > upper, col] = np.nan
    df.loc[df[col] < lower, col] = np.nan

    return df


def df_threshold_fill_na(df: pd.DataFrame, col: str, lower=None, upper=None):
    df = df.copy()
    if upper is not None:
        df.loc[df[col] > upper, col] = np.nan
    if lower is not None:
        df.loc[df[col] < lower, col] = np.nan

    return df


def ffill_on_value(pd_series: pd.Series, val_cond: float) -> pd.Series:
    """

    Parameters
    ----------
    pd_series
    val_cond

    Returns
    -------

    """
    pd_series.loc[pd_series == val_cond] = np.nan
    pd_series = pd_series.ffill()
    pd_series = pd_series.fillna(val_cond)
    return pd_series


def merge_dataframes_dict(
    df_skeleton: pd.DataFrame,
    dict_df: Dict[str, pd.DataFrame],
    merge_settings: Dict[str, Dict[str, str]],
    ordered_keys: List[str],
) -> pd.DataFrame:
    """
    Merges a dict containing multiple dataframes and a set of settings
    Parameters
    ----------
    dict_df
    df_skeleton
    merge_settings
    ordered_keys

    Returns
    -------

    """

    df_skeleton = df_skeleton.copy()
    for key in ordered_keys:
        df_skeleton = pd.merge(df_skeleton, dict_df[key], **merge_settings[key])
    return df_skeleton


def calculate_weighted_average(value: pd.Series, weight: pd.Series, group: pd.Series) -> pd.Series:
    weighted_value = value * weight
    g_weighted_value = weighted_value.groupby(group).transform(sum)
    g_weight = weight.groupby(group).transform(sum)
    return g_weighted_value / g_weight


def merge_multiple_dataframes(
        df_skeleton: pd.DataFrame,
        list_df: List[pd.DataFrame],
        how: str, on:
        List[str]) -> pd.DataFrame:
    df = df_skeleton.copy()
    for df_to_add in list_df:
        df = pd.merge(df, df_to_add, how, on)
    return df


def round_all_columns(df: pd.DataFrame, n_round: int = 2) -> pd.DataFrame:
    for col in df.columns:
        if pd.api.types.is_numeric_dtype(df[col]) and not pd.api.types.is_bool_dtype(
            df[col]
        ):
            df[col] = np.round(df[col], n_round)
    return df


def explode_df(df: pd.DataFrame, list_df: List[pd.DataFrame]) -> pd.DataFrame:
    for df2 in list_df:
        df = cross_join(df, df2)
    return df


def cross_join(df1: pd.DataFrame, df2: pd.DataFrame) -> pd.DataFrame:
    """
    Cross joins two dataframes
    Parameters
    ----------
    df1
    df2

    Returns
    -------

    """
    df1 = df1.copy()
    df2 = df2.copy()
    df1["key"] = 0
    df2["key"] = 0
    df = df1.merge(df2, on="key", how="outer")
    df = df.drop(columns="key")
    return df
