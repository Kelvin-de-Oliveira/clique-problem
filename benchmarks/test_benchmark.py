import time
import signal
import os
import csv
from collections import defaultdict
from typing import Dict, Type
import statistics
import tracemalloc

from benchmarks.test_suite_generator import TestSuiteGenerator


class TestBenchmark:
    """
    Benchmark que espera um mapeamento nome -> AlgorithmClass (classe que implementa .run()).
    Ex: {"forca_bruta": BruteForceClique, "backtracking": BacktrackingClique, ...}
    """
    def __init__(self, algorithm_classes: Dict[str, Type]):
        self.algorithm_classes = algorithm_classes
        self.results = defaultdict(dict)

    # ---------- execução de um algoritmo com timeout e memória ----------
    def run_algorithm(self, AlgoClass, graph, timeout=300):
        start_time = time.time()

        class TimeoutError(Exception):
            pass

        def timeout_handler(signum, frame):
            raise TimeoutError()

        signal.signal(signal.SIGALRM, timeout_handler)
        signal.alarm(timeout)

        try:
            tracemalloc.start()
            instance = AlgoClass(graph)
            result = instance.run()
            current, peak = tracemalloc.get_traced_memory()
            tracemalloc.stop()

            end_time = time.time()
            signal.alarm(0)

            return {
                'clique': set(result) if result else set(),
                'tamanho': len(result) if result else 0,
                'tempo': end_time - start_time,
                'memoria': peak / (1024*1024),
                'timeout': False,
                'erro': False
            }

        except TimeoutError:
            tracemalloc.stop()
            return {
                'clique': set(),
                'tamanho': 0,
                'tempo': timeout,
                'memoria': 0,
                'timeout': True,
                'erro': False
            }

        except Exception as e:
            tracemalloc.stop()
            return {
                'clique': set(),
                'tamanho': 0,
                'tempo': 0,
                'memoria': 0,
                'timeout': False,
                'erro': True,
                'mensagem_erro': str(e)
            }

    # ---------- salvar resultados individuais ----------
    def save_individual_results_csv(self, individual_results, filename="benchmark_individual.csv"):
        output_csv_path = os.path.join("data", "results", "raw", filename)
        os.makedirs(os.path.dirname(output_csv_path), exist_ok=True)
        if not individual_results:
            print("Nenhum resultado individual para salvar.")
            return
        with open(output_csv_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=individual_results[0].keys())
            writer.writeheader()
            writer.writerows(individual_results)

    # ---------- salvar CSV com medianas ----------
    def save_median_csv(self):
        median_rows = []
        for algo_name, size_dict in self.results.items():
            for n, res in size_dict.items():
                median_rows.append({
                    "algoritmo": algo_name,
                    "tamanho_grafo": n,
                    "tempo_mediano": res['tempo_mediano'],
                    "memoria_mediana": res['memoria_mediana']
                })

        median_csv_path = os.path.join("data", "results", "raw", "benchmark_median.csv")
        os.makedirs(os.path.dirname(median_csv_path), exist_ok=True)
        with open(median_csv_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=median_rows[0].keys())
            writer.writeheader()
            writer.writerows(median_rows)

    # ---------- execução completa de todos os benchmarks ----------
    def run_benchmarks(self, timeout_per_run=300, debug_memory=False):
        test_suite = TestSuiteGenerator.generate_test_suite()
        individual_results = []

        for algo_name, graphs in test_suite.items():
            print(f"\n=== Executando algoritmo: {algo_name} ===")
            results_by_n = {}

            for n, tipo_grafo, graph in graphs:
                if n not in results_by_n:
                    results_by_n[n] = []

                result = self.run_algorithm(self.algorithm_classes[algo_name], graph, timeout=timeout_per_run)
                result['tipo_grafo'] = tipo_grafo
                results_by_n[n].append(result)

                individual_results.append({
                    "algoritmo": algo_name,
                    "n": n,
                    "tipo_grafo": tipo_grafo,
                    "tamanho_clique": result['tamanho'],
                    "tempo": result['tempo'],
                    "memoria": result['memoria'],
                    "timeout": result['timeout'],
                    "erro": result['erro']
                })

            # calcular medianas por tamanho
            for n, result_list in results_by_n.items():
                tempo_mediano = statistics.median([r['tempo'] for r in result_list])
                memoria_mediana = statistics.median([r['memoria'] for r in result_list])

                if debug_memory:
                    print(f"[DEBUG] {algo_name} n={n} -> memoria_mediana={memoria_mediana:.2f} MB")

                print(f"n={n}, Tempo mediano: {tempo_mediano:.4f}s, Memória mediana: {memoria_mediana:.2f} MB")

                if algo_name not in self.results:
                    self.results[algo_name] = {}
                self.results[algo_name][n] = {
                    'tempo_mediano': tempo_mediano,
                    'memoria_mediana': memoria_mediana
                }

        # salvar CSVs
        self.save_individual_results_csv(individual_results)
        self.save_median_csv()
