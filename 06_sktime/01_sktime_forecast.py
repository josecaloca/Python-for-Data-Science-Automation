# DS4B 101-P: PYTHON FOR DATA SCIENCE AUTOMATION ----
# Module 6 (Sktime): Introduction to Forecasting ----

# Imports

import pandas as pd
import numpy as np
from pandas.core.frame import DataFrame

from my_pandas_extensions.database import collect_data
from my_pandas_extensions.timeseries import summarize_by_time

df = collect_data()

# Sktime Imports
from sktime.forecasting.arima import AutoARIMA
from sktime.utils.plotting import plot_series

# Progress Bars
from tqdm import tqdm

# ?tqdm
# ?AutoARIMA

# 1.0 DATA SUMMARIZATIONS ----
# ?pd.DataFrame.summarize_by_time
# ?summarize_by_time
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


# 2.0 SINGLE TIME SERIES FORECAST ----

bike_sales_m_df.plot()

bike_sales_m_df

y = bike_sales_m_df['total_price']

forecaster = AutoARIMA(sp = 12)

forecaster.fit(y)

# Predictions
h = 24
forecaster.predict(fh = np.arange(1,h+1) )


# Confidence Intervals
predictions_series, conf_int_df = forecaster.predict(
    fh              = np.arange(1,h+1),
    return_pred_int = True, 
    alpha           = 0.05
)

# type(predictions_ci_tuple)
# predictions_ci_tuple[1]

predictions_series
conf_int_df

# Visualize

# ?plot_series

plot_series(
    y,
    predictions_series,
    conf_int_df['lower'],
    conf_int_df['upper'],
    labels=['actual', 'predictions', 'ci_lower', 'ci_upper']
)



# 3.0 MULTIPLE TIME SERIES FORCAST (LOOP) ----

bike_sales_cat2_m_df.head()

df = bike_sales_cat2_m_df

df.columns[1]

df[df.columns[2]]

model_results_dict = {}
for col in tqdm(df.columns):
    
    # Series Extraction

    y = df[col]

    # Modeling

    forecaster = AutoARIMA(
        # TODO Note: Change to 12 for Monthly
        sp = 12, 
        suppress_warnings = True
    )

    forecaster.fit(y)

    h = 12

    # Predictions and Conf Intervals

    predictions, conf_int_df = forecaster.predict(
        fh              = np.arange(1, h+1),
        return_pred_int = True,
        alpha           = 0.05
    )

    # Combine into data frame
    ret = pd.concat([y, predictions, conf_int_df], axis=1)
    ret.columns = ["value", "prediction", "ci_lo", "ci_hi"]

    # Update dictionary
    model_results_dict[col] = ret

model_results_dict.keys()
model_results_dict[('total_price', 'Cross Country Race')]

model_results_df = pd.concat(model_results_dict, axis=0)

# Visualize
model_results_dict[('total_price', 'Cross Country Race')].plot()

model_results_dict[ list(model_results_dict.keys())[0] ].plot()


