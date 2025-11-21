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

        # Conjunto de candidatos começa com todos os vértices.
        # O tamanho é n e vamos reduzir conforme escolhemos vértices.
        candidates = set(graph.keys())

        # Loop principal: a cada iteração escolhemos 1 vértice
        # ou removemos 1 vértice de candidates.
        #
        # Portanto, o loop pode executar até n vezes.
        while candidates:
            best_vertex = None
            best_degree = -1

            # Escolher o melhor vértice exige percorrer todos os candidatos.
            #
            # Para cada vértice, precisamos calcular:
            #   len(graph[vertex].intersection(candidates))
            #
            # intersection() é O(n) no pior caso,
            # e fazemos isso para até n candidatos.
            #
            # Portanto, esta seleção é O(n²) no pior caso.
            for vertex in candidates:
                current_degree = len(graph[vertex].intersection(candidates))
                if current_degree > best_degree:
                    best_vertex = vertex
                    best_degree = current_degree

            if best_vertex is None:
                break

            # Verificar se o vértice pode entrar na clique custa O(k),
            # onde k = tamanho atual da clique.
            # No pior caso, k ≤ n, então é O(n).
            if all(best_vertex in graph[v] for v in clique):
                # Inserir vértice na clique é O(1)
                clique.add(best_vertex)
                # Atualizar candidatos = candidates ∩ vizinhos(best_vertex).
                #
                # intersection() novamente é O(n).
                candidates = candidates.intersection(graph[best_vertex])
            else:
                # Remover vértice dos candidatos é O(1)
                candidates.remove(best_vertex)
        # O custo total da heurística é dominado pelo loop de seleção O(n²).
        #
        # Como o loop externo roda no máximo n vezes,
        # o limite superior permanece O(n²).
        return clique
