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
                # Extract "Q1" from "stats_q1.sql"
                name = parts[0].strip().replace(".sql", "").replace("stats_q", "")
                latency = float(parts[1])
                if latency > 0: data[name] = latency
            except ValueError: continue
    return data

def main():
    pg_data = read_results(PG_LOG)
    lero_data = read_results(LERO_LOG)
    
    diffs = []
    
    # Calculate difference: (PG_Time - Lero_Time)
    # Positive means Lero is FASTER (Good)
    # Negative means Lero is SLOWER (Regression)
    
    for q, pg_time in pg_data.items():
        if q in lero_data:
            lero_time = lero_data[q]
            # Calculate difference in seconds
            diff = (pg_time - lero_time) / 1000.0
            diffs.append((q, diff))
    
    # Sort from smallest (worst regression) to largest (best speedup)
    diffs.sort(key=lambda x: x[1])
    
    # Extract data for plotting
    queries = [x[0] for x in diffs]
    values = [x[1] for x in diffs]
    x_pos = np.arange(len(queries))
    
    # Colors: Red for Regression (<0), Green for Improvement (>0)
    colors = ['red' if v < 0 else 'green' for v in values]

    # Plot
    plt.figure(figsize=(12, 6))
    plt.bar(x_pos, values, color=colors, width=1.0)
    
    plt.xlabel('Queries (Sorted by Improvement)')
    plt.ylabel('Time Difference (PG - Lero) in Seconds')
    plt.title('Per-Query Performance Distribution (Replicating Figure 5)')
    
    # Add a zero line
    plt.axhline(0, color='black', linewidth=1)
    
    # Clean up X-axis (too many labels, so just hide them or show sparsely)
    plt.xticks([]) 
    
    plt.grid(True, axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    
    plt.savefig(OUTPUT_IMAGE)
    print(f"Graph saved to {OUTPUT_IMAGE}")

if __name__ == "__main__":
    main()
