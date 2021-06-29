# DS4B 101-P: PYTHON FOR BUSINESS ANALYSIS ----
# Module 2 (Pandas Import): Importing Files ----

# IMPORTS ----

# %%
import pandas as pd

# %%
# 1.0 FILES ----

# - Pickle ----
# It is better to save pandas dataframes as pickle for python-related issues

pickle_df = pd.read_pickle("./00_data_wrangled/bike_orderlines_wrangled_df.pkl")
pickle_df.info() # it keeps the datetime64 Dtype
# - CSV ----

csv_df = pd.read_csv("./00_data_wrangled/bike_orderlines_wrangled_df.csv")
csv_df.info() # Reading CSV don't keep the exact format as the python objects that created them. Unless it is deparsed

csv_df = pd.read_csv(
    "./00_data_wrangled/bike_orderlines_wrangled_df.csv",
    parse_dates=['order_date'])

csv_df.info()
# - Excel ----
# loading a excel file is slower than CSV
excel_df = pd.read_excel("00_data_wrangled/bike_orderlines_wrangled_df.xlsx")
excel_df.info()
