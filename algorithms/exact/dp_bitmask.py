from typing import Dict, Set
from algorithms.base import CliqueAlgorithm


class DPCliqueBitmask(CliqueAlgorithm):
    """
    Programação dinâmica com bitmask para encontrar a clique máxima.
    Viável apenas para grafos pequenos (<= 20-22 vértices).
    """

    def run(self) -> Set[int]:
        return self._dp_clique_bitmask(self.graph)

    # ----------------------------------------------------
    # Implementação interna do DP
    # ----------------------------------------------------
    def _dp_clique_bitmask(self, graph: Dict[int, Set[int]]) -> Set[int]:
        vertices = list(graph.keys())
        n = len(vertices)

        if n == 0:
            return set()

        # Mapear vértice -> índice
        vertex_to_index = {v: i for i, v in enumerate(vertices)}

        # Precomputar adjacências como máscaras de bit
        adj_masks = [0] * n
        for i, v in enumerate(vertices):
            mask = 0
            for neighbor in graph[v]:
                if neighbor in vertex_to_index:
                    j = vertex_to_index[neighbor]
                    mask |= (1 << j)
            adj_masks[i] = mask

        # DP[mask] = True se mask representa uma clique válida
        dp = [False] * (1 << n)
        clique_size = [0] * (1 << n)

        # Conjuntos unitários são cliques
        for i in range(n):
            dp[1 << i] = True
            clique_size[1 << i] = 1

        max_mask = 0
        max_size = 1

        # Iterar sobre todas as máscaras
        for mask in range(1 << n):
            if not dp[mask]:
                continue

            current_size = clique_size[mask]

            if current_size > max_size:
                max_size = current_size
                max_mask = mask

            # Expandir mask com outro vértice
            for i in range(n):
                if mask & (1 << i):
                    continue  # já está no conjunto

                # Vértice i é adjacente a todos da clique?
                if (mask & adj_masks[i]) == mask:
                    new_mask = mask | (1 << i)
                    dp[new_mask] = True
                    clique_size[new_mask] = current_size + 1

        # Reconstruir clique final a partir de max_mask
        result = set()
        for i in range(n):
            if max_mask & (1 << i):
                result.add(vertices[i])

        return result
