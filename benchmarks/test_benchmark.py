import time
from collections import defaultdict
import psutil
import signal
from graphs.generators import generate_random_graph, generate_scale_free_graph, generate_clique_based_graph

class TestBenchmark:
    def __init__(self, brute_force_max_clique,
                       BacktrackingClique,
                       divide_conquer_clique,
                       dp_clique_bitmask,
                       greedy_clique_degree,
                       greedy_clique_with_restarts,
                       approximation_clique_coloring,
                       local_search_clique):

        self.algorithms = {
            'forca_bruta': brute_force_max_clique,
            'backtracking': BacktrackingClique,
            'divide_conquer': divide_conquer_clique,
            'programacao_dinamica': dp_clique_bitmask,
            'guloso_grau': greedy_clique_degree,
            'guloso_reinicios': lambda g: greedy_clique_with_restarts(g, 10),
            'aproximacao_coloracao': approximation_clique_coloring,
            'busca_local': lambda g: local_search_clique(g, greedy_clique_degree(g))
        }

        self.results = defaultdict(dict)

    # ------------------------------------------------------------
    # Geração do conjunto completo de testes
    # ------------------------------------------------------------
    def generate_test_suite(self):
        """Gera uma suíte completa de testes."""
        test_suite = {}

        print("Gerando grafos pequenos...")
        test_suite['pequenos_aleatorios'] = [
            generate_random_graph(15, 0.3),
            generate_random_graph(15, 0.5),
            generate_random_graph(15, 0.7),
            generate_random_graph(20, 0.3),
            generate_random_graph(20, 0.5)
        ]

        print("Gerando grafos médios...")
        test_suite['medios_aleatorios'] = [
            generate_random_graph(30, 0.2),
            generate_random_graph(30, 0.4),
            generate_random_graph(50, 0.2),
            generate_random_graph(50, 0.3)
        ]

        print("Gerando grafos grandes...")
        test_suite['grandes_aleatorios'] = [
            generate_random_graph(100, 0.1),
            generate_random_graph(100, 0.2),
            generate_random_graph(200, 0.1)
        ]

        print("Gerando grafos scale-free...")
        test_suite['scale_free'] = [
            generate_scale_free_graph(50, 2),
            generate_scale_free_graph(100, 3),
            generate_scale_free_graph(200, 4)
        ]

        print("Gerando grafos com cliques conhecidas...")
        test_suite['clique_embutida'] = [
            generate_clique_based_graph(30, 8, 50),
            generate_clique_based_graph(50, 12, 100),
            generate_clique_based_graph(100, 15, 200)
        ]

        return test_suite

    # ------------------------------------------------------------
    # Execução de um algoritmo com timeout
    # ------------------------------------------------------------
    def run_algorithm(self, algorithm, graph, timeout=300):
        start_time = time.time()
        start_memory = self.get_memory_usage()

        try:
            class TimeoutError(Exception):
                pass

            def timeout_handler(signum, frame):
                raise TimeoutError()

            signal.signal(signal.SIGALRM, timeout_handler)
            signal.alarm(timeout)

            result = algorithm(graph)

            signal.alarm(0)
            end_time = time.time()
            end_memory = self.get_memory_usage()

            return {
                'clique': result,
                'tamanho': len(result),
                'tempo': end_time - start_time,
                'memoria': end_memory - start_memory,
                'timeout': False,
                'erro': False
            }

        except TimeoutError:
            return {
                'clique': set(),
                'tamanho': 0,
                'tempo': timeout,
                'memoria': 0,
                'timeout': True,
                'erro': False
            }

        except Exception:
            return {
                'clique': set(),
                'tamanho': 0,
                'tempo': 0,
                'memoria': 0,
                'timeout': False,
                'erro': True
            }

    # ------------------------------------------------------------
    # Medição de memória
    # ------------------------------------------------------------
    def get_memory_usage(self):
        process = psutil.Process()
        return process.memory_info().rss

    # ------------------------------------------------------------
    # Execução completa do benchmark
    # ------------------------------------------------------------
    def run_benchmarks(self):
        test_suite = self.generate_test_suite()

        for suite_name, graphs in test_suite.items():
            print(f"\n=== Executando suite: {suite_name} ===")
            for i, graph in enumerate(graphs):
                print(f"Grafo {i + 1}/{len(graphs)} - {len(graph)} vértices")
                for algo_name, algorithm in self.algorithms.items():
                    if len(graph) > 25 and algo_name in ['forca_bruta', 'programacao_dinamica']:
                        continue
                    print(f"  Executando {algo_name}...")
                    result = self.run_algorithm(algorithm, graph)
                    self.results[suite_name][(i, algo_name)] = result
                    if result['timeout']:
                        print("    TIMEOUT")
                    elif result['erro']:
                        print("    ERRO")
                    else:
                        print(f"    Clique: {result['tamanho']}, Tempo: {result['tempo']:.4f}s")

        return self.results
