# DS4B 101-P: PYTHON FOR DATA SCIENCE AUTOMATION ----
# Module 7 (Plotnine): Plotnine Deep-Dive ----

# Imports
from mizani.breaks import date_breaks
from mizani.formatters import dollar_format
import pandas as pd
import numpy as np
import matplotlib


from plotnine import aes
from plotnine.coords.coord_flip import coord_flip
from plotnine.facets.facet_grid import facet_grid
from plotnine.facets.facet_wrap import facet_wrap
from plotnine.geoms import geom_col
from plotnine.geoms.geom_boxplot import geom_boxplot
from plotnine.geoms.geom_density import geom_density
from plotnine.geoms.geom_histogram import geom_histogram
from plotnine.geoms.geom_jitter import geom_jitter
from plotnine.geoms.geom_label import geom_label
from plotnine.geoms.geom_line import geom_line
from plotnine.geoms.geom_point import geom_point
from plotnine.geoms.geom_smooth import geom_smooth
from plotnine.geoms.geom_text import geom_text
from plotnine.geoms.geom_violin import geom_violin
from plotnine.ggplot import ggplot
from plotnine.labels import labs
from plotnine.scales.limits import expand_limits
from plotnine.scales.scale_color import scale_color_brewer, scale_color_cmap_d, scale_color_gradient
from plotnine.scales.scale_manual import scale_color_manual
from plotnine.scales.scale_xy import scale_x_datetime, scale_y_continuous
from plotnine.themes import theme
from plotnine.themes.elements import element_rect
from plotnine.themes.theme_dark import theme_dark
from plotnine.themes.theme_matplotlib import theme_matplotlib
from plotnine.themes.theme_minimal import theme_minimal

from my_pandas_extensions.database import collect_data
from my_pandas_extensions.timeseries import summarize_by_time

import plotnine
from plotnine import *

# Matplotlib stylings


# Data
df = collect_data()


# 1.0 Scatter Plots ----
# - Great for Continuous vs Continuous

# Goal: Explain relationship between order line value
#  and quantity of bikes sold

# Step 1: Data Manipulation
quantity_total_price_by_order_df = df[['order_id', 'quantity', 'total_price']] \
    .groupby('order_id') \
    .sum() \
    .reset_index()

# Step 2: Data Visualization

(
    ggplot(
        mapping= aes('quantity', 'total_price'),
        data   = quantity_total_price_by_order_df
    )
    + geom_point(alpha = 0.5) 
    + geom_smooth(method = 'lm')
)



# 2.0 Line Plot ----
# - Great for time series

# Goal: Describe revenue by Month, expose cyclic nature

# Step 1: Data Manipulation

bike_sales_m_df = df \
    .summarize_by_time(
        date_column  = 'order_date',
        value_column = 'total_price',
        rule         = "M",
        kind         = 'timestamp'
    ) \
    .reset_index()


# Step 2: Plot

(
    ggplot(
        mapping = aes('order_date', 'total_price'),
        data    = bike_sales_m_df
    )

    + geom_line()
    + geom_smooth(method = 'lm', se = False)
    + geom_smooth(
        method = 'loess', 
        se = False, 
        span = 0.2,
        color = "dodgerblue"
    )
)


# 3.0 Bar / Column Plots ----
# - Great for categories

# Goal: Sales by Descriptive Category

# Step 1: Data Manipulation

from plydata.cat_tools import cat_reorder

bike_sales_cat2_df = df \
    .groupby('category_2') \
    .agg(
        {'total_price': np.sum}
    ) \
    .reset_index() \
    .sort_values('total_price', ascending=False) \
    .assign(
        category_2 = lambda x: cat_reorder(
            x['category_2'], x['total_price'],
            ascending=True
        )
    ) \
    .sort_values('category_2')


# Aside: Categorical Data (pd.Categorical)
# - Used frequently in plotting to designate order of categorical data

bike_sales_cat2_df.info()
bike_sales_cat2_df.category_2
bike_sales_cat2_df.category_2.cat.codes

# Step 2: Plot

(
    ggplot(
        mapping = aes('category_2', 'total_price'),
        data    = bike_sales_cat2_df
    ) 

    + geom_col(fill = "#2c3e50", color = "white")
    + coord_flip()
    + theme_minimal()
)



# 4.0 Histogram / Density Plots ----
# - Great for inspecting the distribution of a variable

# Goal: Unit price of bicycles

# Histogram ----

# Step 1: Data Manipulation

unit_price_by_frame_df = df[['model', 'frame_material', 'price']] \
    .drop_duplicates()


# Step 2: Visualize

g_canvas = ggplot(
    data = unit_price_by_frame_df,
    mapping=aes('price', fill = "frame_material")
) 

g1 = g_canvas + geom_histogram(bins = 25, color = "white", fill = "#2c3e50")

g2 = g_canvas + geom_histogram(bins = 25, color = "white")

g2 + facet_grid(facets=[".", "frame_material"])

g2 + facet_grid(["frame_material", "."])

# Density ----

g3 = g_canvas + geom_density(alpha = 0.5)

g3 + facet_wrap("frame_material", ncol = 1)

# 5.0 Box Plot / Violin Plot ----
# - Great for comparing distributions

# Goal: Unit price of model, segmenting by category 2

# Step 1: Data Manipulation

unit_price_by_cat2_df = df[['category_2', 'model', 'price']] \
    .drop_duplicates() \
    .assign(
        category_2 = lambda x: cat_reorder(
            x['category_2'], x['price'],
            fun = np.median,
            ascending=True
        )
    )

unit_price_by_cat2_df.info()
unit_price_by_cat2_df.category_2.cat.codes

# Step 2: Visualize

# Box Plot

(
    ggplot(aes('category_2', 'price'), unit_price_by_cat2_df)
    + geom_boxplot()
    + coord_flip()
)


# Violin Plot & Jitter Plot

(
    ggplot(aes('category_2', 'price'), unit_price_by_cat2_df )

    + geom_violin()
    + geom_jitter(width = 0.15, alpha = 0.5)
    + coord_flip()
)


# 6.0 Adding Text & Label Geometries----

# Goal: Exposing sales over time, highlighting outlier

# Data Manipulation

usd = dollar_format(prefix="$", big_mark=",", digits=0)

usd([100, 1000, 1e10])

bike_sales_y_df = df \
    .summarize_by_time(
        date_column = "order_date",
        value_column = "total_price",
        rule         = "Y"
    ) \
    .reset_index() \
    .assign(
        total_price_text = lambda x: usd(x['total_price'])
    )


# Adding text to bar chart
# Filtering labels to highlight a point

(
    ggplot(aes(x ='order_date', y = 'total_price'), bike_sales_y_df) 

    + geom_col(fill = "#2C3E50") 
    + geom_smooth(
        method = "lm",
        se     = False,
        color  = 'dodgerblue'
    )

    + geom_text(
        aes(label    = 'total_price_text'),
        va       = "top",
        size     = 8,
        nudge_y  = -1.2e5,
        color    = "white"
    )

    + geom_label(
        label   = "Major Demand",
        color   = "red",
        nudge_y = 1e6,
        size    = 10,
        data = bike_sales_y_df[
            bike_sales_y_df.order_date.dt.year == 2013
        ]
    )

    + expand_limits(y = [0, 20e6]) 
    + scale_x_datetime(date_labels = "%Y")
    + scale_y_continuous(labels = usd)

    + theme_minimal()
)


# 7.0 Facets, Scales, Themes, and Labs ----
# - Facets: Used for visualizing groups with subplots
# - Scales: Used for transforming x/y axis and colors/fills
# - Theme: Used to adjust attributes of the plot
# - Labs: Used to adjust title, x/y axis labels

# Goal: Monthly Sales by Categories

# Step 1: Format Data
bike_sales_cat2_m_df = df \
    .summarize_by_time(
        date_column = 'order_date',
        value_column = 'total_price',
        groups       = 'category_2',
        rule         = "M",
        wide_format  = False
    ) \
    .reset_index()

# Step 2: Visualize

matplotlib.pyplot.style.available

matplotlib.pyplot.style.use('default')

matplotlib.pyplot.style.use('dark_background')

g = (
    ggplot(
        aes('order_date', 'total_price', color = 'category_2'),
        data = bike_sales_cat2_m_df
    )

    + geom_line()
    + geom_smooth(
        span  = 0.2,
        se    = False,
        color = "dodgerblue"
    )

    + facet_wrap("category_2", ncol = 3, scales="free_y")

    + scale_x_datetime(
        date_labels = "%Y",
        date_breaks = "2 years"
    )

    + scale_y_continuous(
        labels = usd
    )

    + scale_color_cmap_d() 

    + theme_matplotlib()

    + theme(
        strip_background = element_rect(fill = "black"),
        legend_position  = "none",
        figure_size      = (16, 8),
        subplots_adjust  = {'wspace': 0.25}
        # legend_background= element_rect(fill = "white")
    )

    + labs(
        title = "Revenue by Month and Category 2",
        x     = "Date",
        y     = "Revenue"
        
    )
)

g.save("07_visualization/bike_sales_cat2_m_df.jpg")






