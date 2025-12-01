import matplotlib.pyplot as plt
import os

# --- Configuration ---
PG_LOG = "/home/arhamf123/lero_project/stats_benchmark/pg_stats_results.log"
LERO_LOG = "/home/arhamf123/lero_project/stats_benchmark/lero_stats_results.log"
OUTPUT_IMAGE = "/home/arhamf123/lero_project/stats_benchmark/stats_comparison.png"

def read_results(filename):
    """Reads log file and returns list of latencies in ms."""
    data = []
    if not os.path.exists(filename):
        print(f"Warning: {filename} not found!")
        return []
    with open(filename, 'r') as f:
        for line in f:
            parts = line.strip().split(',')
            if len(parts) < 2: continue
            try:
                lat = float(parts[1])
                if lat > 0: data.append(lat)
            except ValueError: continue
    return data

def get_cumulative(latencies):
    cum = []
    curr = 0
    for lat in latencies:
        curr += lat / 1000.0 # Convert to seconds
        cum.append(curr)
    return cum

def main():
    pg_data = read_results(PG_LOG)
    lero_data = read_results(LERO_LOG)
    
    print(f"PG Queries: {len(pg_data)}")
    print(f"Lero Queries: {len(lero_data)}")
    
    min_len = min(len(pg_data), len(lero_data))
    pg_cum = get_cumulative(pg_data[:min_len])
    lero_cum = get_cumulative(lero_data[:min_len])
    
    # Plot
    plt.figure(figsize=(10, 6))
    x = range(1, min_len + 1)
    
    plt.plot(x, pg_cum, label='PostgreSQL (Baseline)', color='blue', linewidth=2)
    plt.plot(x, lero_cum, label='Lero (Optimized)', color='green', linewidth=2, linestyle='--')
    
    plt.xlabel('Queries Executed')
    plt.ylabel('Total Execution Time (Seconds)')
    plt.title('STATS Benchmark: Lero vs PostgreSQL')
    plt.legend()
    plt.grid(True)
    
    plt.savefig(OUTPUT_IMAGE)
    print(f"Graph saved to {OUTPUT_IMAGE}")

    # Calculate Total Speedup
    total_pg = pg_cum[-1]
    total_lero = lero_cum[-1]
    print(f"Total PG Time: {total_pg:.2f}s")
    print(f"Total Lero Time: {total_lero:.2f}s")
    print(f"Overall Speedup: {total_pg/total_lero:.2f}x")

if __name__ == "__main__":
    main()
