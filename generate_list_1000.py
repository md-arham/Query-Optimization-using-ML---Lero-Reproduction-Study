import random
import os

# Path to your formatted 113 queries
INPUT_FILE = "/home/arhamf123/lero_project/job_queries_formatted.txt"
OUTPUT_FILE = "/home/arhamf123/lero_project/job_1000_sampled.txt"

# Read the 113 queries
with open(INPUT_FILE, 'r') as f:
    lines = [l.strip() for l in f if l.strip()]

# Sample 1000 times with replacement
random.seed(42) # Fixed seed for reproducibility
sampled_lines = random.choices(lines, k=1000)

# Write to new file
with open(OUTPUT_FILE, 'w') as f:
    for line in sampled_lines:
        f.write(line + "\n")

print(f"Generated {len(sampled_lines)} queries in {OUTPUT_FILE}")

