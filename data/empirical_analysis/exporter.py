import pandas as pd
import os

class AnalysisExporter:
    """
    Converte resultados em DataFrame e exporta para CSV.
    """

    @staticmethod
    def to_dataframe(time_results: dict, mem_results: dict):
        rows = []

        for algo, info in time_results.items():
            rows.append({
                "algoritmo": algo,
                "tipo": "tempo",
                "complexidade": info["complexidade_estimada"],
                "r2": max(
                    (m["r_squared"] for m in info["modelos"].values() if m),
                    default=None
                ),
                "tempo_medio": info["tempo_medio"],
                "memoria_media_mb": None
            })

        for algo, info in mem_results.items():
            rows.append({
                "algoritmo": algo,
                "tipo": "memoria",
                "complexidade": info["complexidade_memoria"],
                "r2": max(
                    (m["r_squared"] for m in info["modelos"].values() if m),
                    default=None
                ),
                "tempo_medio": None,
                "memoria_media_mb": info["memoria_media_mb"]
            })

        return pd.DataFrame(rows)

    @staticmethod
    def save_csv(df: pd.DataFrame, filename="empirical_analysis.csv"):
        output_path = os.path.join("data", "results", "analysis", filename)
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        df.to_csv(output_path, index=False)
        print(f"[OK] Arquivo salvo em: {output_path}")
