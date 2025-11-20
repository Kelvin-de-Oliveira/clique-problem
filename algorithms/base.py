from typing import Set, Dict

class CliqueAlgorithm:
    """Interface mínima para algoritmos de clique."""
    def __init__(self, graph: Dict[int, Set[int]]):
        # Normaliza grafo para conjuntos
        self.graph = {v: set(neigh) for v, neigh in graph.items()}

    def run(self) -> Set[int]:
        """Roda o algoritmo e retorna a clique máxima (conjunto de vértices)."""
        raise NotImplementedError
