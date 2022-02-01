# DS4B 101-P: PYTHON FOR DATA SCIENCE AUTOMATION ----
# Module 4 (Time Series): Profiling Data ----


# IMPORTS

import pandas as pd

from pandas_profiling import ProfileReport, profile_report

from my_pandas_extensions.database import collect_data

df = collect_data()
df


# PANDAS PROFILING

# Get a Profile

profile = ProfileReport(
    df = df
)

profile


# Sampling - Big Datasets

df.profile_report()

df.sample(frac=0.5).profile_report()

df.profile_report(dark_mode = True)


# Pandas Helper
# ?pd.DataFrame.profile_report


# Saving Output

df.profile_report().to_file("04_time_series/profile_report.html")


# VSCode Extension - Browser Preview



