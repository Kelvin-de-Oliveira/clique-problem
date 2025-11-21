import random
import networkx as nx

def generate_random_graph(n: int, p: float) -> dict:
    """Gera grafo aleatório Erdős–Rényi G(n, p)."""
    graph = {i: set() for i in range(n)}

    for i in range(n):
        for j in range(i + 1, n):
            if random.random() < p:
                graph[i].add(j)
                graph[j].add(i)

    return graph

def generate_scale_free_graph(n: int, m: int) -> dict:
    """Gera grafo scale–free pelo modelo Barabási–Albert."""
    G = nx.barabasi_albert_graph(n, m)
    graph = {node: set(G.neighbors(node)) for node in G.nodes()}
    return graph

def generate_clique_based_graph(n: int, clique_size: int, noise_edges: int) -> dict:
    """Gera um grafo contendo uma clique grande embutida + ruído."""
    graph = {i: set() for i in range(n)}

    # Criar clique embutida
    for i in range(clique_size):
        for j in range(i + 1, clique_size):
            graph[i].add(j)
            graph[j].add(i)

    # Arestas aleatórias adicionais
    for _ in range(noise_edges):
        u = random.randint(0, n - 1)
        v = random.randint(0, n - 1)
        if u != v:
            graph[u].add(v)
            graph[v].add(u)

    return graph

def generate_graph(n, tipo, **kwargs):
    if tipo == "random":
        return generate_random_graph(n, kwargs.get("p", 0.1))
    elif tipo == "scale_free":
        return generate_scale_free_graph(n, kwargs.get("m", 2))
    elif tipo == "clique":
        return generate_clique_based_graph(
            n,
            kwargs.get("clique_size", min(5, n)),
            kwargs.get("noise_edges", n)
        )
    else:
        raise ValueError(f"Tipo de grafo desconhecido: {tipo}")
