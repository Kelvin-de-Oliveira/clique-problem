import numpy as np
from .base_analysis import BaseAnalysis
from .model_fitting import ModelFitting

class MemoryAnalysis(BaseAnalysis):
    """
    Analisa complexidade de uso de memória.
    """

    def analyze(self):
        valid = self.get_valid_rows({
            "memoria_mediana >": 0
        })

        analysis = {}

        for algoritmo in valid["algoritmo"].unique():
            algo_data = valid[valid["algoritmo"] == algoritmo]

            if len(algo_data) < 3:
                continue

            x = algo_data["tamanho_grafo"].values
            y = algo_data["memoria_mediana"].values

            models = ModelFitting.fit_models(x, y)

            analysis[algoritmo] = {
                "memoria_media_mb": float(np.mean(y)),
                "memoria_maxima_mb": float(np.max(y)),
                "modelos": models,
                "complexidade_memoria": ModelFitting.best_complexity(models),
            }

        self.analysis_results = analysis
        return analysis
