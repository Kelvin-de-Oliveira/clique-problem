from typing import Set, Dict
from algorithms.base import CliqueAlgorithm
import random

class GreedyCliqueCoreDecomposition(CliqueAlgorithm):
    """Heurística baseada em k-core decomposition."""

    def _compute_core_numbers(self) -> Dict[int, int]:
        graph = self.graph
        degrees = {v: len(neigh) for v, neigh in graph.items()}

        vertices = sorted(degrees.keys(), key=lambda x: degrees[x])
        core = {}

        while vertices:
            v = vertices.pop(0)
            core[v] = degrees[v]

            for u in graph[v]:
                if degrees[u] > degrees[v]:
                    degrees[u] -= 1

            vertices.sort(key=lambda x: degrees[x])

        return core

    def run(self) -> Set[int]:
        core_numbers = self._compute_core_numbers()
        
        # Ordenar vértices por core number decrescente
        sorted_vertices = sorted(
            core_numbers.keys(), key=lambda x: core_numbers[x], reverse=True
        )

        clique = set()

        for v in sorted_vertices:
            if all(v in self.graph[u] for u in clique):
                clique.add(v)

        return clique
