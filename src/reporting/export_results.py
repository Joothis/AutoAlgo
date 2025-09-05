# export_results.py
import json
import csv
from pathlib import Path
from typing import Dict, Any, List

def save_json(data: Dict[str,Any], path:Path):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2), encoding="utf8")

def candidates_to_csv(candidates: List[Dict], csv_path: Path):
    csv_path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = [
        "id","name","correctness","avg_runtime_ms","avg_mem_kb",
        "norm_correctness","norm_runtime","norm_memory","final_score"
    ]
    with open(csv_path, "w", newline='', encoding="utf8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for c in candidates:
            row = {k: c.get(k, "") for k in fieldnames}
            writer.writerow(row)

if __name__ == "__main__":
    # usage example:
    from scoring import compute_scores
    candidates = [
        {"id":"a","name":"A","correctness":1.0,"runtime_ms":{"10":0.03,"50":0.5,"100":2.4},"mem_kb":{"10":3.7,"50":60,"100":228}},
        {"id":"b","name":"B","correctness":1.0,"runtime_ms":{"10":0.04,"50":0.66,"100":2.53},"mem_kb":{"10":3.6,"50":58,"100":231}},
    ]
    scored = compute_scores(candidates)
    save_json({"candidates":scored}, Path("reports/comparison_demo.json"))
    candidates_to_csv(scored, Path("reports/comparison_demo.csv"))
    print("Saved demo JSON+CSV to reports/")