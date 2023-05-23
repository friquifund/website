from typing import List, Optional

import numpy as np
import pandas as pd
from pyspark.sql import DataFrame as SparkDataFrame
from pyspark.sql.window import Window

from src.utils.spark.utils import PysparkFunctions as F


def group_by_dict(
    df: SparkDataFrame,
    cols_group: List[str],
    agg_dict: dict,
    col_weight: Optional[str] = None,
    keep_original_names: Optional[bool] = False,
) -> SparkDataFrame:
    """
    This function is a wrapper of pyspark group by that allows to group by a column and perform a set of operations by
    taking care of the naming at the output. Operations include weighted_average.
    The operations go specified in an input dict of the form:
    {
        col_value_1: [sum, avg, w_avg],
        col_value_2: [count, min, max]
        ...
    }
    By default will return col_value_1_sum, col_value_1_avg, col_value_1_w_avg, col_value_2_count, col_value_2_min, col_value_2_max
    Args:
        df: input spark dataframe
        cols_group: cols to group by
        agg_dict: aggregation dict that contains value columns and opperations to perform
        col_weight: column to weight by in case using weighted_average
        keep_original_names: if set to true, will mantain original names after transformation

    Returns:

    """

    agg_list = []
    for col_name, func_list in agg_dict.items():
        if not isinstance(func_list, list):
            func_list = [func_list]
        for func_name in func_list:
            if func_name != "w_avg":
                func = getattr(F, func_name)
                aggregation = func(F.col(col_name))
            else:
                aggregation = w_avg(col_name, col_weight)

            output_name = f"n_{func_name}_{col_name.replace('n_', '')}"
            if keep_original_names:
                output_name = col_name

            agg_list.append(aggregation.alias(output_name))
    df_agg = df.groupby(cols_group).agg(*agg_list)
    return df_agg


def select_and_rename(
    df: SparkDataFrame,
    rename_dict: dict,
    cols_keep: Optional[List[str]] = [],
    keep_all: Optional[bool] = False,
) -> SparkDataFrame:
    """
    Selects and renames columns according to rename_dict. If cools_to_keep added, extra columns will be mantained
    if keep_all is True, all columns will be conserved
    Args:
        df:
        rename_dict:
        cols_keep:
        keep_all:

    Returns:

    """
    if keep_all:
        cols_keep = df.columns
    for col_name in cols_keep:
        if col_name not in rename_dict.keys():
            rename_dict[col_name] = col_name
    df = df.select([F.col(k).alias(v) for k, v in rename_dict.items()])
    return df


def create_window_by_group(
    cols_group: List[str], col_sort: str, desc: bool = True
) -> Window:
    w = Window.partitionBy(*cols_group)
    if desc:
        w = w.orderBy(F.desc(col_sort))
    else:
        w = w.orderBy(F.asc(col_sort))
    return w


def filter_top_row_by_group(
    df: SparkDataFrame,
    cols_group: List[str],
    col_sort: str,
    desc: bool = True,
    resolve_conflicts: bool = True,
) -> SparkDataFrame:
    """
    The function groups by cols_group and then sorts by col_sort, finally selects the first row per group.
    If there is a tie, a random row is selected from those that tied
    Args:
        df:
        cols_group:
        col_sort:
        desc:
        resolve_conflicts

    Returns:

    """

    w = create_window_by_group(cols_group, col_sort, desc)
    if resolve_conflicts:
        rank_calc = F.row_number().over(w)
    else:
        rank_calc = F.dense_rank().over(w)
    df = df.withColumn("ranking", rank_calc).filter("ranking == 1")
    df = df.drop("ranking")
    return df


def forward_fill_multiple(
    df: SparkDataFrame,
    col_fill_list: List[str],
    cols_group: List[str],
    col_sort: str,
    desc: bool = True,
):

    for col_fill in col_fill_list:
        df = forward_fill(df, col_fill, cols_group, col_sort, desc)
    return df


def forward_fill(
    df: SparkDataFrame,
    col_fill: str,
    cols_group: List[str],
    col_sort: str,
    desc: bool = True,
) -> SparkDataFrame:

    w = create_window_by_group(cols_group, col_sort, desc)
    w = w.rowsBetween(Window.unboundedPreceding, 0)
    df = df.withColumn(col_fill, F.last(F.col(col_fill), ignorenulls=True).over(w))
    return df


def w_avg(value: str, weight: str):
    numerator = F.sum(F.col(value) * F.col(weight))
    denominator = F.sum(F.when(F.col(value).isNull(), 0).otherwise(F.col(weight)))
    return numerator / denominator


def reduce_to_size(df, max_size=10):
    num_splits = np.int(np.floor(df.count() / max_size))

    df = df.withColumn("split_int", F.floor(num_splits * F.rand()))
    df = df.filter(F.col("split_int") == 1)
    df = df.drop("split_int")
    return df


def transform_to_pandas(df: SparkDataFrame, max_size=500000) -> pd.DataFrame:

    dict_recast = {}
    for col in df.columns:
        if df.schema[col].dataType.typeName() in ["decimal", "double", "float"]:
            dict_recast[col] = "float64"

    num_splits = np.int(np.floor(df.count() / max_size))

    if num_splits == 0:
        df_out = df.toPandas()

    else:
        df = df.withColumn("split_int", F.floor(num_splits * F.rand()))
        df = df.repartition(num_splits, "split_int")
        df.cache().count()

        df_list = []
        for i in range(num_splits):
            df_local = df.filter(F.col("split_int") == i).toPandas()
            df_local = df_local.drop(columns="split_int")
            df_list.append(df_local)

        df_out = pd.concat(df_list, ignore_index=True)

    for col in dict_recast.keys():
        df_out[col] = df_out[col].astype(dict_recast[col])

    return df_out


def get_sum_nulls_nans_per_row(
    df, list_columns: List[str], col_out: str = "sum_nulls_nans"
):
    """
    Helper function that creates columns with True/False for each column in list_columns, True if it's NaN/null/None
    value, False otherwise
    Args:
        df:
        list_columns:
        col_out

    Returns:

    """

    df = df.withColumn(
        col_out, sum([F.col(var).isNull().cast("int") for var in list_columns])
    )
    return df


def create_top_n_values_by_group(
    df, col_groups: List[str], top_n: int, col_sort: str, desc: bool = True
):
    w = create_window_by_group(col_groups, col_sort, desc)
    df = df.withColumn("ranking", F.row_number().over(w)).filter(
        F.col("ranking") <= top_n
    )

    cols = [col for col in df.columns if (col not in col_groups) & (col != "ranking")]
    top_cols = [f"{col}_top{i+1}" for i in range(top_n) for col in cols]

    for i in range(top_n):
        for col in cols:
            df = df.withColumn(
                f"{col}_top{i+1}",
                F.when(F.col("ranking") == i + 1, F.col(col)).otherwise(F.lit(None)),
            )

    top_agg_df = group_by_dict(
        df, col_groups, {x: "max" for x in top_cols}, keep_original_names=True
    )

    return top_agg_df
