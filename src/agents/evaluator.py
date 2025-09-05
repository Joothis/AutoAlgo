"""
Evaluator agent.
"""
import timeit
import tracemalloc
from importlib import import_module
import os

from src.utils import run_shell_command
from src.problems.shortest_path.input_generators import generate_shortest_path_inputs

class EvaluatorAgent:
    """
    The Evaluator agent runs correctness tests and performance benchmarks.
    """

    def __init__(self, solution_module_path: str, test_path: str):
        """
        Args:
            solution_module_path: The import path for the solution to be tested.
            test_path: The file path to the pytest test suite.
        """
        self.solution_module_path = solution_module_path
        self.test_path = test_path
        self.solution_func = None

    def _load_solution(self):
        """Dynamically loads the solution function."""
        if self.solution_func:
            return
        try:
            module = import_module(self.solution_module_path)
            self.solution_func = module.find_shortest_path
        except (ImportError, AttributeError) as e:
            raise RuntimeError(f"Could not load solution function from {self.solution_module_path}") from e

    def run_correctness_tests(self) -> dict:
        """Runs the pytest suite for correctness checking."""
        print("   - Running correctness tests with a 60-second timeout...")
        command = f"py -m pytest {self.test_path}"
        result = run_shell_command(command, timeout=60)
        
        # Check for timeout or other errors
        if result["returncode"] != 0:
            passed = False
        else:
            # A bit simplistic: we assume any failed test means 0% pass rate for the MVP
            passed = "failed" not in result['stdout'] and "error" not in result['stdout']
        
        return {"passed": passed, "details": result['stdout'] + "\n" + result['stderr']}

    def run_performance_benchmarks(self, num_runs=5) -> dict:
        """Runs runtime and memory benchmarks."""
        self._load_solution()
        print("   - Running performance benchmarks...")
        
        runtime_results = {}
        memory_results = {}
        test_scales = {"10": 10, "50": 50, "100": 100} # Use size as string key

        for scale_key, num_nodes in test_scales.items():
            # Runtime benchmark
            total_time = timeit.timeit(
                lambda: self.solution_func(*generate_shortest_path_inputs(num_nodes, 0.5)),
                number=num_runs
            )
            avg_time = total_time / num_runs
            runtime_results[scale_key] = avg_time * 1000 # ms

            # Memory benchmark
            tracemalloc.start()
            self.solution_func(*generate_shortest_path_inputs(num_nodes, 0.5))
            current, peak = tracemalloc.get_traced_memory()
            tracemalloc.stop()
            memory_results[scale_key] = peak / 1024 # KB

            print(f"     - Size {num_nodes}: {runtime_results[scale_key]:.2f}ms, {memory_results[scale_key]:.2f}KB peak memory")

        return {"runtime_ms": runtime_results, "mem_kb": memory_results}

    def evaluate(self) -> dict:
        """Runs a full evaluation and returns a dictionary of raw results."""
        print("4. Evaluating solution with EvaluatorAgent...")
        correctness_results = self.run_correctness_tests()
        
        correctness_score = 1.0 if correctness_results["passed"] else 0.0
        
        if correctness_score == 0.0:
            print("   - Correctness tests failed. Skipping performance benchmarks.")
            return {
                "correctness": correctness_score,
                "pytest_output": correctness_results['details'],
                "runtime_ms": {},
                "mem_kb": {}
            }
        
        performance_results = self.run_performance_benchmarks()

        return {
            "correctness": correctness_score,
            "pytest_output": correctness_results['details'],
            "runtime_ms": performance_results["runtime_ms"],
            "mem_kb": performance_results["mem_kb"]
        }

