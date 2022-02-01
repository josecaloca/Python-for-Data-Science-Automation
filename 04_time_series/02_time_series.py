# DS4B 101-P: PYTHON FOR BUSINESS ANALYSIS ----
# Module 4 (Time Series): Working with Time Series Data ----

# IMPORTS

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from my_pandas_extensions.database import collect_data

# DATA

df = collect_data()

# 1.0 DATE BASICS

df['order_date']


# Conversion

type("2011-01-07")

pd.to_datetime("2011-01-07") \
    .to_period(freq="W") \
    .to_timestamp()

# Accessing elements

df.order_date

# Months
df.order_date.dt.month
df.order_date.dt.month_name()

# Days
df.order_date.dt.day
df.order_date.dt.day_name()

# Year
df.order_date.dt.year

# DATE MATH

import datetime 

today = datetime.date.today()

pd.to_datetime(today + pd.Timedelta("1 day"))

df.order_date + pd.Timedelta("1Y")

df.order_date + pd.Timedelta("30 min")


# Duration (TimeDeltas)

today = datetime.date.today()

one_year_from_today = today + pd.Timedelta("1Y")

(one_year_from_today - today) / pd.Timedelta("1W")

pd.Timedelta(one_year_from_today - today) / np.timedelta64(1, "M")

pd.Timedelta(one_year_from_today - today) / pd.Timedelta("1M") # This gives minutes



# DATE SEQUENCES

pd.date_range(
    start   = pd.to_datetime("2011-01"),
    periods = 10,
    freq    = "2D"
)

pd.date_range(
    start   = pd.to_datetime("2011-01"),
    end     = pd.to_datetime("2011-12-31"),
    freq    = "1W"
)

# PERIODS
# - Periods represent timestamps that fall within an interval using a frequency.
# - IMPORTANT: {sktime} requires periods to model univariate time series


# Convert to Time Stamp

df.order_date.dt.to_period(freq = "D")

df.order_date.dt.to_period(freq = "W")

df.order_date.dt.to_period(freq = "M")

df.order_date.dt.to_period(freq = "Q")

df.order_date.dt.to_period(freq = "Y")

# Get the Frequency

df.order_date.dt.to_period(freq = "Q").dt.freq

df.order_date.dt.to_period(freq = "Y").dt.freq

# Conversion to Timestamp

df.order_date.dt.to_period(freq = "M").dt.to_timestamp()

df.order_date.dt.to_period(freq = "Q").dt.to_timestamp()



# TIME-BASED GROUPING (RESAMPLING)
# - The beginning of our Summarize by Time Function

# Single Time Series. Using kind = "timestamp"

bike_sales_m_df = df[['order_date', 'total_price']] \
    .set_index("order_date") \
    .resample("MS", kind = "timestamp") \
    .sum()

bike_sales_m_df
    

# Grouped Time Series. Using kind = "period" 
# - Were we had trouble with overlapping time stamps,
#   which required an extra step to convert to period. 

bike_sales_cat2_m_wide_df = df[['category_2', 'order_date', 'total_price']] \
    .set_index('order_date') \
    .groupby('category_2') \
    .resample('M', kind = 'period') \
    .agg(np.sum) \
    .unstack("category_2") \
    .reset_index() \
    .assign(order_date = lambda x: x['order_date'].dt.to_period()) \
    .set_index("order_date")

bike_sales_cat2_m_wide_df


# MEASURING CHANGE

# Difference from Previous Timestamp

#  - Single (No Groups)

bike_sales_m_df \
    .assign(total_price_lag1 = lambda x: x['total_price'].shift(1)) \
    .assign(diff = lambda x: x.total_price - x.total_price_lag1 ) \
    .plot(y = 'diff')

bike_sales_m_df \
    .apply(lambda x: ( x - x.shift(1) ) / x.shift(1)) \
    .plot()


#  - Multiple Groups: Key is to use wide format with apply

bike_sales_cat2_m_wide_df \
    .apply(lambda x: ( x - x.shift(1) ) / x.shift(1) ) \
    .plot()


#  - Difference from First Timestamp

bike_sales_m_df \
    .apply(lambda x: (x - x[0]) / x[0]) \
    .plot()

bike_sales_cat2_m_wide_df \
    .apply(lambda x: (x - x[0]) / x[0]) \
    .plot()


# CUMULATIVE CALCULATIONS

bike_sales_m_df \
    .resample('YS') \
    .sum() \
    .cumsum() \
    .reset_index() \
    .assign(order_date = lambda x: x.order_date.dt.to_period()) \
    .set_index("order_date") \
    .plot(kind = "bar")

bike_sales_cat2_m_wide_df \
    .resample("Y") \
    .sum() \
    .cumsum() \
    .plot(kind = "bar", stacked = True)

# ROLLING CALCULATIONS

# Single

bike_sales_m_df.plot()

bike_sales_m_df['total_price'] \
    .rolling(
        window = 12
    ) \
    .mean()

bike_sales_m_df \
    .assign(
        total_price_roll12 = lambda x: x['total_price'] \
            .rolling(
                window = 24,
                center = True,
                min_periods = 1
            ) \
            .mean()
    ) \
    .plot()

# Groups - Can't use assign(), we'll use merging

bike_sales_cat2_m_wide_df \
    .apply(
        lambda x: x.rolling(
            window = 24, 
            center = True, 
            min_periods = 1
        ) \
        .mean()
    ) \
    .rename(lambda x: x + "_roll_24", axis = 1) \
    .merge(
        bike_sales_cat2_m_wide_df,
        how = "right",
        left_index = True, 
        right_index = True
    ) \
    .plot()


