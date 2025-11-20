from graphs.generators import generate_random_graph, generate_scale_free_graph, generate_clique_based_graph

class TestSuiteGenerator:
    """
    Classe responsável apenas por gerar suítes de grafos para benchmarks.
    """
    @staticmethod
    def generate_small_graphs():
        return [
            generate_random_graph(15, 0.3),
            generate_random_graph(15, 0.5),
            generate_random_graph(15, 0.7),
            generate_random_graph(20, 0.3),
            generate_random_graph(20, 0.5)
        ]

    @staticmethod
    def generate_medium_graphs():
        return [
            generate_random_graph(30, 0.2),
            generate_random_graph(30, 0.4),
            generate_random_graph(50, 0.2),
            generate_random_graph(50, 0.3)
        ]

    @staticmethod
    def generate_large_graphs():
        return [
            generate_random_graph(100, 0.1),
            generate_random_graph(100, 0.2),
            generate_random_graph(200, 0.1)
        ]

    @staticmethod
    def generate_scale_free_graphs():
        return [
            generate_scale_free_graph(50, 2),
            generate_scale_free_graph(100, 3),
            generate_scale_free_graph(200, 4)
        ]

    @staticmethod
    def generate_clique_based_graphs():
        return [
            generate_clique_based_graph(30, 8, 50),
            generate_clique_based_graph(50, 12, 100),
            generate_clique_based_graph(100, 15, 200)
        ]

    @classmethod
    def generate_test_suite(cls):
        """
        Retorna um dicionário com todas as suítes de teste.
        """
        return {
            "pequenos_aleatorios": cls.generate_small_graphs(),
            "medios_aleatorios": cls.generate_medium_graphs(),
            "grandes_aleatorios": cls.generate_large_graphs(),
            "scale_free": cls.generate_scale_free_graphs(),
            "clique_embutida": cls.generate_clique_based_graphs()
        }
