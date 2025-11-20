from typing import Set, Dict
from algorithms.base import CliqueAlgorithm
import random

class GreedyCliqueWithRestarts(CliqueAlgorithm):
    """Executa o algoritmo guloso múltiplas vezes com reinicializações aleatórias."""

    def __init__(self, graph: Dict[int, Set[int]], num_restarts: int = 10):
        super().__init__(graph)
        self.num_restarts = num_restarts

    def run(self) -> Set[int]:
        graph = self.graph
        vertices = list(graph.keys())

        best_clique = set()

        for _ in range(self.num_restarts):
            random.shuffle(vertices)

            clique = set()
            candidates = set(vertices)

            while candidates:
                vertex = random.choice(list(candidates))

                if all(vertex in graph[v] for v in clique):
                    clique.add(vertex)
                    candidates = candidates.intersection(graph[vertex])
                else:
                    candidates.remove(vertex)

            if len(clique) > len(best_clique):
                best_clique = clique

        return best_clique