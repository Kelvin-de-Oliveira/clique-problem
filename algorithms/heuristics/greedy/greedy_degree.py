from typing import Set, Dict
from algorithms.base import CliqueAlgorithm
import random


class GreedyCliqueDegree(CliqueAlgorithm):
    """Heurística gulosa baseada no vértice de maior grau."""

    def run(self) -> Set[int]:
        graph = self.graph

        if not graph:
            return set()

        clique = set()
        candidates = set(graph.keys())

        while candidates:
            best_vertex = None
            best_degree = -1

            for vertex in candidates:
                current_degree = len(graph[vertex].intersection(candidates))
                if current_degree > best_degree:
                    best_vertex = vertex
                    best_degree = current_degree

            if best_vertex is None:
                break

            # Verificar se pode entrar na clique
            if all(best_vertex in graph[v] for v in clique):
                clique.add(best_vertex)
                candidates = candidates.intersection(graph[best_vertex])
            else:
                candidates.remove(best_vertex)

        return clique
