"""
Input generators for the shortest path problem.
"""
import random

def generate_random_graph(num_nodes: int, edge_density: float) -> dict:
    """
    Generates a random weighted, directed graph.

    Args:
        num_nodes: The number of nodes in the graph.
        edge_density: The probability (0.0 to 1.0) of an edge existing between
                      any two nodes.

    Returns:
        A dictionary representing the graph's adjacency list.
    """
    graph = {i: {} for i in range(num_nodes)}
    max_weight = 100

    for i in range(num_nodes):
        for j in range(num_nodes):
            if i != j and random.random() < edge_density:
                weight = random.randint(1, max_weight)
                graph[i][j] = weight
    
    return graph

def generate_shortest_path_inputs(num_nodes: int, edge_density: float):
    """
    Generates a graph and a random start/end node pair for that graph.
    """
    graph = generate_random_graph(num_nodes, edge_density)
    
    # Ensure there are nodes to choose from
    if not graph:
        return graph, None, None

    nodes = list(graph.keys())
    start_node = random.choice(nodes)
    end_node = random.choice(nodes)
    
    return graph, start_node, end_node

