from pyspark.sql import DataFrame as SparkDataFrame
from pyspark.sql import functions as pyspark_functs
from pyspark.sql import types as PySparkTypes


class PysparkFunctions:
    """
    WHY WE NEED THIS: this is purely to simplify the life of the developer.
    If your IDE is properly setup, you probably see the functions below are highlighted
    as 'reference not found' and may cause some typing/linting errors in your IDE.

    This is a workaround for the problem described here:
    https://stackoverflow.com/questions/45367885/unresolved-reference-while-trying-to-import-col-from-pyspark-sql-functions-in-py

    We are basically allowing PyCharm to make "false errors" here in one place
    rather than having these highlights all over the code logic
    """

    sum = pyspark_functs.sum
    col = pyspark_functs.col
    max = pyspark_functs.max
    sqrt = pyspark_functs.sqrt
    min = pyspark_functs.min
    avg = pyspark_functs.avg
    abs = pyspark_functs.abs
    round = pyspark_functs.round
    mean = pyspark_functs.mean
    count = pyspark_functs.count
    pow = pyspark_functs.pow
    approx_count_distinct = pyspark_functs.approx_count_distinct
    when = pyspark_functs.when
    concat = pyspark_functs.concat
    lit = pyspark_functs.lit
    regexp_replace = pyspark_functs.regexp_replace
    PandasUDFType = pyspark_functs.PandasUDFType
    pandas_udf = pyspark_functs.pandas_udf
    split = pyspark_functs.split
    trim = pyspark_functs.trim
    countDistinct = pyspark_functs.countDistinct
    coalesce = pyspark_functs.coalesce
    to_date = pyspark_functs.to_date
    year = pyspark_functs.year
    month = pyspark_functs.month
    last_day = pyspark_functs.last_day
    next_day = pyspark_functs.next_day
    add_months = pyspark_functs.add_months
    dayofweek = pyspark_functs.dayofweek
    dayofmonth = pyspark_functs.dayofmonth
    lpad = pyspark_functs.lpad
    rpad = pyspark_functs.rpad
    substring = pyspark_functs.substring
    hour = pyspark_functs.hour
    to_timestamp = pyspark_functs.to_timestamp
    upper = pyspark_functs.upper
    collect_list = pyspark_functs.collect_list
    struct = pyspark_functs.struct
    udf = pyspark_functs.udf
    last = pyspark_functs.last
    datediff = pyspark_functs.datediff
    least = pyspark_functs.least
    lag = pyspark_functs.lag
    greatest = pyspark_functs.greatest
    first = pyspark_functs.first
    rank = pyspark_functs.rank
    desc = pyspark_functs.desc
    asc = pyspark_functs.asc
    lower = pyspark_functs.lower
    row_number = pyspark_functs.row_number
    broadcast = pyspark_functs.broadcast
    stddev = pyspark_functs.stddev
    collect_set = pyspark_functs.collect_set
    size = pyspark_functs.size
    date_add = pyspark_functs.date_add
    expr = pyspark_functs.expr
    rand = pyspark_functs.rand
    array = pyspark_functs.array
    concat_ws = pyspark_functs.concat_ws
    sha2 = pyspark_functs.sha2
    isnan = pyspark_functs.isnan
    sort_array = pyspark_functs.sort_array
    length = pyspark_functs.length
    format_string = pyspark_functs.format_string
    array_distinct = pyspark_functs.array_distinct
    monotonically_increasing_id = pyspark_functs.monotonically_increasing_id
    isnull = pyspark_functs.isnull
    initcap = pyspark_functs.initcap
    date_format = pyspark_functs.date_format
    asc_nulls_last = pyspark_functs.asc_nulls_last
    regexp_extract = pyspark_functs.regexp_extract
    array_contains = pyspark_functs.array_contains
    format_number = pyspark_functs.format_number
    current_timestamp = pyspark_functs.current_timestamp
    date_sub = pyspark_functs.date_sub
    ceil = pyspark_functs.ceil
    floor = pyspark_functs.floor
    explode = pyspark_functs.explode
    create_map = pyspark_functs.create_map
    array_intersect = pyspark_functs.array_intersect
    array_except = pyspark_functs.array_except
    array_remove = pyspark_functs.array_remove
    flatten = pyspark_functs.flatten
    current_date = pyspark_functs.current_date
    arrays_overlap = pyspark_functs.arrays_overlap
    dense_rank = pyspark_functs.dense_rank
    weekofyear = pyspark_functs.weekofyear
    dayofyear = pyspark_functs.dayofyear
    variance = pyspark_functs.variance
    covar_samp = pyspark_functs.covar_samp
    sqrt = pyspark_functs.sqrt
    percent_rank = pyspark_functs.percent_rank
    from_unixtime = pyspark_functs.from_unixtime
    to_date = pyspark_functs.to_date
    unix_timestamp = pyspark_functs.unix_timestamp
    reverse = pyspark_functs.reverse

# to enable auto-import in PyCharm
SparkDataFrame = SparkDataFrame
F = PysparkFunctions
T = PySparkTypes
