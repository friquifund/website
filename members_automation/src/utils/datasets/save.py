import os
import json
import logging
import pickle
import joblib
from typing import Any
from src.utils.datasets.load import load_spark
from src.utils.datasets.commons import get_bucket_and_key_from_path, get_file_extension
import datetime as dt
from src.utils.datasets.commons import check_if_single_node


log = logging.getLogger(__name__)


def save_to_disk(input_object: Any, filepath: str, **kwargs):
    """
    Generic function to save a file in path. The function:
    1) Checks if it should use single or distributed engine
    2) Selects the corresponding saving function based on the file extension
    Parameters
    ----------
    input_object: object in memory to be saved
    filepath: Path of the file to be saved

    Returns
    -------
    Nothing, simply saves the file
    """
    if check_if_single_node(filepath):
        function_map = get_single_node_functions()
    else:
        function_map = get_distributed_functions()

    log.info(f"Saving file into {filepath}")
    save_wrapper(input_object, filepath, function_map, **kwargs)


def save_spark(df_spark, filepath: str, **kwargs):
    """

    Parameters
    ----------
    df_spark
    filepath
    kwargs

    Returns
    -------

    """
    df_spark.write.mode("overwrite").parquet(filepath)
    return None


def spark_cache_dataframe(df, temp_path: str):
    """

    Parameters
    ----------
    df
    temp_path

    Returns
    -------

    """
    ts = dt.datetime.now().strftime("%Y%m%dT%H%M%S")
    temp_file = os.path.join(temp_path, f"df_temp_{ts}.parquet")
    save_to_disk(df, temp_file)
    df = load_spark(temp_file)
    return df


def save_wrapper(input_object: Any, filepath: str, function_map: dict, **kwargs):
    """
    Load wrapper that loads a file trying to use the single node functions
    Parameters
    ----------
    input_object: Object to save
    filepath: Location of the object to be loaded
    function_map: Mapping of file type to load function to use
    kwargs any other arguments to be used when loading

    Returns
    -------
    Nothing, simply saves the file
    """
    file_extension = get_file_extension(filepath)

    if file_extension in function_map.keys():
        save_function = function_map[file_extension]
        save_function(input_object, filepath, **kwargs)
    else:
        log.error("File extension not implemented")
        raise ValueError(
            f"Save error: Save is not implemented for extension {file_extension}"
        )


def get_distributed_functions() -> dict:

    function_map = {
        "parquet": lambda input_object, filepath, **kwargs: input_object.write.mode(
            "overwrite"
        ).parquet(filepath, **kwargs),
        "csv": lambda input_object, filepath, **kwargs: input_object.write.mode(
            "overwrite"
        ).csv(filepath, **kwargs),
    }

    return function_map


def get_single_node_functions() -> dict:
    """
    Returns dictionary with load functions to be used in single node environment
    Returns
    -------

    """
    function_map = {
        "csv": lambda input_object, filepath, **kwargs: input_object.to_csv(
            filepath, index=False, **kwargs
        ),
        "parquet": lambda input_object, filepath, **kwargs: input_object.to_parquet(
            filepath, index=False, **kwargs
        ),
        "gz": save_gz,
        "json": save_json,
        "txt": save_txt,
        "pkl": save_pickle,
        "png": lambda input_object, filepath, **kwargs: input_object.write_image(filepath),
        "jpeg": save_image
    }
    return function_map


def check_if_distributed(input_object: Any, filepath: str) -> bool:
    """

    Parameters
    ----------
    input_object
    filepath

    Returns
    -------

    """
    from pyspark.sql import DataFrame as SparkDataFrame

    return isinstance(input_object, SparkDataFrame) or "dbfs:/" in filepath


def save_txt(input_object: Any, filepath: str, **kwargs) -> None:
    """

    Parameters
    ----------
    input_object
    filepath
    kwargs

    Returns
    -------

    """
    with open(filepath, "w") as text_file:
        text_file.write(input_object)
    return None


def save_image(input_object: Any, filepath: str, **kwargs) -> None:
    """

    Parameters
    ----------
    input_object
    filepath
    kwargs

    Returns
    -------

    """
    with open(filepath, "wb") as f:
        f.write(input_object)
    return None


def save_gz(input_object: Any, filepath: str, **kwargs) -> None:
    """

    Parameters
    ----------
    input_object
    filepath
    kwargs

    Returns
    -------

    """
    with open(filepath, "w") as joblib_file:
        joblib.dump(input_object, joblib_file, **kwargs)

    return None


def save_json(input_object: Any, filepath: str, **kwargs) -> None:
    """

    Parameters
    ----------
    input_object
    filepath
    kwargs

    Returns
    -------

    """
    with open(filepath, "w") as json_file:
        json.dump(input_object, json_file, **kwargs)
    return None


def save_pickle(input_object: Any, filepath: str, **kwargs) -> None:
    """
    Function to save a pickle in s3 if the path is s3, or in local folder if not
    Parameters
    ----------
    input_object
    filepath
    kwargs

    Returns
    -------

    """

    if "s3://" in filepath:
        s3_object, _ = get_bucket_and_key_from_path(filepath, return_bucket=False)
        pickle_byte_obj = pickle.dumps(input_object)
        s3_object.put(Body=pickle_byte_obj)
    else:
        with open(filepath, "wb") as handle:
            pickle.dump(input_object, handle, **kwargs)
    return None
