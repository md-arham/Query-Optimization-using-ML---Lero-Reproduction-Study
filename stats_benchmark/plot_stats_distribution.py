import matplotlib.pyplot as plt
import os
import numpy as np

# --- Configuration ---
PG_LOG = "/home/arhamf123/lero_project/stats_benchmark/pg_stats_results.log"
LERO_LOG = "/home/arhamf123/lero_project/stats_benchmark/lero_stats_results.log"
OUTPUT_IMAGE = "/home/arhamf123/lero_project/stats_benchmark/stats_distribution_fig5.png"

def read_results(filename):
    data = {}
    if not os.path.exists(filename): return {}
    with open(filename, 'r') as f:
        for line in f:
            parts = line.strip().split(',')
            if len(parts) < 2: continue
            try:
                name = parts[0].strip().replace(".sql", "").replace("stats_q", "")
                latency = float(parts[1])
                if latency > 0: data[name] = latency
            except ValueError: continue
    return data

def main():
    pg_data = read_results(PG_LOG)
    lero_data = read_results(LERO_LOG)
    
    diffs = []
    
    for q, pg_time in pg_data.items():
        if q in lero_data:
            lero_time = lero_data[q]
            # Calculate difference in SECONDS
            diff = (pg_time - lero_time) / 1000.0
            diffs.append((q, diff))
    
    # Sort: Regressions (Negative) -> Improvements (Positive)
    diffs.sort(key=lambda x: x[1])
    
    print(f"Min Diff (Worst Regression): {diffs[0][1]:.4f} s")
    print(f"Max Diff (Best Improvement): {diffs[-1][1]:.4f} s")
    
    queries = [x[0] for x in diffs]
    values = [x[1] for x in diffs]
    x_pos = np.arange(len(queries))
    
    colors = ['red' if v < 0 else 'green' for v in values]

    plt.figure(figsize=(12, 6))
    plt.bar(x_pos, values, color=colors, width=1.0)
    
    plt.xlabel('Queries (Sorted by Improvement)')
    plt.ylabel('Time Difference (PG - Lero) in Seconds')
    plt.title('Per-Query Performance Distribution (Replicating Figure 5)')
    plt.axhline(0, color='black', linewidth=1)
    plt.xticks([]) 
    plt.grid(True, axis='y', linestyle='--', alpha=0.7)
    
    # Force Y-axis to show the negative part if it's small
    # Getting the current limits
    ymin, ymax = plt.ylim()
    # If ymin is barely negative (like -0.001) but we have -1.2, matplotlib handles it.
    # But if improvements are +100s and regression is -1s, it might look invisible.
    # Let's not force it, usually matplotlib is good.
    
    plt.tight_layout()
    plt.savefig(OUTPUT_IMAGE)
    print(f"Graph saved to {OUTPUT_IMAGE}")

if __name__ == "__main__":
    main()
