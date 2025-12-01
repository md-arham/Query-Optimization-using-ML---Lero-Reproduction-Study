import matplotlib.pyplot as plt
import os

# --- Configuration ---
# Using the STATS log files
PG_LOG = "/home/arhamf123/lero_project/stats_benchmark/pg_stats_results.log"
LERO_LOG = "/home/arhamf123/lero_project/stats_benchmark/lero_stats_results.log"
OUTPUT_IMAGE = "/home/arhamf123/lero_project/stats_benchmark/stats_top10_speedup.png"

def read_results(filename):
    data = {}
    if not os.path.exists(filename):
        print(f"Warning: {filename} not found!")
        return {}
    with open(filename, 'r') as f:
        for line in f:
            parts = line.strip().split(',')
            if len(parts) < 2: continue
            try:
                # Clean the name (e.g., "stats_q1.sql" -> "Q1")
                raw_name = parts[0].strip()
                # Extract number for cleaner labels if possible
                clean_name = raw_name.replace(".sql", "").replace("stats_q", "Q")
                
                latency = float(parts[1])
                if latency > 0: data[clean_name] = latency
            except ValueError: continue
    return data

def main():
    pg_data = read_results(PG_LOG)
    lero_data = read_results(LERO_LOG)
    
    speedups = []
    
    for q, pg_time in pg_data.items():
        if q in lero_data:
            lero_time = lero_data.get(q)
            # Calculate Speedup (Factor)
            # Avoid division by zero
            if lero_time < 0.1: lero_time = 0.1 
            
            factor = pg_time / lero_time
            speedups.append((q, factor))
    
    # Sort by speedup (highest first) and take top 10
    speedups.sort(key=lambda x: x[1], reverse=True)
    top_10 = speedups[:10]
    
    print("Top 10 STATS Improvements:")
    for q, factor in top_10:
        print(f"{q}: {factor:.2f}x faster")
        
    if not top_10:
        print("No matching queries found to plot!")
        return

    # Plotting
    queries = [x[0] for x in top_10]
    factors = [x[1] for x in top_10]
    
    plt.figure(figsize=(10, 6))
    bars = plt.bar(queries, factors, color='purple', alpha=0.7)
    
    plt.ylabel('Speedup Factor (PG Time / Lero Time)')
    plt.title('Top 10 Query Improvements (STATS Dataset)')
    plt.axhline(y=1, color='black', linestyle='--', linewidth=1) # Baseline
    
    # Add labels on top of bars
    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2, yval, f'{yval:.1f}x', ha='center', va='bottom')
        
    plt.tight_layout()
    plt.savefig(OUTPUT_IMAGE)
    print(f"Graph saved to {OUTPUT_IMAGE}")

if __name__ == "__main__":
    main()
