import itertools
from typing import Set, Optional, Dict

def is_clique(graph: Dict[int, Set[int]], vertices: Set[int]) -> bool:
    """Verifica se um conjunto de vértices forma uma clique"""
    vertex_list = list(vertices)
    for i in range(len(vertex_list)):
        for j in range(i + 1, len(vertex_list)):
            u = vertex_list[i]
            v = vertex_list[j]
            if v not in graph[u]:
                return False
    return True

def brute_force_clique(graph: Dict[int, Set[int]], k: int) -> Optional[Set[int]]:
    """Encontra uma clique de tamanho k usando força bruta"""
    vertices = list(graph.keys())

    for combination in itertools.combinations(vertices, k):
        candidate_set = set(combination)
        if is_clique(graph, candidate_set):
            return candidate_set

    return None

def brute_force_max_clique(graph: Dict[int, Set[int]]) -> Set[int]:
    """Encontra a clique máxima usando força bruta"""
    vertices = list(graph.keys())
    n = len(vertices)

    for size in range(n, 0, -1):
        clique = brute_force_clique(graph, size)
        if clique is not None:
            return clique

    return set()
