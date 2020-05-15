#!/usr/bin/env python
# coding: utf-8

# In[1]:


from math import pi

import pandas as pd
from bokeh.layouts import row, column
from bokeh.models import HoverTool, ColumnDataSource, Panel, DataTable, TableColumn, DateFormatter
from bokeh.models.widgets import RangeSlider
from bokeh.palettes import RdYlGn
from bokeh.plotting import figure
from bokeh.transform import cumsum


def immunoematologici_tab(dataset: pd.DataFrame):
    src_table = ColumnDataSource(dataset)

    columns = [TableColumn(field=q, title=q) for q in dataset.columns.tolist() if q != 'Data Referto']
    columns.append(TableColumn(field='Data Referto', title='Data Referto', formatter=DateFormatter()))
    table = DataTable(source=src_table, columns=columns, fit_columns=True,
                      selectable=True, sortable=True, width=1000, height=100)

    layout = column(table)

    # Make a tab with the layout
    tab = Panel(child=layout, title='Esami Immunoematologici')

    return tab
