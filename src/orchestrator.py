
import os
import sys
import json
import random
import platform
import datetime
from pathlib import Path
from jinja2 import Environment, FileSystemLoader

# Add the project root to the Python path to allow for absolute imports
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from src.agents.designer import DesignerAgent
from src.agents.implementer import ImplementerAgent
from src.agents.evaluator import EvaluatorAgent
from src.reporting import scoring, export_results, chart_generator

class Orchestrator:
    """Main orchestrator for the AutoAlgo system."""

    def __init__(self, problem_name: str):
        self.problem_name = problem_name
        self.project_root = Path(PROJECT_ROOT)
        self.problem_spec_path = self.project_root / "src" / "problems" / self.problem_name / "spec.md"
        self.test_file_path = self.project_root / "src" / "problems" / self.problem_name / "tests" / "test_shortest_path.py"
        
        # Agents
        self.designer = DesignerAgent()
        self.implementer = ImplementerAgent()

    def _collect_and_save_metadata(self, base_experiment_id: str, seed: int) -> dict:
        """Collects and saves metadata about the experiment run."""
        metadata = {
            "experiment_id": base_experiment_id,
            "timestamp_utc": datetime.datetime.utcnow().isoformat(),
            "python_version": platform.python_version(),
            "os": platform.system(),
            "rng_seed": seed,
            "problem_name": self.problem_name,
            "git_commit_hash": "N/A (tool unavailable)"
        }
        metadata_path = self.project_root / "experiments" / base_experiment_id / "metadata.json"
        os.makedirs(os.path.dirname(metadata_path), exist_ok=True)
        with open(metadata_path, 'w') as f:
            json.dump(metadata, f, indent=4)
        print(f"   - Metadata saved to {metadata_path}")
        return metadata

    def _read_problem_spec(self) -> str:
        """Reads the problem specification file."""
        with open(self.problem_spec_path, 'r', encoding='utf-8') as f:
            return f.read()

    def _generate_report(self, base_experiment_id: str, scored_candidates: list[dict], metadata: dict):
        """Generates a full report with JSON, CSV, charts, and HTML."""
        print("5. Generating final report...")
        report_dir = self.project_root / "reports" / base_experiment_id
        report_dir.mkdir(parents=True, exist_ok=True)

        # 1. Save raw + scored data
        json_path = report_dir / "results.json"
        csv_path = report_dir / "results.csv"
        report_data = {
            "experiment_id": base_experiment_id,
            "metadata": metadata,
            "candidates": scored_candidates,
            "winner": scored_candidates[0]["id"] if scored_candidates else None
        }
        export_results.save_json(report_data, json_path)
        export_results.candidates_to_csv(scored_candidates, csv_path)
        print(f"   - Saved JSON and CSV results to {report_dir}")

        # 2. Generate charts
        chart_generator.runtime_chart(scored_candidates, report_dir / "runtime_chart.png")
        chart_generator.memory_chart(scored_candidates, report_dir / "memory_chart.png")
        chart_generator.score_bar(scored_candidates, report_dir / "scores_chart.png")
        print(f"   - Saved charts to {report_dir}")

        # 3. Render HTML report
        env = Environment(loader=FileSystemLoader(self.project_root / "src" / "templates"))
        tpl = env.get_template("report_template.html")
        html = tpl.render(report_data)
        html_path = report_dir / "index.html"
        html_path.write_text(html, encoding="utf8")
        print(f"   - Saved final HTML report to {html_path}")

    def run_comparison_experiment(self, base_experiment_id: str, seed: int = None):
        """Runs a full comparison experiment across multiple candidates."""
        if seed is not None:
            random.seed(seed)
            print(f"--- Seeding RNG with {seed} for reproducibility ---")

        print(f"--- Starting Comparison Experiment {base_experiment_id} for Problem: {self.problem_name} ---")

        # 0. Collect and save metadata
        metadata = self._collect_and_save_metadata(base_experiment_id, seed)

        # 1. Read Problem Spec
        print("1. Reading problem specification...")
        problem_spec = self._read_problem_spec()

        # 2. Design Algorithm Variations
        print("2. Designing algorithm variations with DesignerAgent...")
        candidates = self.designer.propose_algorithms(problem_spec)
        print(f"   - {len(candidates)} candidates proposed.")

        candidates_data = []
        for i, candidate in enumerate(candidates):
            variation_id = candidate['variation_id']
            print(f"\n--- Evaluating Candidate {i+1}/{len(candidates)}: {variation_id} ---")

            # 3. Implement Algorithm & Save Artifacts
            solution_dir = self.project_root / "experiments" / base_experiment_id / variation_id
            solution_dir.mkdir(parents=True, exist_ok=True)
            
            (solution_dir / "prompt.txt").write_text(candidate['prompt'])
            (solution_dir / "llm_output.txt").write_text(candidate['code'])

            solution_file_path = solution_dir / "solution.py"
            solution_module_path = f"experiments.{base_experiment_id}.{variation_id}.solution"
            
            (self.project_root / "experiments" / base_experiment_id / "__init__.py").touch()
            (solution_dir / "__init__.py").touch()

            self.implementer.save_code(candidate['code'], str(solution_file_path))

            # 4. Evaluate Algorithm
            self._update_test_path(solution_module_path)
            evaluator = EvaluatorAgent(solution_module_path=solution_module_path, test_path=str(self.test_file_path))
            results = evaluator.evaluate()
            
            # Append data for scoring
            candidate_result = {
                "id": variation_id,
                "name": variation_id,
                **results
            }
            candidates_data.append(candidate_result)

            # Save logs
            (solution_dir / "run.log").write_text(results['pytest_output'])
            if results['correctness'] == 0.0:
                (solution_dir / "error.log").write_text(results['pytest_output'])

        # 5. Score candidates and generate final report
        scored_candidates = scoring.compute_scores(candidates_data)
        self._generate_report(base_experiment_id, scored_candidates, metadata)

        print(f"\n--- Comparison Experiment {base_experiment_id} Finished ---")

    def _update_test_path(self, solution_module_path: str):
        """Updates the test file to point to the correct solution module."""
        with open(self.test_file_path, 'r') as f:
            content = f.read()
        
        new_content = []
        for line in content.splitlines():
            if line.strip().startswith("SOLUTION_MODULE_PATH"):
                new_content.append(f"SOLUTION_MODULE_PATH = \"{solution_module_path}\"")
            else:
                new_content.append(line)
        
        with open(self.test_file_path, 'w') as f:
            f.write("\n".join(new_content))

if __name__ == "__main__":
    print("This is a class file. Please use run.py to execute an experiment.")

