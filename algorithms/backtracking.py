from typing import Set, Optional, Dict


class BacktrackingClique:
    def __init__(self, graph: Dict[int, Set[int]]):
        self.graph = graph
        # Ordenar vértices por grau decrescente
        self.vertices = sorted(graph.keys(), key=lambda x: len(graph[x]), reverse=True)
        self.best_clique: Set[int] = set()
        self.current_clique: Set[int] = set()

    def backtracking_max_clique(self) -> Set[int]:
        """Encontra a clique máxima usando backtracking com podas"""
        self._backtrack(0)
        return self.best_clique

    def _backtrack(self, start_index: int):
        # Poda: se não é possível superar a melhor solução atual
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
        """Verifica se um vértice pode ser adicionado à clique atual"""
        return all(vertex in self.graph[v] for v in self.current_clique)

    def _get_common_neighbors(self, vertex: int) -> Set[int]:
        """Vizinhos comuns entre o vértice e a clique atual"""
        if not self.current_clique:
            return set(self.graph[vertex])
        common_neighbors = set(self.graph[vertex])
        for v in self.current_clique:
            common_neighbors.intersection_update(self.graph[v])
        return common_neighbors

    def _get_next_index(self, neighbors: Set[int], start: int) -> int:
        """Encontra o próximo índice baseado nos vizinhos comuns"""
        for i in range(start, len(self.vertices)):
            if self.vertices[i] in neighbors:
                return i
        return len(self.vertices)


# -----------------------------
# Versão para k-clique
# -----------------------------
def backtracking_k_clique(graph: Dict[int, Set[int]], k: int) -> Optional[Set[int]]:
    """Encontra uma clique de tamanho k usando backtracking"""

    def backtrack(current_clique: Set[int], candidates: Set[int]) -> bool:
        nonlocal found, result_clique
        if found:
            return True

        if len(current_clique) == k:
            result_clique = current_clique.copy()
            found = True
            return True

        if len(current_clique) + len(candidates) < k:
            return False

        for vertex in list(candidates):
            if all(vertex in graph[v] for v in current_clique):
                current_clique.add(vertex)
                new_candidates = candidates.intersection(graph[vertex])
                if backtrack(current_clique, new_candidates):
                    return True
                current_clique.remove(vertex)
                candidates.remove(vertex)

        return False

    vertices = set(graph.keys())
    found = False
    result_clique: Set[int] = set()
    sorted_vertices = sorted(vertices, key=lambda x: len(graph[x]), reverse=True)

    for start_vertex in sorted_vertices:
        if backtrack({start_vertex}, set(graph[start_vertex])):
            return result_clique

    return None
