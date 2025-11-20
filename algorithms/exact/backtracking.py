from typing import Set, Dict
from algorithms.base import CliqueAlgorithm

class BacktrackingClique(CliqueAlgorithm):
    """Classe Backtracking já existente, adaptada para .run()."""
    def __init__(self, graph: Dict[int, Set[int]]):
        super().__init__(graph)
        # Ordenar vértices por grau decrescente para heurística
        self.vertices = sorted(self.graph.keys(), key=lambda x: len(self.graph[x]), reverse=True)
        self.best_clique: Set[int] = set()
        self.current_clique: Set[int] = set()

    def run(self) -> Set[int]:
        return self.backtracking_max_clique()

    def backtracking_max_clique(self) -> Set[int]:
        self._backtrack(0)
        return self.best_clique

    def _backtrack(self, start_index: int):
        # poda simples: mesmo que escolha todos os restantes não superei best
        if len(self.current_clique) + (len(self.vertices) - start_index) <= len(self.best_clique):
            return

        for i in range(start_index, len(self.vertices)):
            vertex = self.vertices[i]
            if self._can_add_to_clique(vertex):
                self.current_clique.add(vertex)
                if len(self.current_clique) > len(self.best_clique):
                    self.best_clique = self.current_clique.copy()
                self._backtrack(i + 1)
                self.current_clique.remove(vertex)

    def _can_add_to_clique(self, vertex: int) -> bool:
        return all(vertex in self.graph[v] for v in self.current_clique)

    # Métodos auxiliares (mantidos caso queira usar otimizações futuras)
    def _get_common_neighbors(self, vertex: int) -> Set[int]:
        if not self.current_clique:
            return set(self.graph[vertex])
        common_neighbors = set(self.graph[vertex])
        for v in self.current_clique:
            common_neighbors.intersection_update(self.graph[v])
        return common_neighbors

    def _get_next_index(self, neighbors: Set[int], start: int) -> int:
        for i in range(start, len(self.vertices)):
            if self.vertices[i] in neighbors:
                return i
        return len(self.vertices)
