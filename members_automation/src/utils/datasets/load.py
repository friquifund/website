import logging
from typing import Any, Dict

import pandas as pd
from box import BoxList
import gspread

from src.utils.datasets.commons import check_if_single_node, get_file_extension, file_exists, load_txt

log = logging.getLogger(__name__)


def load_in_memory(filepath: str, file_extension: str = None, **kwargs) -> Any:
    """
    This function allows to load a generic data file using its extension to call the proper function. If the file doesn't
    exist returns none
    Function follows steps:
    1) Decide if load using distributed (spark) functionalities or python
    2) Call the load_wrapper on the corresponding functions
    Parameters
    ----------
    filepath: path of the file
    file_extension: specified file extension, typically if we want to read a full folder that contains parquet files
    but the folder name doesn't have parquet in it

    Returns object with the data of the file loaded in memory or None if the file doesn't exist
    -------

    """
    # 1) Return None if the file doesn't exist

    # 2) Get file extension

    # 1) Decide if load using distributed (spark) functionalities or python
    if check_if_single_node(filepath):
        if not file_exists(filepath):
            raise ValueError(f"Load error: File {filepath} not found")
        function_map = get_single_node_functions()
    else:
        function_map = get_distributed_functions()
    # 2) Call the load_wrapper on the corresponding functions
    dict_kwargs = _parse_parameters(kwargs)
    data = load_wrapper(filepath, function_map, file_extension, **dict_kwargs)

    return data


def _parse_parameters(kwargs: Dict) -> Dict:
    """
    Transforms boxlist to dictionary. This is needed because some load functions throw an error
    when receiving a boxlist as input
    Parameters
    ----------
    kwargs

    Returns
    -------

    """
    dict_kwargs = {}
    for k, v in kwargs.items():
        if isinstance(v, BoxList):
            dict_kwargs[k] = list(v)
        else:
            dict_kwargs[k] = v
    return dict_kwargs


def get_single_node_functions() -> dict:
    """
    Returns dictionary with load functions to be used in single node environment
    Returns
    -------

    """
    from src.utils.datasets.commons import load_json, load_pickle

    function_map = {
        "parquet": pd.read_parquet,
        "gzip": pd.read_parquet,
        "csv": pd.read_csv,
        "json": load_json,
        "xlsx": pd.read_excel,
        "pkl": load_pickle,
        "txt": load_txt
    }
    return function_map


def get_distributed_functions() -> dict:
    """
    [Initializes sparkr session] Returns dictionary with load functions to be used in spark cluster
    Returns
    -------

    """
    from src.utils.spark.session import spark

    function_map = {
        "parquet": spark.read.parquet,
        "csv": lambda filepath, **kwargs: spark.read.csv(
            filepath, header=True, **kwargs
        ),
        "text": spark.read.text,
        "json": spark.read.json,
    }
    return function_map


def load_wrapper(
    filepath: str, function_map: dict = get_single_node_functions(), file_extension: str = None, **kwargs
) -> Any:
    """
    Load wrapper that loads a file trying to use the single node functions
    Parameters
    ----------
    filepath: Location of the object to be loaded
    function_map: Mapping of file type to load function to use
    file_extension: forced file extension, typically if we want to read a full folder that contains parquet files
    but the folder name doesn't have parquet in it
    kwargs any other arguments to be used when loading

    Returns
    -------

    """
    if file_extension is None:
        file_extension = get_file_extension(filepath)

    if file_extension in function_map.keys():
        load_function = function_map[file_extension]
        data = load_function(filepath, **kwargs)
        return data
    else:
        log.error("File extension not implemented")
        raise ValueError(f"Load error: Load is not implemented for extension {file_extension}")


def load_single_node(filepath: str, **kwargs) -> Any:
    """
    Wrapper function to load generic in single node function
    Parameters
    ----------
    filepath
    kwargs

    Returns
    -------

    """
    function_map = get_single_node_functions()
    data = load_wrapper(filepath, function_map, **kwargs)
    return data


def load_spark(filepath: str, **kwargs) -> Any:
    """
    Wrapper function to load generic in spark environment
    Parameters
    ----------
    filepath
    kwargs

    Returns
    -------

    """
    function_map = get_distributed_functions()
    data = load_wrapper(filepath, function_map, **kwargs)
    return data