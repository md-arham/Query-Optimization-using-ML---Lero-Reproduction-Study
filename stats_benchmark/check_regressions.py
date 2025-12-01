import os

PG_LOG = "/home/arhamf123/lero_project/stats_benchmark/pg_stats_results.log"
LERO_LOG = "/home/arhamf123/lero_project/stats_benchmark/lero_stats_results.log"

def read_results(filename):
    data = {}
    with open(filename, 'r') as f:
        for line in f:
            parts = line.strip().split(',')
            if len(parts) < 2: continue
            try:
                name = parts[0].strip().replace(".sql", "")
                lat = float(parts[1])
                data[name] = lat
            except: continue
    return data

pg = read_results(PG_LOG)
lero = read_results(LERO_LOG)

regressions = []
improvements = []

for q in pg:
    if q in lero:
        diff = pg[q] - lero[q]
        # If diff is negative, Lero was SLOWER (Regression)
        if diff < 0:
            regressions.append((q, diff))
        else:
            improvements.append((q, diff))

print(f"Total Queries Compared: {len(regressions) + len(improvements)}")
print(f"Number of Improvements: {len(improvements)}")
print(f"Number of Regressions: {len(regressions)}")

if len(regressions) > 0:
    print("\nTop 5 Worst Regressions (ms):")
    regressions.sort(key=lambda x: x[1])
    for q, d in regressions[:5]:
        print(f"{q}: {d} ms")
