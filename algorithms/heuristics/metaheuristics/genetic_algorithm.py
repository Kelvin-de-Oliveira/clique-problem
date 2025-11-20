from typing import Set, Dict, List
from algorithms.base import CliqueAlgorithm
import random


class GeneticAlgorithmClique(CliqueAlgorithm):
    """
    Algoritmo Genético para busca de cliques grandes.
    """

    def __init__(
        self,
        graph: Dict[int, Set[int]],
        population_size: int = 50,
        generations: int = 100,
        mutation_rate: float = 0.1
    ):
        super().__init__(graph)
        self.population_size = population_size
        self.generations = generations
        self.mutation_rate = mutation_rate

    # -----------------------------
    # Funções auxiliares
    # -----------------------------

    @staticmethod
    def _is_clique(graph: Dict[int, Set[int]], clique: Set[int]) -> bool:
        """Verifica se o conjunto é uma clique válida."""
        for u in clique:
            for v in clique:
                if u != v and v not in graph[u]:
                    return False
        return True

    def _fitness(self, clique: Set[int]) -> int:
        """Fitness é o tamanho da clique se válida, senão 0."""
        return len(clique) if self._is_clique(self.graph, clique) else 0

    def _repair(self, clique: Set[int]) -> Set[int]:
        """
        Repara uma clique inválida retirando vértices conflitantes.
        Usa ordenação por grau para estabilidade.
        """
        graph = self.graph
        valid = set()
        for v in sorted(clique, key=lambda x: len(graph[x]), reverse=True):
            if all(v in graph[u] for u in valid):
                valid.add(v)
        return valid

    def _crossover(self, p1: Set[int], p2: Set[int]) -> Set[int]:
        """Cruzamento: união seguida de reparo."""
        child = p1.union(p2)
        return self._repair(child)

    def _mutate(self, clique: Set[int]) -> Set[int]:
        """Mutação: tenta adicionar vértices aleatórios."""
        if random.random() < self.mutation_rate:
            graph = self.graph
            candidates = set(graph.keys()) - clique
            # tenta adicionar até 3 vértices compatíveis
            for v in random.sample(list(candidates), min(3, len(candidates))):
                if all(v in graph[u] for u in clique):
                    clique.add(v)
        return clique

    # -----------------------------
    # População inicial
    # -----------------------------

    def _random_clique(self) -> Set[int]:
        """Gera uma clique inicial válida usando construção gulosa aleatória."""
        graph = self.graph
        vertices = list(graph.keys())
        random.shuffle(vertices)

        clique = set()
        for v in vertices:
            if all(v in graph[u] for u in clique):
                clique.add(v)
        return clique

    def _initial_population(self) -> List[Set[int]]:
        """Gera população de cliques iniciais válidas."""
        return [self._random_clique() for _ in range(self.population_size)]

    # -----------------------------
    # Execução principal
    # -----------------------------

    def run(self) -> Set[int]:
        """Executa o Algoritmo Genético."""
        population = self._initial_population()

        for _ in range(self.generations):
            # seleção: escolhe 50% melhores
            population.sort(key=lambda c: self._fitness(c), reverse=True)
            survivors = population[: self.population_size // 2]

            # reprodução
            new_population = survivors.copy()
            while len(new_population) < self.population_size:
                p1, p2 = random.sample(survivors, 2)
                child = self._crossover(p1, p2)
                child = self._mutate(child)
                new_population.append(child)

            population = new_population

        # melhor indivíduo final
        best = max(population, key=lambda c: self._fitness(c))
        return best
