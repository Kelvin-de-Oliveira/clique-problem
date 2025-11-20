import json
import pandas as pd
import os


class DataCollector:
    def __init__(self, benchmark_results):
        """
        benchmark_results: dict retornado pelo TestBenchmark.run_benchmarks()
        """
        self.results = benchmark_results
        self.df = None

    def create_dataframe(self):
        """
        Converte os resultados do benchmark em um DataFrame do pandas.
        """
        rows = []

        for suite_name, suite_dict in self.results.items():
            for key, res in suite_dict.items():
                # key é uma tupla (graph_idx, algo_name)
                graph_idx, algo_name = key

                rows.append({
                    "suite": suite_name,
                    "grafo_id": int(graph_idx),
                    "algoritmo": algo_name,
                    "tamanho_clique": res["tamanho"],
                    "tempo_execucao": res["tempo"],
                    "uso_memoria": res["memoria"],
                    "timeout": res["timeout"],
                    "erro": res["erro"],
                })

        self.df = pd.DataFrame(rows)
        return self.df

    def save_json(self, filename="resultados_benchmark.json"):
        """
        Salva os resultados completos em JSON, convertendo as chaves tupla em strings.
        """
        output_path = os.path.join("data", "results", "processed", filename)
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        serializable = {}
        for suite, data in self.results.items():
            serializable[suite] = {}
            for key, res in data.items():
                graph_idx, algo_name = key
                serializable[suite][f"{graph_idx}_{algo_name}"] = res

        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(serializable, f, indent=2, default=str)

    def save_csv(self, filename="resultados_detalhados.csv"):
        """
        Salva o DataFrame em CSV. Cria diretório se necessário.
        """
        if self.df is None:
            raise RuntimeError("DataFrame ainda não foi criado. Use create_dataframe() antes.")

        output_path = os.path.join("data", "results", "processed", filename)
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        self.df.to_csv(output_path, index=False)

    def load_json(self, filename="resultados_benchmark.json"):
        """
        Carrega um arquivo JSON com resultados processados.
        """
        output_path = os.path.join("data", "results", "processed", filename)
        with open(output_path, 'r', encoding='utf-8') as f:
            return json.load(f)
