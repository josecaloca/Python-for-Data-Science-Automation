# DS4B 101-P: PYTHON FOR DATA SCIENCE AUTOMATION ----
# Module 6 (Sktime): ARIMA Automation ----

# Imports

import pandas as pd
import numpy as np

from my_pandas_extensions.database import collect_data
from my_pandas_extensions.timeseries import summarize_by_time

from sktime.forecasting.arima import AutoARIMA

from tqdm import tqdm

# Workflow

df = collect_data()

bike_sales_m_df = df \
    .summarize_by_time(
        date_column = 'order_date',
        value_column = 'total_price',
        rule = "M",
        kind = 'period'
    )

bike_sales_cat2_m_df = df \
    .summarize_by_time(
        date_column = 'order_date',
        value_column = 'total_price',
        groups = ['category_2'],
        rule = 'M',
        kind = 'period'
    )


# FUNCTION DEVELOPMENT ----
# - arima_forecast(): Generates ARIMA forecasts for one or more time series.

# ?AutoARIMA

data = bike_sales_cat2_m_df
h = 12
sp = 1
alpha = 0.05
suppress_warnings = True

def arima_forecast(
    data, h, sp, alpha = 0.05, 
    suppress_warnings = True, 
    *args, **kwargs
    ):

    # Checks

    # Handle Inputs ----
    df = data

    # FOR LOOP ----

    model_results_dict = {}
    for col in tqdm(df.columns, mininterval=0):

        # Series Extraction
        y = df[col]

        # Modeling
        forecaster = AutoARIMA(
            sp = sp, 
            suppress_warnings = suppress_warnings,
            *args, 
            **kwargs
        )

        forecaster.fit(y)

        # Predictions & Conf Intervals

        predictions, conf_int_df = forecaster.predict(
            fh              = np.arange(1, h+1),
            return_pred_int = True,
            alpha           = alpha 
        )

        # Combine into data frame
        ret = pd.concat([y, predictions, conf_int_df], axis=1)
        ret.columns = ["value", "prediction", "ci_lo", "ci_hi"]

        # Update Dictionary
        model_results_dict[col] = ret

    # Stack Each Dict Element on Top of Each Other
    model_results_df = pd.concat(
        model_results_dict, 
        axis=0
    )

    # Handle Names
    nms = [*df.columns.names, *df.index.names]
    model_results_df.index.names = nms

    # Reset Index
    ret = model_results_df.reset_index()

    # Drop columns containing "level"
    cols_to_keep = ~ret.columns.str.startswith("level_")

    ret = ret.iloc[:, cols_to_keep]

    return ret

fcast = arima_forecast(data, h = 12, sp = 1)

fcast.reset_index()

df.columns.names
df.index.names

nms = [*df.columns.names, *df.index.names]

arima_forecast(
    bike_sales_m_df,
    h = 12, 
    sp = 1
)

arima_forecast(
    bike_sales_cat2_m_df,
    h = 12, 
    sp = 1
)


# Import Test

from my_pandas_extensions.forecasting import arima_forecast

forecast_df = bike_sales_cat2_m_df \
    .arima_forecast(
        h  = 12, 
        sp = 1
    ) 
    
forecast_df \
    .groupby('category_2') \
    .plot(x = 'order_date')

