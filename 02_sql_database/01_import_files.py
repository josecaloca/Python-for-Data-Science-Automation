# DS4B 101-P: PYTHON FOR DATA SCIENCE AUTOMATION ----
# SQL DATABASES (Module 2): Importing Files ----

# IMPORTS ----

import pandas as pd


# 1.0 FILES ----

# - Pickle ----

pickle_df = pd.read_pickle("./00_data_wrangled/bike_orderlines_wrangled_df.pkl")

pickle_df.info()

# - CSV ----

csv_df = pd.read_csv("./00_data_wrangled/bike_orderlines_wrangled_df.csv", parse_dates=['order_date'])

csv_df.info()

# - Excel ----

excel_df = pd.read_excel("./00_data_wrangled/bike_orderlines_wrangled_df.xlsx")

excel_df.info()




