import os
import pandas as pd

from benchmarks import TestBenchmark
from data import DataCollector
from data.empirical_analysis.plotter import Plotter
  

from algorithms import (
    BruteForceClique, BacktrackingClique, DivideConquerClique, DPCliqueBitmask,
    GreedyCliqueDegree, GreedyCliqueWithRestarts, GreedyCliqueMinDegree, GreedyCliqueCoreDecomposition,
    ColoringHeuristicClique, LocalSearchClique, GeneticAlgorithmClique
)

from data.empirical_analysis import (
    TimeAnalysis,
    MemoryAnalysis,
    AnalysisExporter,
    ReportGenerator,
)

def main():
    # -------------------
    # Mapeamento de algoritmos
    # -------------------
    algorithms = {
        'forca_bruta': BruteForceClique,
        'backtracking': BacktrackingClique,
        'divide_conquer': DivideConquerClique,
        'programacao_dinamica': DPCliqueBitmask,
        'guloso_grau': GreedyCliqueDegree,
        'guloso_reinicios': GreedyCliqueWithRestarts,
        'guloso_min_degree': GreedyCliqueMinDegree,
        'guloso_core': GreedyCliqueCoreDecomposition,
        "heuristica_coloring": ColoringHeuristicClique,
        "heuristica_local_search": LocalSearchClique,
        "meta_heuristica_genetico": GeneticAlgorithmClique,
    }
   
    # -------------------
    # Roda o benchmark (gera CSVs medianos e individuais)
    # -------------------
    tb = TestBenchmark(algorithms)
    tb.run_benchmarks(timeout_per_run=300)  # não precisa mais do return

    # -------------------
    # DataCollector: lê os CSVs gerados pelo benchmark
    # -------------------
    collector = DataCollector(raw_folder="data/results/raw")
    df_median, df_individual = collector.load_csvs()

    print(f"Linhas do DataFrame mediano: {len(df_median)}")
    print(f"Linhas do DataFrame individual: {len(df_individual)}")
    print("Benchmark completo!")

    # -------------------
    # Executa análises empíricas com os dados medianos
    # -------------------
    time_analysis = TimeAnalysis(df_median).analyze()
    memory_analysis = MemoryAnalysis(df_median).analyze()

    # Gera relatório textual
    report = ReportGenerator(time_analysis, memory_analysis)
    report.print_report()

    # Salvar resultados da análise em CSV
    results_df = AnalysisExporter.to_dataframe(time_analysis, memory_analysis)
    AnalysisExporter.save_csv(results_df, filename="empirical_analysis.csv")
    print("\nAnálise empírica concluída!")

    # -------------------
    # Plotagem dos gráficos usando dados individuais
    # -------------------
    
    plotter = Plotter(df_consolidado=df_median, df_individual=df_individual,
                      output_dir="data/results/graphics")
    plotter.plot_tempo_por_algoritmo()
    plotter.plot_memoria_por_algoritmo()
    plotter.plot_scaling_por_algoritmo()
    plotter.plot_tipo_grafo()
    plotter.plot_tempo_vs_clique()
    plotter.plot_empirical_summary()
    print("Gráficos gerados na pasta data/results/graphics")

if __name__ == "__main__":
    main()
