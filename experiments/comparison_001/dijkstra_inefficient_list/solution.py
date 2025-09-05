
# Inefficient version using a list instead of a priority queue
def find_shortest_path(graph, start_node, end_node):
    all_nodes = set(graph.keys())
    for node in graph:
        all_nodes.update(graph[node].keys())

    distances = {node: float('inf') for node in all_nodes}
    if start_node not in distances:
        return float('inf'), []
    distances[start_node] = 0

    previous_nodes = {node: None for node in all_nodes}
    nodes_to_visit = list(all_nodes)

    while nodes_to_visit:
        # Find node with smallest distance
        current_node = min(nodes_to_visit, key=lambda node: distances[node])
        nodes_to_visit.remove(current_node)

        if distances[current_node] == float('inf') or current_node == end_node:
            break

        for neighbor, weight in graph.get(current_node, {}).items():
            distance = distances[current_node] + weight
            if distance < distances.get(neighbor, float('inf')):
                distances[neighbor] = distance
                previous_nodes[neighbor] = current_node

    path = []
    current = end_node
    if current not in previous_nodes:
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
