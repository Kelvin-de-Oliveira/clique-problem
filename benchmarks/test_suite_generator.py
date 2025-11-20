import random
from graphs.generators import generate_random_graph

class TestSuiteGenerator:
    """
    Classe ajustada para gerar suítes controladas por tamanho de grafo e semente,
    separadas por tipo de algoritmo.
    """

    @staticmethod
    def generate_graphs_for_algorithm(ns, p=0.1, instances_per_n=3):
        """
        Gera múltiplas instâncias de grafos aleatórios para cada n em ns.
        """
        graphs = []
        for n in ns:
            for seed in range(instances_per_n):
                random.seed(seed)  # para reprodutibilidade
                g = generate_random_graph(n, p)
                graphs.append((n, g))  # tupla (tamanho, grafo)
        return graphs

    @classmethod
    def generate_test_suite(cls):
        """
        Retorna um dicionário com as suítes ajustadas para cada tipo de algoritmo.
        """
        # Série de n por tipo de algoritmo
        ns_expo = [6, 8, 10, 12, 14, 16, 18, 20, 22, 24]       # força bruta / DP
        ns_bt = [10, 12, 14, 16, 18, 20, 22, 24, 26, 28]       # backtracking
        ns_heur = [30, 50, 80, 120, 200, 300, 450, 700]        # heurísticas/gulosos

        return {
            "forca_bruta": cls.generate_graphs_for_algorithm(ns_expo, p=0.1),
            "programacao_dinamica": cls.generate_graphs_for_algorithm(ns_expo, p=0.1),
            "backtracking": cls.generate_graphs_for_algorithm(ns_bt, p=0.1),
            "guloso_grau": cls.generate_graphs_for_algorithm(ns_heur, p=0.1),
            "guloso_reinicios": cls.generate_graphs_for_algorithm(ns_heur, p=0.1),
            "guloso_min_degree": cls.generate_graphs_for_algorithm(ns_heur, p=0.1),
            "guloso_core": cls.generate_graphs_for_algorithm(ns_heur, p=0.1),
            "heuristica_coloring": cls.generate_graphs_for_algorithm(ns_heur, p=0.1),
            "heuristica_local_search": cls.generate_graphs_for_algorithm(ns_heur, p=0.1),
            "meta_heuristica_genetico": cls.generate_graphs_for_algorithm(ns_heur, p=0.1),
        }
