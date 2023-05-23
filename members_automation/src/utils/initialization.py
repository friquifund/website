import logging
import os
import pathlib
from typing import Tuple, List

from box import Box
from dotenv import load_dotenv

from src.utils.config import load_configs, merge, parse_config
from src.utils.logging import get_logger
from src.utils.paths import get_path_repo, get_path_configs


def initialize_run() -> Tuple[Box, logging.log]:
    """
    Initializes a run merging the dictionaries from the config path and the region specific path
    Returns:

    """
    load_dotenv(os.path.join(get_path_repo(), "environment.env"), override=True)
    path_configs = get_path_configs()
    log = get_logger(os.path.join(os.environ["LOG"], "logs"))
    config = load_configs(os.path.join(path_configs, "default"))
    return config, log


def create_directories(list_directories: List[str]) -> None:
    """
    Generates the directories structure of each run of the project according to the config file, the current setup is:
    date
    ├── data
    │   ├── raw
    │   ├── clean
    ├── logs
    ├── output
    Parameters
    ----------
    list_directories: list of directories

    Returns Nothing, creates a set of directories according to a dictionary structure
    -------

    """
    # -----Create all directories in list ---- #
    for path_name in list_directories:
        pathlib.Path(path_name).mkdir(parents=True, exist_ok=True)
