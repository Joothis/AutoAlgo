
import heapq

def find_shortest_path(graph, start_node, end_node):
    all_nodes = set(graph.keys())
    for node in graph:
        all_nodes.update(graph[node].keys())

    distances = {node: float('inf') for node in all_nodes}
    if start_node not in distances:
        return float('inf'), []
    distances[start_node] = 0

    previous_nodes = {node: None for node in all_nodes}
    priority_queue = [(0, start_node)]

    while priority_queue:
        current_distance, current_node = heapq.heappop(priority_queue)

        if current_distance > distances[current_node]:
            continue

        if current_node == end_node:
            break

        for neighbor, weight in graph.get(current_node, {}).items():
            distance = current_distance + weight

            if distance < distances.get(neighbor, float('inf')):
                distances[neighbor] = distance
                previous_nodes[neighbor] = current_node
                heapq.heappush(priority_queue, (distance, neighbor))

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
