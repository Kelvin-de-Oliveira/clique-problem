from typing import Dict, Set, List
from algorithms.base import CliqueAlgorithm


class ColoringHeuristicClique(CliqueAlgorithm):
    """
    Heurística híbrida baseada em:
      1) Coloração gulosa do grafo (resultando em classes de cor)
      2) Escolha de vértices dentro das classes mais promissoras
      3) Construção iterativa de uma clique válida

    Não garante ótimo, mas é rápida e costuma gerar cliques boas
    em grafos aleatórios, densos e scale-free.
    """

    def __init__(self, graph: Dict[int, Set[int]]):
        super().__init__(graph)

    # -----------------------------------------------------------
    # 1) Coloração gulosa — retorna um dicionário {v: cor}
    # -----------------------------------------------------------
    def _greedy_coloring(self) -> Dict[int, int]:
        colors = {}
        for v in sorted(self.graph, key=lambda x: -len(self.graph[x])):
            neighbor_colors = {colors[n] for n in self.graph[v] if n in colors}
            color = 0
            while color in neighbor_colors:
                color += 1
            colors[v] = color
        return colors

    # -----------------------------------------------------------
    # 2) Tenta construir uma clique escolhendo vértices por cor
    # -----------------------------------------------------------
    def _build_clique_from_coloring(self, colors: Dict[int, int]) -> Set[int]:
        clique: Set[int] = set()

        # Agrupar vértices por cor
        color_classes: Dict[int, List[int]] = {}
        for v, c in colors.items():
            color_classes.setdefault(c, []).append(v)

        # Processar cores em ordem crescente (classes menores primeiro)
        for color in sorted(color_classes.keys()):
            for v in color_classes[color]:
                # Verifica se pode entrar na clique
                if all(v in self.graph[u] for u in clique):
                    clique.add(v)

        return clique

    def run(self) -> Set[int]:
        colors = self._greedy_coloring()
        clique = self._build_clique_from_coloring(colors)
        return clique
