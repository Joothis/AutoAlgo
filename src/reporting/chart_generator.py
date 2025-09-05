# chart_generator.py
from pathlib import Path
import json
import matplotlib.pyplot as plt
import pandas as pd

def load_json(path:Path):
    return json.loads(path.read_text(encoding="utf8"))

def runtime_chart(candidates, out_png:Path):
    # candidates: list with runtime_ms dicts
    # build DataFrame where rows are sizes, cols are candidate ids
    dfs = {}
    for c in candidates:
        runtimes = c.get("runtime_ms", {})
        if runtimes:
            s = pd.Series(runtimes, name=c["id"])
            dfs[c["id"]] = s.astype(float)
    if not dfs:
        return
    df = pd.concat(dfs.values(), axis=1)
    df = df.sort_index(key=lambda x: x.astype(int))
    plt.figure()
    for col in df.columns:
        plt.plot(df.index.astype(int), df[col], marker='o', label=col)
    plt.xlabel("Input size (n)")
    plt.ylabel("Runtime (ms)")
    plt.title("Runtime vs Input Size")
    plt.legend()
    out_png.parent.mkdir(parents=True, exist_ok=True)
    plt.tight_layout()
    plt.savefig(out_png)
    plt.close()

def memory_chart(candidates, out_png:Path):
    dfs = {}
    for c in candidates:
        mem = c.get("mem_kb", {})
        if mem:
            s = pd.Series(mem, name=c["id"])
            dfs[c["id"]] = s.astype(float)
    if not dfs:
        return
    df = pd.concat(dfs.values(), axis=1)
    df = df.sort_index(key=lambda x: x.astype(int))
    plt.figure()
    for col in df.columns:
        plt.plot(df.index.astype(int), df[col], marker='o', label=col)
    plt.xlabel("Input size (n)")
    plt.ylabel("Peak memory (KB)")
    plt.title("Memory vs Input Size")
    plt.legend()
    out_png.parent.mkdir(parents=True, exist_ok=True)
    plt.tight_layout()
    plt.savefig(out_png)
    plt.close()

def score_bar(candidates, out_png:Path):
    ids = [c["id"] for c in candidates]
    scores = [c["final_score"] for c in candidates]
    plt.figure()
    plt.bar(ids, scores)
    plt.xlabel("Candidate")
    plt.ylabel("Final score")
    plt.title("Final scores (normalized)")
    out_png.parent.mkdir(parents=True, exist_ok=True)
    plt.tight_layout()
    plt.savefig(out_png)
    plt.close()

if __name__ == "__main__":
    data = load_json(Path("reports/comparison_demo.json"))
    candidates = data.get("candidates", [])
    runtime_chart(candidates, Path("reports/runtime_vs_size.png"))
    memory_chart(candidates, Path("reports/memory_vs_size.png"))
    score_bar(candidates, Path("reports/final_scores.png"))
    print("Charts written to reports/*.png")