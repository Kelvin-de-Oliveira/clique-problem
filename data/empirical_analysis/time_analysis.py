import numpy as np
from .base_analysis import BaseAnalysis
from .model_fitting import ModelFitting

class TimeAnalysis(BaseAnalysis):
    """
    Analisa complexidade temporal empírica dos algoritmos.
    """

    def analyze(self):
        valid = self.get_valid_rows({
            "tempo_mediano >": 0
        })

        analysis = {}

        for algoritmo in valid["algoritmo"].unique():
            algo_data = valid[valid["algoritmo"] == algoritmo]

            if len(algo_data) < 3:
                continue

            x = algo_data["tamanho_grafo"].values
            y = algo_data["tempo_mediano"].values

            models = ModelFitting.fit_models(x, y)

            analysis[algoritmo] = {
                "dados": algo_data,
                "modelos": models,
                "complexidade_estimada": ModelFitting.best_complexity(models),
                "tempo_medio": float(np.mean(y))
            }

        self.analysis_results = analysis
        return analysis
