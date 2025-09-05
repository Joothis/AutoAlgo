
# Bellman-Ford algorithm, capable of handling negative weights.
def find_shortest_path(graph, start_node, end_node):
    all_nodes = set(graph.keys())
    for node in graph:
        all_nodes.update(graph[node].keys())

    distances = {node: float('inf') for node in all_nodes}
    if start_node not in distances:
        return float('inf'), []
    distances[start_node] = 0

    previous_nodes = {node: None for node in all_nodes}

    for _ in range(len(all_nodes) - 1):
        for node in all_nodes:
            for neighbor, weight in graph.get(node, {}).items():
                if distances[node] != float('inf') and distances[node] + weight < distances[neighbor]:
                    distances[neighbor] = distances[node] + weight
                    previous_nodes[neighbor] = node

    # Check for negative weight cycles (optional for this problem spec)
    # but good practice.
    for node in all_nodes:
        for neighbor, weight in graph.get(node, {}).items():
            if distances[node] != float('inf') and distances[node] + weight < distances[neighbor]:
                # Negative cycle detected
                return float('-inf'), []

    path = []
    current = end_node
    if current not in previous_nodes and start_node != end_node:
         # Handle unreachable nodes when start/end are different
        if distances[end_node] == float('inf'):
             return float('inf'), []

    while current is not None:
        path.insert(0, current)
        current = previous_nodes[current]

    if distances.get(end_node, float('inf')) == float('inf'):
        return float('inf'), []

    if start_node == end_node:
        return 0, [start_node]

    if path and path[0] == start_node:
        return distances[end_node], path
    else:
        return float('inf'), []
