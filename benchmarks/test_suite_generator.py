import random
from graphs.generators import generate_random_graph

class TestSuiteGenerator:
    """
    Classe ajustada para gerar suítes controladas por tamanho de grafo e semente,
    separadas por tipo de algoritmo.
    """

    @staticmethod
    def generate_graphs_for_algorithm(ns, tipos_grafo=("random", "scale_free", "clique"), instances_per_n=3, **kwargs):
        """
        Gera múltiplas instâncias de grafos de diferentes tipos para cada tamanho n.
        Retorna lista de tuplas: (n, tipo_grafo, grafo)
        """
        from graphs.generators import generate_graph  # usando função que encapsula tipos

        graphs = []
        for n in ns:
            for seed in range(instances_per_n):
                for tipo in tipos_grafo:
                    random.seed(seed)
                    g = generate_graph(n, tipo=tipo, **kwargs)
                    graphs.append((n, tipo, g))  # armazenamos também o tipo de grafo
        return graphs

    @classmethod
    def generate_test_suite(cls):
        ns_expo = [6, 8, 10, 12, 14, 16, 18, 20, 22, 24]       # força bruta / DP
        ns_bt = [10, 12, 14, 16, 18, 20, 22, 24, 26, 28]       # backtracking
        ns_heur = [30, 50, 80, 120, 200, 300, 450, 700, 900, 1000]        # heurísticas/gulosos

        tipos_grafo = ("random", "scale_free", "clique")

        return {
            "forca_bruta": cls.generate_graphs_for_algorithm(ns_expo, tipos_grafo=tipos_grafo),
            "programacao_dinamica": cls.generate_graphs_for_algorithm(ns_expo, tipos_grafo=tipos_grafo),
            "backtracking": cls.generate_graphs_for_algorithm(ns_bt, tipos_grafo=tipos_grafo),
            "guloso_grau": cls.generate_graphs_for_algorithm(ns_heur, tipos_grafo=tipos_grafo),
            "guloso_reinicios": cls.generate_graphs_for_algorithm(ns_heur, tipos_grafo=tipos_grafo),
            "guloso_min_degree": cls.generate_graphs_for_algorithm(ns_heur, tipos_grafo=tipos_grafo),
            "guloso_core": cls.generate_graphs_for_algorithm(ns_heur, tipos_grafo=tipos_grafo),
            "heuristica_coloring": cls.generate_graphs_for_algorithm(ns_heur, tipos_grafo=tipos_grafo),
            "heuristica_local_search": cls.generate_graphs_for_algorithm(ns_heur, tipos_grafo=tipos_grafo),
            "meta_heuristica_genetico": cls.generate_graphs_for_algorithm(ns_heur, tipos_grafo=tipos_grafo),
        }
