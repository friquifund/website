import logging
import os
from datetime import datetime
from typing import List
from pathlib import Path

import pandas as pd


def get_logger(log_filepath: str, level: str = "DEBUG") -> logging.log:
    """

    Parameters
    ----------
    log_filepath: string, can be either a full path or a directory
    level

    Returns a logger that logs both to console and file
    -------

    """
    # Get logger
    logger = logging.getLogger()
    logger.setLevel(level)

    # Create file handler
    if not Path(log_filepath).suffix == ".log":
        current_date = datetime.today().strftime("%Y-%m-%d_%H-%M-00")
        log_filepath = os.path.join(log_filepath, f"{current_date}.log")

    Path(log_filepath).parents[0].mkdir(parents=True, exist_ok=True)
    fh = logging.FileHandler(log_filepath)
    fh.setLevel(level)

    # Create console handler
    ch = logging.StreamHandler()
    ch.setLevel(level)
    # Add formatter to the handlers
    formatter = logging.Formatter("%(asctime)s %(levelname)-8s %(message)s")
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)
    # Add handlers to the logger
    logger.addHandler(fh)
    logger.addHandler(ch)
    return logger


class DataTracker:
    """
    This class facilitates field tracking by simplifying the syntax of:
    1) Doing a left join by the key (shp_part_num, generally)
    2) Renaming the columns
    This allows to make the pipeline more readable and understand the intent of certain operations
    """

    def __init__(self, primary_key: pd.Series, key_name):
        self.key = key_name
        self.data = pd.DataFrame({key_name: primary_key.copy()})

    def track(self, df: pd.DataFrame, column_names: List[str] = None, how="left"):
        df_merge = df.copy()
        if column_names is not None:
            df_merge.columns = [self.key] + column_names
        self.data = pd.merge(self.data, df_merge, on=self.key, how=how)
        return None

    def track_multiple(self, df_list: List[pd.DataFrame]):
        for df in df_list:
            self.track(df)
        return None
