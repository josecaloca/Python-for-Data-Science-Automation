# DS4B 101-P: PYTHON FOR DATA SCIENCE AUTOMATION ----
# SQL DATABASES (Module 2): Testing the collect_data() function ----

import pandas as pd

from my_pandas_extensions.database import collect_data

collect_data(conn_string="sqlite:///00_database/bike_orders_database.sqlite")

