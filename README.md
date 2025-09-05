# AutoAlgo: An Autonomous Generative Agent for Algorithm Design & Evaluation

An open-source multi-agent system that autonomously generates, tests, and evaluates algorithm designs for a given problem (e.g., pathfinding, scheduling, sorting variants), ranking candidates by correctness, complexity, and empirical performance.

---

## Motivation

This project demonstrates a complete pipeline for modern AI-driven software engineering. It combines several key skills:

- **LLM-based Planning & Code Synthesis:** Using large language models to generate multiple functional algorithm candidates from a high-level specification.
- **Automated Testing & Benchmarking:** A rigorous evaluation harness that tests for correctness against multiple edge cases and benchmarks empirical performance (runtime, memory usage).
- **Multi-Agent Architecture:** A modular system of specialized agents (`Designer`, `Implementer`, `Evaluator`) coordinated by an `Orchestrator`.
- **Reproducible Research:** The entire experiment pipeline is versioned, seeded, and logged, producing detailed reports and artifacts for analysis.

The results are measurable and easy to present, making this a strong portfolio piece.

## Quick Start

1.  **Install Dependencies:**
    ```bash
    # Ensure you are using a compatible version of Python (e.g., 3.10+)
    py -m pip install -r requirements.txt
    ```

2.  **Run the Experiment:**
    ```bash
    py run.py
    ```

    This will execute the default comparison experiment for the `shortest_path` problem. The console will show the progress as it evaluates each candidate.

3.  **View the Results:**
    After the run completes, you can find the results in the `reports/` directory. Open `reports/comparison_001.html` in a web browser to see the final ranked comparison of the algorithm candidates.

## Architecture & Components

The system is composed of several agents and modules working in concert:

-   **`run.py`**: The main entry point to start an experiment.
-   **`src/orchestrator.py`**: The `Orchestrator` class manages the entire experiment workflow. It coordinates the agents, runs the evaluation loop, ranks the candidates, and generates the final report.
-   **`src/agents/`**: Contains the specialized agents:
    -   `designer.py`: Proposes one or more algorithm implementations based on a problem specification. (Currently simulated, but designed to be plugged into an LLM).
    -   `implementer.py`: Saves the proposed code to a runnable file.
    -   `evaluator.py`: The core of the testing pipeline. It runs correctness tests (`pytest`) and performance benchmarks (`timeit`, `tracemalloc`) against a candidate solution.
-   **`src/problems/`**: Contains the definitions for different algorithmic problems. Each problem has its own directory containing:
    -   `spec.md`: A detailed, human-readable specification of the problem.
    -   `tests/`: A directory with a `pytest` suite defining the correctness criteria.
    -   `input_generators.py`: A script to generate random inputs of varying sizes for benchmarking.
-   **`experiments/`**: This directory stores all the artifacts for each experiment run, including generated code, logs, and metadata, ensuring full reproducibility.
-   **`reports/`**: This directory contains the final high-level reports (in JSON and HTML format) summarizing the results of an experiment.

## How to Add a New Problem

The system is designed to be easily extensible.

1.  Create a new directory under `src/problems/`, e.g., `src/problems/sorting`.
2.  Inside, create a `spec.md` file describing the sorting problem.
3.  Create a `tests/test_sorting.py` file with a `pytest` suite for sorting algorithms.
4.  Create an `input_generators.py` that can generate lists of numbers to be sorted.
5.  Update `run.py` to point the `Orchestrator` to your new `sorting` problem.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
