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

'''
hierarchy:

1. Pandas data frame
2. Pandas series
3. Numpy arrays
'''
# - PANDAS DATA FRAME

type(df)

# - PANDAS SERIES

type(df.order_date)

df['order_date'].dt.year
df.dt.year #error - doesn't work because a dataframe doesnt have this "dt" attribute

# - NUMPY

df['order_date'].values # series formed by numpy arrays 
type(df['order_date'].values)
type(df['order_date'].values).mro

# - DATA TYPES

df['price'].values
type(df['price'].values)
type(df['price'].values).mro
df['price'].values.dtype
df['order_date'].values.dtype

for i in df.columns:
    print(df[i].values.dtype)

# Example 1: Covert a numpy array to a dataframe
#  
# I create a numpy array
numpy_array= np.array([6070, 5970, 2770, 1680, 2880, 3200])
numpy_array
type(numpy_array)

#The np array is converted to a pd series
pandas_series = pd.Series(numpy_array)
pandas_series
type(pandas_series)

# The pd series is converted to a pd DataFrame
pandas_dataframe = pd.DataFrame(pandas_series)
pandas_dataframe
type(pandas_dataframe)

# The np array can be converted to a pd DataFrame without being previously transformed to a pd series
pandas_dataframe_2 = pd.DataFrame(numpy_array)
pandas_dataframe_2
type(pandas_dataframe_2)

# Example 2: Convert a dataframe to a numpy array

# I extract a column as a dataframe (instead of a series)
pandas_dataframe_3 = pd.DataFrame(df.price)
pandas_dataframe_3
type(pandas_dataframe_3)

# The dataframe is converted to a series
pandas_series_2 = pandas_dataframe_3.price
pandas_series_2
type(pandas_series_2)

# The series is converted to a numpy array
numpy_array_2 = pandas_series_2.to_numpy()
numpy_array_2
type(numpy_array_2)

# A dataframe is converted directly to a numpy array
numpy_array_3 = pandas_dataframe_3.to_numpy()
numpy_array_3
type(numpy_array_3)

# 3.0 DATA STRUCTURES - PYTHON

# DICTIONARIES

d = {'a' : 1}
d
type(d)

d.keys() # keys are identifiers in the dict

d.values() # values are the data assigned to the key

d['a'] # we can select the values from a key (similar to a pd dataframe)

# LISTS: 
# 
# un-keyed dictionaries. Are commonly used for iteration

l = [1, "A", [2, "B"]]
l[0] # access to list items by their index location
l[1]
l[2]

list(d.values()) # it returns a list, and we can extract values from that
list(d.values())[0]

# TUPLES: 
# 
# an immutable list. Used in pandas for storing data frame shape and multi-index column names

df.shape # uses parenthesis

type(df.shape).mro()

t = (10, 20)

t[0]

t[0] = 99999 # error: we cannot change the element


# BASE DATA TYPES

type(1.5).mro() # float: number with decimal

type(1).mro() # int: number without decimal

df.price.values
df.price.dtype

type(df.model[0]) # str: string 
type('Jekyll Carbon 2') 

# CASTING

price = 6070	
model = 'Jekyll Carbon 2'

f"The first model is: {model}, and its price is: {price}" # this converts the numerical values to a string

price + 'Jekyll Carbon 2' # gives an error since price is numerical (int)
type(price)

str(price) +'Jekyll Carbon 2' # it can now be combined since price was converted to a string 
str(price)
type(str(price))

"50%" # str "50%"
"50%".replace("%", "") # str "50"
int("50%".replace("%", "")) # num 50

# range() : makes a range object that defines how to generate a sequence of numbers.
#
# Range is a generator. It produces a specification for how to generate the sequence (only creates the range when you need it)

range(1, 51)
type(range(1, 50)).mro() # range object

# we can activate the range we used on a function. Say list()
# 

r = list(range(1, 51)) # first 50 numbers 

np.array(r) #convert to an array

pd.Series(r) #convert to a series

pd.DataFrame(r) #convert to a dataframe

# Coverting Column data types:

df['order_date'].astype('str').str.replace("-","/")  #astype converts a series to another dtype

