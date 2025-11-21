from typing import Set, List, Dict
from algorithms.base import CliqueAlgorithm
from algorithms.exact.brute_force import BruteForceClique
from algorithms.exact.backtracking import BacktrackingClique

class DivideConquerClique(CliqueAlgorithm):
    """Classe para abordagem divisão e conquista (componentes conexos)."""
    def __init__(self, graph: Dict[int, Set[int]]):
        super().__init__(graph)

    def run(self) -> Set[int]:
        if not self.graph:
            return set()
        # Dividimos o grafo em componentes conexos.
        # Esta etapa custa no máximo O(n + m) e NÃO afeta a complexidade exponencial.
        components = self._connected_components()
        max_clique: Set[int] = set()
         # A divisão em componentes reduz o problema SOMENTE
        # quando o grafo tem partes realmente separadas.
        # Mas no pior caso, o grafo inteiro é um ÚNICO componente conexo.
        #
        # Nesse pior caso, "components" tem exatamente 1 conjunto de n vértices
        # → nenhuma divisão ocorre
        for comp in components:
            sub = self._induced_subgraph(comp)
             # A divisão em componentes reduz o problema SOMENTE
            # quando o grafo tem partes realmente separadas.
            # Mas no pior caso, o grafo inteiro é um ÚNICO componente conexo.
            #
            # Nesse pior caso, "components" tem exatamente 1 conjunto de n vértices
            # → nenhuma divisão ocorre

            if len(comp) <= 20:
                solver = BruteForceClique(sub)
            else:
                solver = BacktrackingClique(sub)
            # Aqui o solver é executado.
            # No pior caso, BacktrackingClique(sub) = O(2^n).
            comp_clique = solver.run()
            if len(comp_clique) > len(max_clique):
                max_clique = comp_clique
        return max_clique

    def _connected_components(self) -> List[Set[int]]:
    # DFS iterativo para componentes.    
    # Complexidade O(n + m).
    # Isso é polinomial e NÃO altera a complexidade exponencial.
        visited = set()
        components: List[Set[int]] = []
        for vertex in self.graph:
            if vertex not in visited:
                comp = set()
                stack = [vertex]
                while stack:
                    cur = stack.pop()
                    if cur not in visited:
                        visited.add(cur)
                        comp.add(cur)
                        for neigh in self.graph[cur]:
                            if neigh not in visited:
                                stack.append(neigh)
                components.append(comp)
        return components

    def _induced_subgraph(self, vertices: Set[int]) -> Dict[int, Set[int]]:
        # Criar subgrafo induzido é O(n²) no pior caso,
        # mas isso continua sendo irrelevante frente ao solver O(2^n).
        return {v: self.graph[v].intersection(vertices) for v in vertices}
