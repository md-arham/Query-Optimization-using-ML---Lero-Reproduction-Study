import os

# Input file (The big SQL file with all queries)
INPUT_SQL = "/home/arhamf123/lero_project/stats_benchmark/End-to-End-CardEst-Benchmark-master/workloads/stats_CEB/stats_CEB.sql"
OUTPUT_DIR = "/home/arhamf123/lero_project/stats_benchmark/queries"
LIST_FILE = "/home/arhamf123/lero_project/stats_benchmark/stats_query_list.txt"

if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

print("Reading queries...")
with open(INPUT_SQL, 'r') as f:
    content = f.read()

# Split by semicolon (standard SQL delimiter)
queries = content.split(';')

valid_queries = []
for i, q in enumerate(queries):
    q = q.strip()
    if len(q) < 10: continue # Skip empty lines
    # --- NEW FIX: Remove the "Answer||" prefix ---
    if "||" in q:
        # Split by || and take the second part (the actual SQL)
        q = q.split("||")[1].strip()
        # ---------------------------------------------
    # Save individual file
    filename = f"stats_q{i+1}.sql"
    filepath = os.path.join(OUTPUT_DIR, filename)
    with open(filepath, 'w') as out:
        out.write(q + ";")
        
    valid_queries.append(f"{filename},{filepath}")

# Save the list file for Lero
with open(LIST_FILE, 'w') as f:
    for line in valid_queries:
        f.write(line + "\n")
        
print(f"Split {len(valid_queries)} queries into {OUTPUT_DIR}")
print(f"List saved to {LIST_FILE}")
