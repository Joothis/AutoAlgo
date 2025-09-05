# scoring.py
from __future__ import annotations
from typing import List, Dict, Any
import math

def avg_runtime_ms(runtime_dict: Dict[str, float]) -> float:
    # runtime_dict: {"10":0.03, "50":0.53, "100":2.44}
    vals = list(runtime_dict.values())
    return sum(vals) / len(vals) if vals else float("inf")

def avg_mem_kb(mem_dict: Dict[str, float]) -> float:
    vals = list(mem_dict.values())
    return sum(vals) / len(vals) if vals else float("inf")

def normalize_list(values: List[float], higher_is_better: bool = True) -> List[float]:
    if not values:
        return []

    finite_vals = [v for v in values if v != float('inf') and not math.isnan(v)]
    if not finite_vals:
        return [1.0] * len(values) # All are inf or nan

    mn, mx = min(finite_vals), max(finite_vals)

    results = []
    for v in values:
        if v == float('inf'):
            # For lower-is-better, inf is worst (0.0). For higher-is-better, it's also worst (0.0).
            results.append(0.0)
        elif math.isnan(v):
            results.append(0.0)
        elif math.isclose(mx, mn):
            results.append(1.0)
        else:
            if higher_is_better:
                results.append((v - mn) / (mx - mn))
            else:
                results.append((mx - v) / (mx - mn))
    return results

def compute_scores(candidates: List[Dict[str, Any]], weights=None) -> List[Dict[str, Any]]:
    """
    candidates: list of dicts with keys:
      - id, name
      - correctness: float (0.0-1.0)
      - runtime_ms: dict of runtimes by size
      - mem_kb: dict of memory by size
    Returns: same list with added keys: avg_runtime_ms, avg_mem_kb, norm_* and final_score
    """
    if weights is None:
        weights = {"correctness": 0.6, "runtime": 0.3, "memory": 0.1}

    # compute averages
    for c in candidates:
        c["avg_runtime_ms"] = avg_runtime_ms(c.get("runtime_ms", {}))
        c["avg_mem_kb"] = avg_mem_kb(c.get("mem_kb", {}))
        # safety defaults
        c["correctness"] = float(c.get("correctness", 0.0))

    # build lists
    correctness_list = [c["correctness"] for c in candidates]
    runtime_list = [c["avg_runtime_ms"] for c in candidates]
    mem_list = [c["avg_mem_kb"] for c in candidates]

    # normalize
    n_corr = normalize_list(correctness_list, higher_is_better=True)
    n_time = normalize_list(runtime_list, higher_is_better=False)
    n_mem  = normalize_list(mem_list, higher_is_better=False)

    # compute weighted score
    for i, c in enumerate(candidates):
        c["norm_correctness"] = round(n_corr[i], 4)
        c["norm_runtime"] = round(n_time[i], 4)
        c["norm_memory"] = round(n_mem[i], 4)
        score = (weights["correctness"] * n_corr[i] +
                 weights["runtime"]     * n_time[i] +
                 weights["memory"]      * n_mem[i])
        c["final_score"] = round(score, 4)

    # sort candidates by score descending for convenience
    candidates.sort(key=lambda x: x["final_score"], reverse=True)
    return candidates

if __name__ == "__main__":
    # tiny local test
    sample = [
        {"id":"a","name":"A","correctness":1.0,"runtime_ms":{"10":0.03,"50":0.5,"100":2.4},"mem_kb":{"10":3.7,"50":60,"100":228}},
        {"id":"b","name":"B","correctness":1.0,"runtime_ms":{"10":0.04,"50":0.66,"100":2.53},"mem_kb":{"10":3.6,"50":58,"100":231}},
        {"id":"c","name":"C","correctness":0.0,"runtime_ms":{},"mem_kb":{}},
    ]
    import json
    out = compute_scores(sample)
    print(json.dumps(out, indent=2))