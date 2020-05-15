from bokeh.layouts import row, column
from bokeh.models import Panel
import pandas as pd
from lib.dashboard.utils import plot_variables


def emocromocitometrici_tab(dataset: pd.DataFrame, limits=None):
    print('Creating tab')
    plot_var = dataset.columns
    dataset = dataset.reset_index()

    h_lines = dict(zip(limits['Esame'], list(zip(limits['Inf. ref'], limits['Sup. ref']))))
    plots = plot_variables(data=dataset, var_names=plot_var, x_axis='Data Referto', h_lines=h_lines)
    print('Created plots')
    # Create a row layout
    # layout = row(controls, column(p2, p1))
    # layout = column(plots)
    # Make a tab with the layout
    tab = Panel(child=plots, title='Esami emocromocitometrici')
    print(tab)
    print('Returning tab')
    return tab
