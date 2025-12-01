import matplotlib.pyplot as plt
import os

# --- Configuration ---
PG_LOG = "pg_results.log"
LERO_LOG = "lero_results.log"
OUTPUT_IMAGE = "lero_vs_pg_reproduction.png"

def read_results(filename):
    """Reads the log file and returns a dictionary {query_name: latency_ms}."""
    data = {}
    if not os.path.exists(filename):
        print(f"Warning: {filename} not found!")
        return {}
        
    with open(filename, 'r') as f:
        for line in f:
            line = line.strip()
            if not line: continue
            parts = line.split(',')
            if len(parts) < 2: continue
            
            name = parts[0].strip()
            # Filter out non-query files like schema.sql or fkindexes.sql
            if not name[0].isdigit(): 
                continue
                
            try:
                latency = float(parts[1])
                # If failed (-1), we can replace with a penalty or 0. 
                # For visual clarity, let's assume 0 but warn.
                if latency < 0:
                    latency = 0 
                data[name] = latency
            except ValueError:
                continue
    return data

def get_cumulative_data(data_dict, query_order):
    """Returns a list of cumulative times in Minutes."""
    cumulative_time = []
    current_total = 0
    
    for q in query_order:
        # Get latency in seconds (file is in ms)
        lat_ms = data_dict.get(q, 0)
        lat_sec = lat_ms / 1000.0
        
        current_total += lat_sec
        cumulative_time.append(current_total / 60.0) # Convert to Minutes
        
    return cumulative_time

def main():
    # 1. Read Data
    pg_data = read_results(PG_LOG)
    lero_data = read_results(LERO_LOG)
    
    # 2. Establish a common order of queries (sort alphabetically)
    # We use the intersection of queries found in both files to be fair
    all_queries = sorted(list(set(pg_data.keys()) | set(lero_data.keys())))
    
    print(f"Plotting {len(all_queries)} queries...")

    # 3. Calculate Cumulative Times
    pg_curve = get_cumulative_data(pg_data, all_queries)
    lero_curve = get_cumulative_data(lero_data, all_queries)
    
    # 4. Plot
    plt.figure(figsize=(10, 6))
    
    # X-axis is just 1, 2, 3... N
    x_axis = range(1, len(all_queries) + 1)
    
    plt.plot(x_axis, pg_curve, label='PostgreSQL (Baseline)', color='blue', linewidth=2)
    plt.plot(x_axis, lero_curve, label='Lero (Pre-trained)', color='green', linewidth=2, linestyle='--')
    
    plt.xlabel('Number of Queries Executed')
    plt.ylabel('Accumulated Execution Time (Minutes)')
    plt.title('Lero vs PostgreSQL: IMDB Benchmark Reproduction')
    plt.legend()
    plt.grid(True)
    
    # 5. Save
    plt.savefig(OUTPUT_IMAGE)
    print(f"Graph saved successfully to: {os.path.abspath(OUTPUT_IMAGE)}")

if __name__ == "__main__":
    main()
