"""
Designer agent.
"""
import textwrap

class DesignerAgent:
    """
    The Designer agent is responsible for proposing an algorithm design
    based on a given problem specification.
    """

    def __init__(self, llm_client=None):
        """
        Initializes the DesignerAgent.

        Args:
            llm_client: A client for a large language model API. For the MVP,
                        this is simulated.
        """
        self.llm_client = llm_client

    def _create_prompt(self, problem_spec: str) -> str:
        """
        Creates a prompt for the LLM to generate an algorithm.
        """
        return textwrap.dedent(f"""
            You are an expert algorithm designer. Based on the following problem
            specification, provide a Python implementation of a suitable algorithm.

            The implementation should be a single function that adheres to the
            signature and output format described in the specification. The function
            should be self-contained and not rely on any external libraries that are
            not part of the standard Python library.

            Problem Specification:
            ---
            {problem_spec}
            ---

            Please provide only the Python code for the function.
        """).strip()

    def propose_algorithms(self, problem_spec: str) -> list[dict]:
        """
        Proposes multiple algorithm variations for the given problem spec.

        Args:
            problem_spec: The detailed problem specification.

        Returns:
            A list of dictionaries, where each dict contains a variation_id and the code.
        """
        prompt = self._create_prompt(problem_spec)

        if self.llm_client:
            # In a real implementation, you would call the LLM here, perhaps in a loop
            # or with a more complex prompt asking for multiple variations.
            pass

        # For the MVP, we simulate the LLM call by returning hardcoded solutions.
        return self._simulate_llm_responses(prompt)

    def _simulate_llm_responses(self, prompt: str) -> list[dict]:
        """
        Simulates a response from an LLM for the shortest path problem,
        providing multiple variations.
        """
        
        optimal_code = textwrap.dedent('''
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
        ''')

        inefficient_code = textwrap.dedent('''
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
        ''')

        buggy_code = textwrap.dedent('''
            import heapq

            # Buggy version: Fails the start_node == end_node test
            def find_shortest_path(graph, start_node, end_node):
                if start_node == end_node:
                    # Incorrectly returns an empty path
                    return 0, [] 

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

                if path and path[0] == start_node:
                    return distances[end_node], path
                else:
                    return float('inf'), []
        ''')

        bellman_ford_code = textwrap.dedent('''
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
        ''')

        return [
            {"variation_id": "dijkstra_optimal", "code": optimal_code, "prompt": prompt},
            {"variation_id": "dijkstra_inefficient_list", "code": inefficient_code, "prompt": prompt},
            {"variation_id": "dijkstra_buggy_edge_case", "code": buggy_code, "prompt": prompt},
            {"variation_id": "bellman_ford_correct", "code": bellman_ford_code, "prompt": prompt},
        ]

