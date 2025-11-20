import time
import signal
import os
import json
from collections import defaultdict
from typing import Dict, Any, Type

from benchmarks.test_suite_generator import TestSuiteGenerator
import psutil


class TestBenchmark:
    """
    Benchmark que espera um mapeamento nome -> AlgorithmClass (classe que implementa .run()).
    Ex: {"forca_bruta": BruteForceClique, "backtracking": BacktrackingClique, ...}
    """
    def __init__(self, algorithm_classes: Dict[str, Type]):
        self.algorithm_classes = algorithm_classes
        self.results = defaultdict(dict)

    # ---------- execução com timeout ----------
    def run_algorithm(self, AlgoClass, graph, timeout=300):
        """
        Recebe a classe do algoritmo (não instância). Instancia com o grafo e chama .run().
        Mede tempo e memória. Usa signal.SIGALRM para timeout (Unix).
        """
        start_time = time.time()
        start_mem = self.get_memory_usage()

        try:
            class TimeoutError(Exception):
                pass

            def timeout_handler(signum, frame):
                raise TimeoutError()

            # registra handler e seta alarme
            signal.signal(signal.SIGALRM, timeout_handler)
            signal.alarm(timeout)

            # instancia e executa
            instance = AlgoClass(graph)
            result = instance.run()

            # desliga alarme
            signal.alarm(0)

            end_time = time.time()
            end_mem = self.get_memory_usage()

            return {
                'clique': set(result) if result is not None else set(),
                'tamanho': len(result) if result is not None else 0,
                'tempo': end_time - start_time,
                'memoria': end_mem - start_mem,
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
        except Exception as e:
            return {
                'clique': set(),
                'tamanho': 0,
                'tempo': 0,
                'memoria': 0,
                'timeout': False,
                'erro': True,
                'mensagem_erro': str(e)
            }

    def get_memory_usage(self):
        p = psutil.Process()
        return p.memory_info().rss

    # ---------- execução completa ----------
    def run_benchmarks(self, timeout_per_run=300):
        test_suite = TestSuiteGenerator.generate_test_suite()

        for suite_name, graphs in test_suite.items():
            print(f"\n=== Executando suite: {suite_name} ===")
            for i, graph in enumerate(graphs):
                print(f"Grafo {i+1}/{len(graphs)} - {len(graph)} vértices")
                for algo_name, AlgoClass in self.algorithm_classes.items():
                    # política: evita forca bruta e DP em grafos grandes
                    if len(graph) > 25 and algo_name in ['forca_bruta', 'programacao_dinamica']:
                        print(f"  Pulando {algo_name} (muitos vértices)")
                        continue

                    print(f"  Executando {algo_name}...")
                    result = self.run_algorithm(AlgoClass, graph, timeout=timeout_per_run)
                    # armazena
                    self.results[suite_name][(i, algo_name)] = result

                    if result.get('timeout'):
                        print("    TIMEOUT")
                    elif result.get('erro'):
                        print("    ERRO", result.get('mensagem_erro', ''))
                    else:
                        print(f"    Clique: {result['tamanho']}, Tempo: {result['tempo']:.4f}s")

        return self.results

    def save_results_json(self, filename="benchmark_output.json"):
        output_path = os.path.join("data", "results", "raw", filename)

    # garante que a pasta existe
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        # converte sets em listas para JSON
        serializable = {}
        for suite, data in self.results.items():
            serializable[suite] = {}
            for key, res in data.items():
                i, algo_name = key
                res_copy = res.copy()
                res_copy['clique'] = list(res_copy.get('clique', []))
                serializable[suite][f"{i}_{algo_name}"] = res_copy
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(serializable, f, ensure_ascii=False, indent=2)
