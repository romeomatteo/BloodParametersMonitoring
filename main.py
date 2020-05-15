from lib.exams.blood_exam import BloodExam
from lib.dashboard.emocromocitometrici import emocromocitometrici_tab
from lib.dashboard.immunoematologici import immunoematologici_tab
from pathlib2 import Path
from datetime import datetime

from bokeh.io import curdoc
from bokeh.models.widgets import Tabs
from bokeh.layouts import column

import pandas as pd


def get_ref_dict(ref_dir, template_path):
    referti_files = list(ref_dir.glob('**/referto_raw*.pdf'))
    results = {}
    for referto in referti_files:
        print(referto)
        exam = BloodExam(pdf_path=referto, template_path=template_path)
        date = referto.stem[-8:]
        results[date] = {}
        results[date]['virologico'] = exam.virologico
        results[date]['emocromocitometrico'] = exam.emocromocitometrico
        results[date]['immunoematologici'] = exam.immunoematologici
    return results


def aggregate_referti_dict(ref_dict):
    # compute final dfs
    virologico = None
    emocromocitometrico = None
    immunoematologici = None

    for date in ref_dict.keys():
        date_dt = datetime.strptime(date, '%Y%m%d')

        v = ref_dict[date]['virologico'].copy()
        v['Data Referto'] = date_dt
        virologico = pd.concat([virologico, v], axis=0)

        e = ref_dict[date]['emocromocitometrico'].copy()
        e['Data Referto'] = date_dt
        emocromocitometrico = pd.concat([emocromocitometrico, e], axis=0)

        i = ref_dict[date]['immunoematologici'].copy()
        i['Data Referto'] = date_dt
        immunoematologici = pd.concat([immunoematologici, i], axis=0)

    return virologico, emocromocitometrico, immunoematologici


referti_dir = Path("Referti")
referti_agg_dir = Path("Referti_aggregati")
template_path = Path("RefertoSangue.tabula-template.json")

ref_dict = get_ref_dict(ref_dir=referti_dir, template_path=template_path)

virologici, emocromocitometrici, immunoematologici = aggregate_referti_dict(ref_dict=ref_dict)

virologici.to_excel(referti_agg_dir / "Virologici_aggreati.xlsx")
emocromocitometrici.to_excel(referti_agg_dir / "Emocromocitometrici_aggreati.xlsx")
immunoematologici.to_excel(referti_agg_dir / "Immunoemetologici_aggreati.xlsx")

e_limits = emocromocitometrici[['Esame', 'V. ref']].drop_duplicates().dropna()
e_limits[['Inf. ref', 'Sup. ref']] = e_limits['V. ref'].str.split('-', expand=True)
e_limits['Inf. ref'] = e_limits['Inf. ref'].str.replace(',', '.').astype(float)
e_limits['Sup. ref'] = e_limits['Sup. ref'].str.replace(',', '.').astype(float)

e_pivot = emocromocitometrici.pivot(index='Data Referto', columns='Esame', values='Risultato')
e_tab = emocromocitometrici_tab(dataset=e_pivot, limits=e_limits)

print(immunoematologici)

res = immunoematologici.sort_values(by='Data Referto', ascending=True).drop_duplicates(subset=['Esame', 'Risultato'],
                                                                                       keep='last')
i_tab = immunoematologici_tab(dataset=res)
final = Tabs(tabs=[i_tab, e_tab])
layout = column(final)
# Put the tabs in the current document for display
curdoc().add_root(layout)
