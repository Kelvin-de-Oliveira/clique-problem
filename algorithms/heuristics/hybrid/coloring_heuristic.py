from typing import Dict, Set, List
from algorithms.base import CliqueAlgorithm


class ColoringHeuristicClique(CliqueAlgorithm):
    """
    Heurística de clique baseada em coloração gulosa.
    Complexidade total aproximada: O(n²) em grafos representados por listas
    de adjacência (dominado pelas verificações de vizinhança).
    """

    def __init__(self, graph: Dict[int, Set[int]]):
        super().__init__(graph)

    # -----------------------------------------------------------
    # 1) Coloração gulosa — retorna um dicionário {v: cor}
    # -----------------------------------------------------------
    def _greedy_coloring(self) -> Dict[int, int]:
        # Ordenar vértices por grau: O(n log n)
        colors = {}
        for v in sorted(self.graph, key=lambda x: -len(self.graph[x])):
            # Coletar cores dos vizinhos já coloridos: O(grau(v))
            neighbor_colors = {colors[n] for n in self.graph[v] if n in colors}

            # Encontrar a menor cor disponível: O(k), k = cores usadas (<= n)
            color = 0
            while color in neighbor_colors:
                color += 1

            colors[v] = color
        # Custo total típico: O( ∑ grau(v) ) = O(m), pior caso O(n²)
        return colors

    # -----------------------------------------------------------
    # 2) Constroi clique iterativamente com base nas classes de cor
    # -----------------------------------------------------------
    def _build_clique_from_coloring(self, colors: Dict[int, int]) -> Set[int]:
        clique: Set[int] = set()

        # Agrupar vértices por cor: O(n)
        color_classes: Dict[int, List[int]] = {}
        for v, c in colors.items():
            color_classes.setdefault(c, []).append(v)

        # Para cada classe de cor (<= n classes)
        for color in sorted(color_classes.keys()):
            for v in color_classes[color]:
                # Testar se v é adjacente a todos da clique: O(|clique|) ⊆ O(n)
                if all(v in self.graph[u] for u in clique):
                    clique.add(v)
        # Pior caso: O(n²)
        return clique

    def run(self) -> Set[int]:
        # Coloração → O(n²)
        colors = self._greedy_coloring()

        # Construção da clique → O(n²)
        clique = self._build_clique_from_coloring(colors)

        # Complexidade total: O(n²) típico / O(n² + m) geral
        return clique
