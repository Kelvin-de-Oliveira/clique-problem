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

        # O algoritmo será repetido num_restarts vezes.
        # Isso não cria exponencialidade, apenas multiplica a complexidade por um fator constante.
        for _ in range(self.num_restarts):

            # Cada reinicialização embaralha a ordem dos vértices
            # Isso altera o comportamento guloso a cada tentativa.
            random.shuffle(vertices)

            clique = set()
            candidates = set(vertices)

            # Enquanto ainda houver vértices candidatos para tentar entrar na clique
            while candidates:

                # Escolhe um vértice aleatório entre os candidatos
                # Este passo é O(1), mas será executado várias vezes
                vertex = random.choice(list(candidates))

                # Verifica se o vértice escolhido é adjacente a *todos* da clique atual
                # Isso custa O(|clique|) no pior caso.
                if all(vertex in graph[v] for v in clique):

                    # Se sim, adiciona à clique
                    clique.add(vertex)

                    # Atualiza candidatos para manter apenas os vizinhos do novo vértice
                    # Essa interseção custa O(n)
                    candidates = candidates.intersection(graph[vertex])

                else:
                    # Caso não entre, removemos o vértice do conjunto de candidatos
                    candidates.remove(vertex)

            # Após terminar o loop, atualiza a maior clique encontrada
            if len(clique) > len(best_clique):
                best_clique = clique

        return best_clique
