import pandas as pd

class BaseAnalysis:
    """
    Classe base para análises empíricas.
    Armazena o DataFrame original e os resultados parciais.
    """

    def __init__(self, dataframe: pd.DataFrame):
        self.df = dataframe
        self.analysis_results = {}

    def get_valid_rows(self, filters: dict):
        """
        Filtra o DataFrame baseado em um dicionário de condições.
        Exemplo:
            filters = {
                "tempo_mediano >": 0,
                "memoria_mediana >": 0
            }
        """
        df = self.df.copy()
        for key, value in filters.items():
            if ">" in key:
                col = key.replace(">", "").strip()
                df = df[df[col] > value]
            elif "<" in key:
                col = key.replace("<", "").strip()
                df = df[df[col] < value]
            else:
                df = df[df[key] == value]
        return df
