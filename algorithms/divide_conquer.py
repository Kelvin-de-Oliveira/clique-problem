from typing import Set, List, Dict
from algorithms.brute_force import brute_force_max_clique
from algorithms.backtracking import BacktrackingClique

def divide_conquer_clique(graph: Dict[int, Set[int]]) -> Set[int]:
    """
    Abordagem de divisão e conquista para clique máxima.
    Divide por componentes conexos e combina soluções.
    """
    if not graph:
        return set()

    components = connected_components(graph)

    max_clique = set()
    for component in components:
        subgraph = induced_subgraph(graph, component)

        # Para componentes pequenos, usar força bruta
        if len(component) <= 20:
            component_clique = brute_force_max_clique(subgraph)
        else:
            # Para componentes grandes, usar backtracking
            solver = BacktrackingClique(subgraph)
            component_clique = solver.backtracking_max_clique()

        if len(component_clique) > len(max_clique):
            max_clique = component_clique

    return max_clique

def connected_components(graph: Dict[int, Set[int]]) -> List[Set[int]]:
    """Encontra todos os componentes conexos do grafo"""
    visited = set()
    components = []

    for vertex in graph:
        if vertex not in visited:
            component = set()
            stack = [vertex]

            while stack:
                current = stack.pop()
                if current not in visited:
                    visited.add(current)
                    component.add(current)
                    for neighbor in graph[current]:
                        if neighbor not in visited:
                            stack.append(neighbor)

            components.append(component)

    return components

def induced_subgraph(graph: Dict[int, Set[int]], vertices: Set[int]) -> Dict[int, Set[int]]:
    """Extrai subgrafo induzido por um conjunto de vértices"""
    subgraph = {}
    for vertex in vertices:
        subgraph[vertex] = graph[vertex].intersection(vertices)
    return subgraph
