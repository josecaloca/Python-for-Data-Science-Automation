# DS4B 101-P: PYTHON FOR DATA SCIENCE AUTOMATION ----
# SQL DATABASES (Module 2): Working with SQLAlchemy ----

# IMPORTS ----

import pandas as pd
import sqlalchemy as sql

import os 

os.mkdir("./00_database")

# CREATING A DATABASE ----

# Instatiate a database

engine = sql.create_engine("sqlite:///00_database/bike_orders_database.sqlite")

conn = engine.connect()

# Read Excel Files

bikes_df = pd.read_excel("./00_data_raw/bikes.xlsx")
bikeshops_df = pd.read_excel("./00_data_raw/bikeshops.xlsx")
orderlines_df = pd.read_excel("./00_data_raw/orderlines.xlsx")


# Create Tables
bikes_df.to_sql("bikes", con=conn)

pd.read_sql("SELECT * FROM bikes", con=conn)

bikeshops_df.to_sql("bikeshops", con=conn)
pd.read_sql("SELECT * FROM bikeshops", con=conn)

orderlines_df \
    .iloc[: , 1:] \
    .to_sql("orderlines", con=conn, if_exists="replace")

pd.read_sql("SELECT * FROM orderlines", con = conn)


# Close Connection
conn.close()

# RECONNECTING TO THE DATABASE 

# Connecting is the same as creating
engine = sql.create_engine("sqlite:///00_database/bike_orders_database.sqlite")

conn = engine.connect()

# GETTING DATA FROM THE DATABASE

# Get the table names
engine.table_names()

inspector = sql.inspect(conn)

inspector.get_schema_names()

inspector.get_table_names('main')

inspector.get_table_names()

# Read the data
table = inspector.get_table_names()
pd.read_sql(f"SELECT * FROM {table[2]}", con=conn)

# Close connection
conn.close()