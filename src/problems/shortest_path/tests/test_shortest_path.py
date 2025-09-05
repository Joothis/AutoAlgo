
import pytest
from importlib import import_module
import sys
import os

# This is a placeholder for the solution module.
# The orchestrator will dynamically replace this with the actual module path.
SOLUTION_MODULE_PATH = "experiments.comparison_001.bellman_ford_correct.solution"

# Add the project root to the Python path to allow for absolute imports
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

@pytest.fixture
def find_shortest_path_func():
    """
    Dynamically imports the find_shortest_path function from the module
    specified by SOLUTION_MODULE_PATH. This allows tests to be run against
    any generated solution file.
    """
    try:
        # Ensure the temp_solution module can be found
        # The orchestrator will be responsible for creating this file.
        solution_module = import_module(SOLUTION_MODULE_PATH)
        return solution_module.find_shortest_path
    except ImportError:
        pytest.skip(f"Could not import solution from {SOLUTION_MODULE_PATH}. "
                    "This test is skipped if the solution has not been generated yet.")
    except AttributeError:
        pytest.fail(f"The solution module at {SOLUTION_MODULE_PATH} does not have a "
                    "`find_shortest_path` function.")


@pytest.fixture
def sample_graph():
    """A sample graph for testing."""
    return {
        'A': {'B': 1, 'C': 4},
        'B': {'C': 2, 'D': 5},
        'C': {'D': 1},
        'D': {'E': 2},
        'E': {'F': 1},
        'F': {}
    }

def test_simple_path(find_shortest_path_func, sample_graph):
    """Tests a simple, direct path."""
    cost, path = find_shortest_path_func(sample_graph, 'A', 'D')
    assert cost == 4
    assert path == ['A', 'B', 'C', 'D']

def test_no_path(find_shortest_path_func, sample_graph):
    """Tests a scenario where no path exists."""
    cost, path = find_shortest_path_func(sample_graph, 'A', 'F')
    # Assuming 'D' does not connect back to anything that can reach 'F'
    # based on the sample_graph, let's refine the graph to make this certain.
    graph = {
        'A': {'B': 1},
        'C': {'D': 1},
        'F': {} # F is unreachable
    }
    cost, path = find_shortest_path_func(graph, 'A', 'F')
    assert cost == float('inf')
    assert path == []

def test_start_equals_end(find_shortest_path_func, sample_graph):
    """Tests when the start and end nodes are the same."""
    cost, path = find_shortest_path_func(sample_graph, 'A', 'A')
    assert cost == 0
    assert path == ['A']

def test_more_complex_path(find_shortest_path_func):
    """Tests a graph with multiple path options."""
    graph = {
        'A': {'B': 10, 'C': 3},
        'B': {'C': 1, 'D': 2},
        'C': {'B': 4, 'D': 8, 'E': 2},
        'D': {'E': 7},
        'E': {'D': 9}
    }
    cost, path = find_shortest_path_func(graph, 'A', 'D')
    assert cost == 9
    assert path == ['A', 'C', 'B', 'D']

def test_path_with_isolated_node(find_shortest_path_func, sample_graph):
    """Tests a path to a node that has no outgoing edges."""
    cost, path = find_shortest_path_func(sample_graph, 'A', 'F')
    # Correcting the logic from the no_path test, using the full sample_graph
    cost, path = find_shortest_path_func(sample_graph, 'A', 'F')
    assert cost == 7
    assert path == ['A', 'B', 'C', 'D', 'E', 'F']

def test_disconnected_component(find_shortest_path_func):
    """Tests a graph where the start and end are in disconnected components."""
    graph = {
        'A': {'B': 1},
        'B': {},
        'C': {'D': 1},
        'D': {}
    }
    cost, path = find_shortest_path_func(graph, 'A', 'C')
    assert cost == float('inf')
    assert path == []

def test_negative_weights(find_shortest_path_func):
    """
    Tests a graph with negative weights. Dijkstra's is not expected to work
    correctly here, so this tests if an algorithm can handle it or fails gracefully.
    A correct implementation (like Bellman-Ford) would find the path.
    """
    graph = {
        'A': {'B': 1, 'C': 2},
        'B': {},
        'C': {'D': 1},
        'D': {'B': -3}
    }
    # Correct path to B is A->C->D->B with cost 2+1-3=0
    # Dijkstra will find A->B with cost 1
    cost, path = find_shortest_path_func(graph, 'A', 'B')
    assert cost == 0
    assert path == ['A', 'C', 'D', 'B']

def test_multiple_equal_paths(find_shortest_path_func):
    """Tests a graph with two paths of the same cost."""
    graph = {
        'A': {'B': 2, 'C': 2},
        'B': {'D': 3},
        'C': {'D': 3}
    }
    cost, path = find_shortest_path_func(graph, 'A', 'D')
    assert cost == 5
    # The algorithm should deterministically choose one. We accept either.
    assert path == ['A', 'B', 'D'] or path == ['A', 'C', 'D']