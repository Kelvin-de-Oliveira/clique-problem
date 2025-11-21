from typing import Set, Dict
from algorithms.base import CliqueAlgorithm
from algorithms import GreedyCliqueWithRestarts


class LocalSearchClique(CliqueAlgorithm):
    """
    Implementação da busca local para clique máxima,
    exatamente baseada na função que você forneceu.
    """

    def __init__(self, graph: Dict[int, Set[int]], max_iterations: int = 1000):
        super().__init__(graph)
        self.max_iterations = max_iterations

    # ----- Funções auxiliares -----

    @staticmethod
    def is_clique(graph, vertices: Set[int]) -> bool:
        for v in vertices:
            for u in vertices:
                if v != u and u not in graph[v]:
                    return False
        return True

    def local_search(self, initial_clique: Set[int]) -> Set[int]:
        graph = self.graph
        current = set(initial_clique)
        best = set(initial_clique)
        vertices = set(graph.keys())

        for _ in range(self.max_iterations):
            improved = False

            # ------------ 1) Adição de vértice ------------
            candidates = vertices - current
            for v in candidates:
                if all(v in graph[u] for u in current):
                    current.add(v)
                    improved = True
                    break

            if improved:
                if len(current) > len(best):
                    best = set(current)
                continue

            # ------------ 2) Swap: troca 2 -> 2 ------------
            if len(current) >= 2:
                for v1 in current:
                    for v2 in current:
                        if v1 >= v2:
                            continue

                        swap_candidates = set()
                        for cand in candidates:
                            ok = True
                            for v in current:
                                if v not in {v1, v2} and cand not in graph[v]:
                                    ok = False
                                    break
                            if ok:
                                swap_candidates.add(cand)

                        if len(swap_candidates) >= 2:
                            new_clique = (current - {v1, v2}).union(
                                list(swap_candidates)[:2]
                            )
                            if self.is_clique(graph, new_clique) and len(new_clique) > len(current):
                                current = new_clique
                                improved = True
                                break

                    if improved:
                        break

            if not improved:
                break

        return best

    # ----- Método principal -----

    def run(self) -> Set[int]:
        # Fase 1: solução inicial via greedy com restarts
        initial = GreedyCliqueWithRestarts(self.graph, num_restarts=10).run()

        # Fase 2: busca local
        best = self.local_search(initial)

        return best
