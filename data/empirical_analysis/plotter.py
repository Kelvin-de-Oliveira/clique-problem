import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os

class Plotter:
    def __init__(self, df_consolidado: pd.DataFrame = None, df_individual: pd.DataFrame = None,
                 output_dir="data/results/graphics"):
        self.df_consolidado = df_consolidado
        self.df_individual = df_individual
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

    def plot_tempo_por_algoritmo(self):
        plt.figure(figsize=(10,6))
        sns.barplot(data=self.df_consolidado, x="algoritmo", y="tempo_mediano")
        plt.xticks(rotation=45, ha='right')
        plt.title("Tempo mediano por algoritmo")
        plt.tight_layout()
        plt.savefig(f"{self.output_dir}/tempo_por_algoritmo.png", dpi=300)
        plt.close()

    def plot_memoria_por_algoritmo(self):
        plt.figure(figsize=(10,6))
        sns.barplot(data=self.df_consolidado, x="algoritmo", y="memoria_mediana")
        plt.xticks(rotation=45, ha='right')
        plt.title("Memória mediana por algoritmo")
        plt.tight_layout()
        plt.savefig(f"{self.output_dir}/memoria_por_algoritmo.png", dpi=300)
        plt.close()

    def plot_scaling_por_algoritmo(self):
        #  Gráfico com todos os algoritmos
        plt.figure(figsize=(10,6))
        sns.lineplot(data=self.df_consolidado, x="tamanho_grafo", y="tempo_mediano",
                    hue="algoritmo", marker="o")
        plt.title("Tempo mediano x Tamanho do grafo (Todos os algoritmos)")
        plt.tight_layout()
        plt.savefig(f"{self.output_dir}/tempo_vs_tamanho_todos.png", dpi=300)
        plt.close()

        # Gráfico apenas com algoritmos heurísticos
        heuristics = [
            "heuristica_coloring",
            "heuristica_local_search",
            "meta_heuristica_genetico",
            "guloso_grau",
            "guloso_reinicios",
            "guloso_min_degree",
            "guloso_core"
        ]

        df_heuristics = self.df_consolidado[self.df_consolidado["algoritmo"].isin(heuristics)]

        plt.figure(figsize=(10,6))
        sns.lineplot(data=df_heuristics, x="tamanho_grafo", y="tempo_mediano",
                    hue="algoritmo", marker="o")
        plt.title("Tempo mediano x Tamanho do grafo (Algoritmos heurísticos)")
        plt.tight_layout()
        plt.savefig(f"{self.output_dir}/tempo_vs_tamanho_heuristics.png", dpi=300)
        plt.close()


    def plot_tipo_grafo(self):
        plt.figure(figsize=(12,6))
        sns.boxplot(data=self.df_individual, x="algoritmo", y="tempo", hue="tipo_grafo")
        plt.xticks(rotation=45, ha='right')
        plt.title("Distribuição do tempo por tipo de grafo e algoritmo")
        plt.tight_layout()
        plt.savefig(f"{self.output_dir}/tempo_por_tipo_grafo.png", dpi=300)
        plt.close()

    def plot_tempo_vs_clique(self):
        plt.figure(figsize=(10,6))
        sns.scatterplot(data=self.df_individual, x="tempo", y="tamanho_clique", hue="algoritmo")
        plt.title("Tempo x Tamanho da clique encontrada")
        plt.tight_layout()
        plt.savefig(f"{self.output_dir}/tempo_vs_clique.png", dpi=300)
        plt.close()

    def plot_empirical_summary(self, csv_path="data/results/analysis/empirical_analysis.csv"):
        """
        Gera gráficos a partir do CSV de análise empírica:
        - Barplot de tempo médio por algoritmo (log scale)
        - Scatter de tempo médio vs memória média (log-log)
        """
        if not os.path.exists(csv_path):
            raise FileNotFoundError(f"{csv_path} não encontrado.")

        df = pd.read_csv(csv_path)

        # Barplot de tempo médio (log scale)
        plt.figure(figsize=(10,6))
        sns.barplot(data=df, x="algoritmo", y="tempo_medio")
        plt.xticks(rotation=45, ha='right')
        plt.yscale("log")
        plt.title("Tempo médio por algoritmo (escala log)")
        plt.tight_layout()
        plt.savefig(f"{self.output_dir}/empirical_tempo_bar.png", dpi=300)
        plt.close()

