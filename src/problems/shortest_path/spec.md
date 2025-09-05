### Problem: Weighted Shortest Path

**Objective:** Implement a function `find_shortest_path` that finds the shortest path between a `start_node` and an `end_node` in a weighted, directed graph.

**Input:**
- `graph`: A dictionary representing the graph's adjacency list. 
  - Keys are node identifiers (strings).
  - Values are dictionaries where keys are neighbor node identifiers and values are the integer weights of the edges.
- `start_node`: The identifier of the starting node.
- `end_node`: The identifier of the ending node.

**Output:**
- A tuple containing two elements:
  1. The total cost (integer) of the shortest path.
  2. A list of node identifiers representing the shortest path from start to end.
- If no path exists, the function should return `(float('inf'), [])`.

**Example:**
```python
graph = {
    'A': {'B': 1, 'C': 4},
    'B': {'C': 2, 'D': 5},
    'C': {'D': 1},
    'D': {}
}
start_node = 'A'
end_node = 'D'

# Expected output:
# (4, ['A', 'B', 'C', 'D'])
```

