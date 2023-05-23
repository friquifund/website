"""
The ``session`` module provides a convenient interface to access

If no ``SparkSession`` is currently available, this module will try
to create a new one if Spark is properly installed on the host machine.
"""
import getpass
import logging
import os

from pyspark.sql import SparkSession


log = logging.getLogger(__name__)


def _get_or_create_spark_session() -> SparkSession:
    # Create spark app name
    task_id = os.environ.get("TASK_ID", f"adhoc-{getpass.getuser()}")
    run_id = os.environ.get("RUN_ID", "adhoc")
    app_name = f"{task_id}_{run_id}"
    log.info(f"initializing spark session - {app_name}")

    # Create spark session
    spark_session = SparkSession.builder.appName(app_name)
    spark_session = spark_session.getOrCreate()

    return spark_session


# Try creating the global spark and spark context
try:
    spark = _get_or_create_spark_session()
except Exception as e:
    log.error(e)
    log.error(("Couldn't import spark...Running in an environment "
               "where Spark isn't properly configured"))
    spark = None
