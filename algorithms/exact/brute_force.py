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
        # Este duplo loop verifica todos os pares dentro de um conjunto de tamanho k.
        # Complexidade: O(k²), o que é pequeno comparado a gerar subconjuntos.

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
        # Aqui está a principal fonte da complexidade exponencial:
        # itertools.combinations(vertices, k) gera TODAS as combinações possíveis
        # de k vértices dentre n vértices.
        #
        # O número de combinações é C(n, k) = n! / (k!(n-k)!)
        #
        # Ao longo do algoritmo principal, testamos k = n, n-1, ..., 1.
        # Isso faz com que o número total de subconjuntos gerados seja:
        #
        #   C(n, n) + C(n, n-1) + ... + C(n, 1)
        #
        # Isso é exatamente igual a 2ⁿ - 1.
        #
        # Portanto, só a geração das combinações já implica complexidade O(2ⁿ).
        for combination in itertools.combinations(vertices, k):
            candidate_set = set(combination)
            # Verificar cada subconjunto leva O(k²), mas isso é desprezível
            # frente ao custo de gerar 2ⁿ subconjuntos.
            if BruteForceClique._is_clique(graph, candidate_set):
                return candidate_set
        return None

    def run(self) -> Set[int]:
        vertices = list(self.graph.keys())
        n = len(vertices)
        # Este loop percorre todos os tamanhos k = n, n-1, ..., 1.
        # Para cada k, geramos C(n, k) subconjuntos.
        #
        # A soma total de todos os C(n, k) é 2ⁿ.
        # Logo, mesmo que interrompa cedo em alguns casos,
        # o pior caso continua sendo O(2ⁿ).
        for size in range(n, 0, -1):
            clique = BruteForceClique._brute_force_clique(self.graph, size)
            if clique is not None:
                return clique
        return set()
