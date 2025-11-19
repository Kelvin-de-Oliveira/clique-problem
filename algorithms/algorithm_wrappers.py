from algorithms.backtracking import BacktrackingClique
from algorithms.brute_force import brute_force_max_clique
from algorithms.divide_conquer import divide_conquer_clique

def backtracking_max_clique_wrapper(graph):
    graph = {v: set(neigh) for v, neigh in graph.items()}
    bt = BacktrackingClique(graph)
    return bt.backtracking_max_clique()

def brute_force_max_clique_wrapper(graph):
    graph = {v: set(neigh) for v, neigh in graph.items()}
    return brute_force_max_clique(graph)

def divide_conquer_clique_wrapper(graph):
    return divide_conquer_clique(graph)