import os

from benchmarks.test_benchmark import TestBenchmark
from data.data_collector import DataCollector

from algorithms.exact.brute_force import BruteForceClique
from algorithms.exact.backtracking import BacktrackingClique
from algorithms.exact.divide_conquer import DivideConquerClique

from algorithms.exact.dp_bitmask import DPCliqueBitmask
from algorithms.heuristics.greedy.greedy_degree import GreedyCliqueDegree
from algorithms.heuristics.greedy.greedy_restarts import GreedyCliqueWithRestarts
from algorithms.heuristics.greedy.greedy_min_degree import GreedyCliqueMinDegree
from algorithms.heuristics.greedy.greedy_core import GreedyCliqueCoreDecomposition
from algorithms.heuristics.hybrid.coloring_heuristic import ColoringHeuristicClique
from algorithms.heuristics.enhancement.local_search import LocalSearchClique
from algorithms.heuristics.metaheuristics.genetic_algorithm import GeneticAlgorithmClique

def main():
    # Mapeamento de algoritmos
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
    # Roda o benchmark
    # -------------------
    tb = TestBenchmark(algorithms)
    results = tb.run_benchmarks(timeout_per_run=300)

    # Salva resultados brutos
    tb.save_results_json("benchmark_output.json")
    print("Resultados brutos salvos em data/results/raw/benchmark_output.json")

    # -------------------
    # Processa resultados com DataCollector
    # -------------------
    collector = DataCollector(results)
    df = collector.create_dataframe()

    collector.save_json("processed_benchmark.json")
    collector.save_csv("processed_benchmark.csv")
    print("Resultados processados salvos em data/results/processed/")

    # Informação resumida
    print(f"Linhas geradas no DataFrame: {len(df)}")
    print(f"Algoritmos testados: {len(algorithms)}")
    print("Benchmark completo!")

if __name__ == "__main__":
    main()
