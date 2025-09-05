
import sys
import os

# Add the project root to the Python path
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from src.orchestrator import Orchestrator

def main():
    """Main entry point to run an AutoAlgo experiment."""
    
    # Set a seed for reproducibility
    SEED = 42

    problem_name = "shortest_path"
    base_experiment_id = "comparison_001"
    
    orchestrator = Orchestrator(problem_name=problem_name)
    orchestrator.run_comparison_experiment(base_experiment_id=base_experiment_id, seed=SEED)

if __name__ == "__main__":
    main()
