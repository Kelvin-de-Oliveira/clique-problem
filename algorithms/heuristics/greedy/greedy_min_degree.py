from typing import Set, Dict
from algorithms.base import CliqueAlgorithm
import random


class GreedyCliqueMinDegree(CliqueAlgorithm):
    """Heurística que remove vértices de menor grau até restar uma clique."""

    def _is_clique(self, vertices: Set[int]) -> bool:
        """Verifica se o conjunto é uma clique."""
        for u in vertices:
            for v in vertices:
                if u != v and v not in self.graph[u]:
                    return False
        return True

    def run(self) -> Set[int]:
        graph_copy = {v: set(neigh) for v, neigh in self.graph.items()}

        while graph_copy:
            min_vertex = min(graph_copy, key=lambda x: len(graph_copy[x]))
            current_vertices = set(graph_copy.keys())

            if self._is_clique(current_vertices):
                return current_vertices

            # Remove o vértice de menor grau
            del graph_copy[min_vertex]
            for neighbors in graph_copy.values():
                neighbors.discard(min_vertex)

        return set()