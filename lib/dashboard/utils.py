import bokeh
import os

import bokeh
from bokeh.palettes import Category20 as bokeh_palette
from bokeh.plotting import figure
from bokeh.models import HoverTool
import bokeh.plotting as bokeh_plotting
import numpy as np
import pandas as pd


def style_plot(p):
    # Title
    p.title.align = 'center'
    p.title.text_font_size = '20pt'
    p.title.text_font = 'serif'

    # Axis titles
    p.xaxis.axis_label_text_font_size = '14pt'
    p.xaxis.axis_label_text_font_style = 'bold'
    p.yaxis.axis_label_text_font_size = '14pt'
    p.yaxis.axis_label_text_font_style = 'bold'

    # Tick labels
    p.xaxis.major_label_text_font_size = '10pt'
    p.yaxis.major_label_text_font_size = '10pt'

    return p


def plot_variables(data, var_names, x_axis,
                   h_lines={}, plot_width=1000, plot_height=300):
    print(data)
    plot_tools = 'pan,box_zoom,undo,reset,save'
    palette = bokeh_palette[max([3, len(var_names)])]
    p = []

    for _iv, _v in enumerate(var_names):

        legend_it = []
        if _iv == 0:
            p.append(bokeh.plotting.figure(plot_width=plot_width,
                                           plot_height=plot_height,
                                           x_axis_type='datetime',
                                           tools=plot_tools))
        else:
            p.append(bokeh.plotting.figure(plot_width=plot_width,
                                           plot_height=plot_height,
                                           x_range=p[0].x_range,
                                           x_axis_type='datetime',
                                           tools=plot_tools))

        c = p[_iv].line(x=x_axis, y=_v, color=palette[_iv], source=data)

        if _v in h_lines:
            heights = h_lines[_v]
            print(_v)
            print(heights)
            for height in heights:
                p[_iv].line(x=[data[x_axis].iloc[0], data[x_axis].iloc[-1]],
                            y=[height, height], color='black', line_alpha=0.8)

        legend_it.append((_v, [c]))

        p[_iv].xaxis.formatter = bokeh.models.DatetimeTickFormatter(days=["%d/%m/%y"])

        style_plot(p[_iv])

        legend = bokeh.models.Legend(items=legend_it, location=(0, +10), orientation='horizontal')
        legend.location = 'center'
        legend.label_text_font_size = '12pt'
        p[_iv].add_layout(legend, 'above')

        tooltips = [('index', '@index'),
                    (x_axis, f'@{{{x_axis}}}{{%d-%m-%Y %H:%M:%S}}'),
                    (_v, f'@{{{_v}}}')]
        formatters = {x_axis: 'datetime'}
        ht = HoverTool(tooltips=tooltips, formatters=formatters)
        p[_iv].add_tools(ht)

    return bokeh.layouts.column(p)
