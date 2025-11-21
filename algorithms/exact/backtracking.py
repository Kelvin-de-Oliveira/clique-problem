from typing import Set, Dict
from algorithms.base import CliqueAlgorithm

class BacktrackingClique(CliqueAlgorithm):
    """Classe Backtracking já existente, adaptada para .run()."""
    def __init__(self, graph: Dict[int, Set[int]]):
        super().__init__(graph)
        # Ordenamos os vértices por grau decrescente.
        # Isso ajuda bastante na prática, mas não muda o pior caso assintótico:
        # mesmo ordenando, ainda podemos explorar quase todos os subconjuntos.
        self.vertices = sorted(self.graph.keys(), key=lambda x: len(self.graph[x]), reverse=True)
        self.best_clique: Set[int] = set()
        self.current_clique: Set[int] = set()

    def run(self) -> Set[int]:
        return self.backtracking_max_clique()

    def backtracking_max_clique(self) -> Set[int]:
        self._backtrack(0)
        return self.best_clique

    def _backtrack(self, start_index: int):
        # PODA: se mesmo pegando todos os restantes não supero a best, retorno.
        # Esta poda reduz muito a busca média, mas no pior caso (ex: grafo completo),
        # esta condição NUNCA é acionada.
        #
        # Em um grafo completo: len(current) + (n - start_index) SEMPRE cresce,
        # então nunca ocorre retorno antecipado.
        #
        # Nesse cenário, o algoritmo vai explorar TODOS os subconjuntos possíveis.

        if len(self.current_clique) + (len(self.vertices) - start_index) <= len(self.best_clique):
            return
        
        # Este loop tenta incluir ou não incluir cada vértice.
        # Essa decisão binária (incluir / não incluir) gera uma árvore de busca
        # com até 2ⁿ folhas no pior caso.
        for i in range(start_index, len(self.vertices)):
            vertex = self.vertices[i]
            # Testa se pode adicionar o vértice à clique atual.
            # Isto é O(k) para clique atual de tamanho k,
            # mas isso é insignificante comparado à árvore exponencial gerada.
            if self._can_add_to_clique(vertex):
                self.current_clique.add(vertex)
                 # Atualiza melhor clique.
                # Não muda a complexidade, apenas mantém o melhor tamanho.
                if len(self.current_clique) > len(self.best_clique):
                    self.best_clique = self.current_clique.copy()
                # Chamamos recursivamente para o próximo vértice.
                # Em um grafo completo, nada impede a inclusão,
                # então todas as ramificações são visitadas.
                #
                # Isso significa que a árvore de recursão tem tamanho O(2ⁿ).
                self._backtrack(i + 1)
                # Remover o vértice faz parte do backtracking.
                self.current_clique.remove(vertex)

    def _can_add_to_clique(self, vertex: int) -> bool:
        # Checa se 'vertex' é adjacente a toda a clique atual.
        # É O(k), mas novamente, irrelevante comparado ao custo exponencial.
        #
        # Em grafos completos, este teste SEMPRE retorna True.
        # Isso permite que a árvore de recursão cresça ao máximo
        return all(vertex in self.graph[v] for v in self.current_clique)

