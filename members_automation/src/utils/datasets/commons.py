import os
from typing import Any


def load_txt(filepath: str, **kwargs) -> Any:

    file = open(filepath, "rb")
    filecontents = file.read().decode("utf-8", "ignore")
    file.close()

    return filecontents


def load_json(filepath, **kwargs) -> Any:
    """
    Custom function to load_json
    Parameters
    ----------
    filepath
    kwargs

    Returns
    -------

    """
    import json

    with open(filepath) as f:
        data = json.load(f, **kwargs)
    return data


def load_pickle(filepath, **kwargs) -> Any:
    """
    Custom function to load pickle when path in S3
    Parameters
    ----------
    filepath
    kwargs

    Returns
    -------
    """
    if "s3://" in filepath:
        import io
        import joblib

        s3_bucket, path = get_bucket_and_key_from_path(filepath)
        with io.BytesIO() as data:
            s3_bucket.download_fileobj(path, data)
            data.seek(0)
            data = joblib.load(data)
    else:
        import pickle

        with open(filepath, "rb") as handle:
            data = pickle.load(handle, **kwargs)

    return data


def get_bucket_and_key_from_path(filepath: str, return_bucket: bool = True):
    """

    Parameters
    ----------
    filepath
    return_bucket

    Returns
    -------

    """
    import boto3

    bucket = filepath.split("/", maxsplit=3)[2]
    path = filepath.split("/", maxsplit=3)[3]
    s3 = boto3.resource("s3")
    if return_bucket:
        s3_bucket = s3.Bucket(bucket)
    else:
        s3_bucket = s3.Object(bucket, path)
    return s3_bucket, path


def file_exists_in_bucket(filepath: str) -> bool:
    """
    Returns true if a path is a file in a bucket
    Parameters
    ----------
    filepath

    Returns
    -------

    """
    s3_bucket, path = get_bucket_and_key_from_path(filepath)
    file_exists = len(list(s3_bucket.objects.filter(Prefix=path))) >= 1
    return file_exists


def get_file_extension(filepath: str) -> str:
    """

    Parameters
    ----------
    filepath

    Returns
    -------

    """
    _, file_extension = os.path.splitext(filepath)
    file_extension = file_extension.lower().replace(".", "")
    return file_extension


def check_if_single_node(filepath: str) -> bool:
    """

    Parameters
    ----------
    filepath

    Returns
    -------

    """
    return "dbfs:/" not in filepath


def file_exists(filepath: str) -> bool:
    """

    Args:
        filepath:

    Returns:

    """
    if "s3://" in filepath:
        return file_exists_in_bucket(filepath)
    else:
        return os.path.isfile(filepath)


def load_image(filepath: str, **kwargs) -> None:
    """

    Parameters
    ----------
    filepath
    kwargs

    Returns
    -------

    """
    with open(filepath, "rb") as f:
        f.read()
    return None
