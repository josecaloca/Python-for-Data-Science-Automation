# DS4B 101-P: PYTHON FOR DATA SCIENCE AUTOMATION ----
# Module 3 (Pandas Core): Data Structures ----

# IMPORTS ----

import pandas as pd
import numpy as np

from my_pandas_extensions.database import collect_data

df = collect_data()

df


# 1.0 HOW PYTHON WORKS - OBJECTS

# Objects

type(df)


# Objects have classes

type(df).mro()

type("string").mro()


# Objects have attributes

df.shape

df.columns



# Objects have methods

df.query("model == 'Jekyll Carbon 2'")


# 2.0 KEY DATA STRUCTURES FOR ANALYSIS

# - PANDAS DATA FRAME

type(df)


# - PANDAS SERIES

type(df['order_date'])

df['order_date'].dt.year

df.dt

# - NUMPY ARRAY

type(df['order_date'].values).mro()

df['order_date'].values.dtype

# - Data Types

df['price'].values.dtype




# 3.0 DATA STRUCTURES - PYTHON

# Dictionaries

d = {'a':1}

type(d)

d.keys()

d.values()

d['a']


# Lists

l = [1, "A", [2, "B"]]

l[0]
l[1]
l[2]

list(d.values())[0]

# Tuples

type(df.shape).mro()

t = (10, 20)

t[0] = 20


# Base Data Types

type(1.5).mro()

type(1)

df.total_price.values

type(df['model'].values[0])

type("Jekyll Carbon 2")


# Casting

model = "Jekyll Carbon 2"
price = 6070

f"The first model is: {model}"

f"The price of the first model: {price}"

str(price) + " Some Text"

str(1.0)

int("50%".replace("%", ""))

# Go from Low Level to High-Level through Casting

type(range(1, 50)).mro()

r = list(range(1,51))

np.array(r)

pd.Series(r).to_frame()

# Converting Column Data types

df['order_date'].astype('str').str.replace("-", "/")


