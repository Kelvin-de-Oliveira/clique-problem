from typing import Set, Dict
from algorithms.base import CliqueAlgorithm
import random


class GreedyCliqueMinDegree(CliqueAlgorithm):
    """Heurística que remove vértices de menor grau até restar uma clique."""

    def _is_clique(self, vertices: Set[int]) -> bool:
        """Verifica se o conjunto é uma clique."""
        # Verificar se um conjunto de k vértices é clique exige
        # verificar TODAS as k*(k-1) adjacências possíveis.
        #
        # Portanto, _is_clique(vertices) custa O(k²).
        for u in vertices:
            for v in vertices:
                if u != v and v not in self.graph[u]:
                    return False
        return True

    def run(self) -> Set[int]:
        # Fazemos uma cópia do grafo. Isso custa O(n + m).
        graph_copy = {v: set(neigh) for v, neigh in self.graph.items()}

        # Loop principal: removemos um vértice por iteração,
        # então podemos ter no máximo n iterações.
        while graph_copy:

            # Encontrar o vértice de menor grau exige percorrer todos os vértices.
            # Isso é O(n) por iteração.
            min_vertex = min(graph_copy, key=lambda x: len(graph_copy[x]))

            # current_vertices tem tamanho k, começando em n e diminuindo.
            current_vertices = set(graph_copy.keys())

            # Testar se current_vertices forma uma clique custa O(k²).
            #
            # No início do algoritmo, k ≈ n,
            # então este teste custa O(n²).
            #
            # Como ele ocorre em cada iteração,
            # o custo acumulado da verificação de clique será O(n²) + O((n-1)²) + ...
            # o que leva a O(n³) no pior caso.
            if self._is_clique(current_vertices):
                return current_vertices

            # Remover o vértice de menor grau é O(1)
            del graph_copy[min_vertex]

            # Remover o vértice das listas de adjacência restantes
            # exige percorrer todos os vértices remanescentes.
            #
            # Cada remoção neighbors.discard(min_vertex) é O(1),
            # mas fazemos isso para até n vértices, então é O(n).
            for neighbors in graph_copy.values():
                neighbors.discard(min_vertex)

        return set()
