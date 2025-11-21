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
        # Verificação completa: O(k²), onde k = |clique|
        for u in clique:
            for v in clique:
                if u != v and v not in graph[u]:
                    return False
        return True

    def _fitness(self, clique: Set[int]) -> int:
        # Apenas chama _is_clique → O(k²)
        return len(clique) if self._is_clique(self.graph, clique) else 0

    def _repair(self, clique: Set[int]) -> Set[int]:
        # Ordenação O(k log k)
        # Construção checando compatibilidade: O(k²)
        # Total: O(k²)
        graph = self.graph
        valid = set()
        for v in sorted(clique, key=lambda x: len(graph[x]), reverse=True):
            if all(v in graph[u] for u in valid):  # O(k)
                valid.add(v)
        return valid

    def _crossover(self, p1: Set[int], p2: Set[int]) -> Set[int]:
        # União O(k)
        # Reparo O(k²)
        return self._repair(p1.union(p2))

    def _mutate(self, clique: Set[int]) -> Set[int]:
        # Seleção aleatória de até 3 vértices: O(1)
        # Cada tentativa verifica compatibilidade: O(k)
        # Total: O(k)
        if random.random() < self.mutation_rate:
            graph = self.graph
            candidates = set(graph.keys()) - clique
            for v in random.sample(list(candidates), min(3, len(candidates))):
                if all(v in graph[u] for u in clique):  # O(k)
                    clique.add(v)
        return clique

    # -----------------------------
    # População inicial
    # -----------------------------

    def _random_clique(self) -> Set[int]:
        # Embaralhamento O(n)
        # Tentativa de inserção: O(n * k) ≈ O(n²) no pior caso
        graph = self.graph
        vertices = list(graph.keys())
        random.shuffle(vertices)

        clique = set()
        for v in vertices:
            if all(v in graph[u] for u in clique):  # O(k)
                clique.add(v)
        return clique

    def _initial_population(self) -> List[Set[int]]:
        # Gera P indivíduos → P * O(n²)
        return [self._random_clique() for _ in range(self.population_size)]

    # -----------------------------
    # Execução principal
    # -----------------------------

    def run(self) -> Set[int]:
        """
        Complexidade geral:
        - Cada geração faz:
            * ordenação da população: O(P log P * k²)
            * reprodução + mutação: O(P * k²)
        - Total: O(G * P * k²)
        Onde:
            n = |V|
            k = tamanho médio das cliques
            P = população
            G = gerações
        """
        population = self._initial_population()  # O(P * n²)

        for _ in range(self.generations):
            # seleção: ordena por fitness (fitness = O(k²)) → O(P log P * k²)
            population.sort(key=lambda c: self._fitness(c), reverse=True)
            survivors = population[: self.population_size // 2]

            # reprodução
            new_population = survivors.copy()
            while len(new_population) < self.population_size:
                p1, p2 = random.sample(survivors, 2)  # O(1)
                child = self._crossover(p1, p2)       # O(k²)
                child = self._mutate(child)           # O(k)
                new_population.append(child)

            population = new_population  # O(1)

        # melhor indivíduo final: O(P * k²)
        best = max(population, key=lambda c: self._fitness(c))
        return best
