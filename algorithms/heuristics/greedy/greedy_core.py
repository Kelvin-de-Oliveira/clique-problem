from typing import Set, Dict
from algorithms.base import CliqueAlgorithm
import random

class GreedyCliqueCoreDecomposition(CliqueAlgorithm):
    """Heurística baseada em k-core decomposition."""

    def _compute_core_numbers(self) -> Dict[int, int]:
        graph = self.graph

        # Calcula o grau inicial de cada vértice → O(n)
        degrees = {v: len(neigh) for v, neigh in graph.items()}

        # Ordena vértices pelo grau (para iniciar o processo do k-core) → O(n log n)
        vertices = sorted(degrees.keys(), key=lambda x: degrees[x])
        core = {}

        # Processo de k-core:
        # Remove vértices de menor grau repetidamente actualizando graus
        # Este processo no pior caso é O(n^2)
        while vertices:
            # Pega o vértice com menor grau atual (primeiro da lista)
            v = vertices.pop(0)
            core[v] = degrees[v]

            # Para cada vizinho, se ele tinha grau maior que v, reduz
            # Essa remoção encadeada é cara: pode ser O(n) por iteração
            for u in graph[v]:
                if degrees[u] > degrees[v]:
                    degrees[u] -= 1

            # Reordena toda a lista após atualizações → O(n log n) por iteração
            vertices.sort(key=lambda x: degrees[x])

        return core

    def run(self) -> Set[int]:
        # Calcula o core number de todos os vértices
        core_numbers = self._compute_core_numbers()
        
        # Ordena vértices pelo core number decrescente
        # Ideia: vértices com core alto são mais prováveis de formar grandes cliques
        sorted_vertices = sorted(
            core_numbers.keys(), key=lambda x: core_numbers[x], reverse=True
        )

        clique = set()

        # Constrói clique de forma gulosa
        for v in sorted_vertices:
            # Verifica se v é vizinho de todos da clique
            # Isto é O(|clique|)
            if all(v in self.graph[u] for u in clique):
                clique.add(v)

        return clique
