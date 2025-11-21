import numpy as np
from scipy.optimize import curve_fit


class ModelFitting:
    """
    Ajusta modelos matemáticos aos dados empíricos
    para estimar complexidade temporal e espacial.
    """

    @staticmethod
    def linear(n, a, b):
        return a * n + b

    @staticmethod
    def quadratic(n, a, b, c):
        return a * n**2 + b * n + c

    @staticmethod
    def exponential(n, a, b):
        return a * np.exp(b * n)

    @staticmethod
    def log_linear(n, a, b):
        return a * n * np.log(n + 1) + b

    @staticmethod
    def r_squared(func, x, y, params):
        y_pred = func(x, *params)
        ss_res = np.sum((y - y_pred) ** 2)
        ss_tot = np.sum((y - np.mean(y)) ** 2)
        return 1 - (ss_res / ss_tot) if ss_tot != 0 else 0

    @classmethod
    def fit_models(cls, x, y):
        """
        Ajusta todos os modelos de complexidade.
        """
        models = {}

        model_defs = {
            "linear": cls.linear,
            "quadratic": cls.quadratic,
            "exponential": cls.exponential,
            "log_linear": cls.log_linear
        }

        initial_params = {
            "exponential": [1e-6, 0.1]
        }

        for name, func in model_defs.items():
            try:
                popt, _ = curve_fit(
                    func,
                    x,
                    y,
                    maxfev=5000,
                    p0=initial_params.get(name, None)
                )
                models[name] = {
                    "params": popt,
                    "r_squared": cls.r_squared(func, x, y, popt)
                }
            except Exception:
                models[name] = None

        return models

    @staticmethod
    def best_complexity(models: dict):
        """
        Retorna a melhor complexidade com base no maior R².
        """
        complex_table = {
            "linear": "O(n)",
            "quadratic": "O(n²)",
            "exponential": "O(2ⁿ)",
            "log_linear": "O(n log n)"
        }

        best_model = None
        best_r2 = -float("inf")

        for name, data in models.items():
            if data and data["r_squared"] > best_r2:
                best_model = name
                best_r2 = data["r_squared"]

        if best_model is None:
            return "Desconhecida"

        return f"{complex_table.get(best_model)} (R²={best_r2:.3f})"
