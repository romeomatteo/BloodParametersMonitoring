import tabula
import pandas as pd


class BloodExam:
    def __init__(self, pdf_path, template_path):
        self._raw_df = tabula.read_pdf_with_template(input_path=pdf_path,
                                                     template_path=template_path,

                                                     pandas_options={'header': None})
        self._raw_cols = ['Esame', 'Risultato', 'V. ref', 'Unità di misura']
        self.immunoematologici = self._get_immunoematologici()
        self.emocromocitometrico = self._get_emocromocitometrico()
        self.virologico = self._get_virologico()

    def _get_immunoematologici(self):
        immunoematologici = self._raw_df[0].copy()
        immunoematologici.columns = self._raw_cols[:3]
        return immunoematologici

    def _get_emocromocitometrico(self):
        emocromocitometrico_1 = self._raw_df[2].copy()
        emocromocitometrico_1.loc[emocromocitometrico_1[4].isna(), 4] = ''
        emocromocitometrico_1[3] = emocromocitometrico_1[3] + emocromocitometrico_1[4] + \
                                   emocromocitometrico_1[5]
        emocromocitometrico_1 = emocromocitometrico_1.drop(columns=[2, 4, 5])
        emocromocitometrico_1.columns = self._raw_cols

        # TODO
        # emocromocitometrico_2 = self._raw_df[3].copy()
        emocromocitometrico_2 = None
        emocromocitometrico = pd.concat([emocromocitometrico_1, emocromocitometrico_2], axis=0)
        emocromocitometrico['Risultato'] = emocromocitometrico['Risultato'].str.replace(',', '.').astype(float)
        return emocromocitometrico

    def _get_virologico(self):
        virologico = self._raw_df[1].copy()
        virologico.columns = self._raw_cols
        return virologico
