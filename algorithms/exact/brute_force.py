import itertools
from typing import Set, Dict
from algorithms.base import CliqueAlgorithm

class BruteForceClique(CliqueAlgorithm):
    """Implementação em classe do brute-force já existente."""
    def __init__(self, graph: Dict[int, Set[int]]):
        super().__init__(graph)

    @staticmethod
    def _is_clique(graph: Dict[int, Set[int]], vertices: Set[int]) -> bool:
        vertex_list = list(vertices)
        for i in range(len(vertex_list)):
            for j in range(i + 1, len(vertex_list)):
                u = vertex_list[i]
                v = vertex_list[j]
                if v not in graph[u]:
                    return False
        return True

    @staticmethod
    def _brute_force_clique(graph: Dict[int, Set[int]], k: int):
        vertices = list(graph.keys())
        for combination in itertools.combinations(vertices, k):
            candidate_set = set(combination)
            if BruteForceClique._is_clique(graph, candidate_set):
                return candidate_set
        return None

    def run(self) -> Set[int]:
        vertices = list(self.graph.keys())
        n = len(vertices)
        # procura do maior para o menor
        for size in range(n, 0, -1):
            clique = BruteForceClique._brute_force_clique(self.graph, size)
            if clique is not None:
                return clique
        return set()
