

import pandas as pd
import numpy as np

import pandas_flavor as pf

@pf.register_dataframe_method
def summarize_by_time(
    data, date_column, value_column, 
    groups = None, 
    rule   = "D",
    agg_func = np.sum, 
    kind     = "timestamp",
    wide_format = True, 
    fillna = 0,
    *args,
    **kwargs 
):
    """
    Applies one or more aggregating functions by a Pandas Period or TimeStamp to one or more numeric columns. 

    Args:
        data ([Pandas DataFrame]): 
            A pandas data frame with a date column and value column. 
        date_column ([str]): 
            The name of a single date or datetime column to be aggregated by. Must be datetime64.
        value_column ([str, list]): 
            The names of one or more value columns to be aggregated by. 
        groups ([str, list, None], optional): 
            One or more column names representing groups to aggregate by. Defaults to None.
        rule (str, optional): 
            A pandas frequency (offset) such as "D" for Daily or "MS" for Month Start. Defaults to "D".
        agg_func ([function, list], optional): 
            One or more aggregating functions such as np.sum. Defaults to np.sum.
        kind (str, optional): 
            One of "timestamp" or "period". Defaults to "timestamp".
        wide_format (bool, optional): 
            Whether or not to return "wide" or "long" format. Defaults to True.
        fillna (int, optional): 
            Value to fill in missing data. Defaults to 0. If missing values are desired, use np.nan.
        *args, **kwargs: 
            Arguments passed to pd.DataFrame.agg()

    Returns:
        [Pandas DataFrame]: A data frame that is summarized by time. 
    """

    # CHECKS

    if (type(data) is not pd.DataFrame):
        raise TypeError("`data` is not Pandas Data Frame.")

    if type(value_column) is not list:
        value_column = [value_column]
    
    # BODY 

    # Handle date column
    data = data.set_index(date_column)

    # Handle groupby
    if groups is not None:
        data = data.groupby(groups)

    # Handle resample
    data = data.resample(
        rule = rule,
        kind = kind
    )

    # Handle aggregation
    function_list = [agg_func] * len(value_column)
    agg_dict      = dict(zip(value_column, function_list))

    data = data \
        .agg(
            func = agg_dict,
            *args,
            **kwargs 
        )

    # Handle Pivot Wider 
    if wide_format:
        if groups is not None:
            data = data.unstack(groups)
            if (kind == 'period'):
                data.index = data.index.to_period()

    data = data.fillna(value = fillna)

    return data
