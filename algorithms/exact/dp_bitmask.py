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

        # Precomputar adjacências como bitmasks é O(n^2),
        # o que é polinomial e irrelevante para o custo exponencial principal.
        adj_masks = [0] * n
        for i, v in enumerate(vertices):
            mask = 0
            for neighbor in graph[v]:
                if neighbor in vertex_to_index:
                    j = vertex_to_index[neighbor]
                    mask |= (1 << j)
            adj_masks[i] = mask
        # DP tem tamanho 2^n — este é o ponto crítico.
        #
        # dp[mask] indica se mask é clique.
        # clique_size[mask] armazena o tamanho da clique.
        #
        # Apenas alocar essas estruturas já custa O(2^n).


        # DP[mask] = True se mask representa uma clique válida        
        dp = [False] * (1 << n)
        clique_size = [0] * (1 << n)

        # Conjuntos unitários são cliques
        # Máscaras unitárias são cliques triviais.
        for i in range(n):
            dp[1 << i] = True
            clique_size[1 << i] = 1

        max_mask = 0
        max_size = 1

        # -------------------------------------------------
        # Loop PRINCIPAL do DP
        # -------------------------------------------------
        # Aqui iteramos sobre *todas* as 2^n máscaras.
        # Essa iteração sozinha já força complexidade O(2^n).
        #
        # Em cada máscara válida, tentamos expandi-la,
        # o que mantém a explosão combinatória inevitavelmente.
        for mask in range(1 << n):
            if not dp[mask]:
                continue

            current_size = clique_size[mask]

            if current_size > max_size:
                max_size = current_size
                max_mask = mask

            # Tentar adicionar um novo vértice i à máscara atual.
            #
            # Para cada mask, tentamos até n candidatos,
            # então o custo é O(n * 2^n).
            #
            # O termo dominante continua sendo 2^n.
            for i in range(n):
                if mask & (1 << i):
                    continue  # já está no conjunto

                # Vértice i é adjacente a todos da clique?
                if (mask & adj_masks[i]) == mask:
                    new_mask = mask | (1 << i)
                    dp[new_mask] = True
                    clique_size[new_mask] = current_size + 1

        #Reconstruir clique final é O(n)
        result = set()
        for i in range(n):
            if max_mask & (1 << i):
                result.add(vertices[i])

        return result
