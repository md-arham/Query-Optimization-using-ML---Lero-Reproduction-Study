# Lero Reproduction Study: Learning-to-Rank Query Optimization

This repository contains the source code, scripts, and experimental logs for the reproduction study of the paper **"Lero: A Learning-to-Rank Query Optimizer"** (VLDB 2023). 

We successfully deployed Lero on **PostgreSQL 13.1** and verified its performance improvements against the native optimizer using the **IMDB (JOB)** and **STATS (Stack Exchange)** benchmarks.

## Repository Structure

- **`analysis/`**: Python scripts used to parse logs and generate the comparison graphs (Cumulative Time & Per-Query Speedup).
- **`generation/`**: Scripts for generating the synthetic 1,000-query dynamic workload and parsing the STATS benchmark queries.
- **`logs/`**: Raw execution logs containing latency data for both Lero and PostgreSQL.
- **`results/`**: Generated plots visualizing the performance differences.

## Environment Setup

The reproduction was conducted in a **WSL 2 (Ubuntu 20.04)** environment with the following specifications:
- **Database:** PostgreSQL 13.1 (Compiled from source)
- **Extension:** `pg_hint_plan` (Patched for Lero plan injection)
- **Hardware:** Intel i5-11300H (4 Cores), 16GB RAM

### Prerequisites
1. **PostgreSQL 13.1 Source:** `wget https://ftp.postgresql.org/pub/source/v13.1/postgresql-13.1.tar.bz2`
2. **Apply Patch:** Apply `0001-init-lero.patch` to the Postgres source before building.
3. **Build Flags:** `./configure --prefix=...` (Disable parallel workers in `postgresql.conf`).

## Key Results

### 1. IMDB Benchmark (Join Order Benchmark)
We reproduced the "Performance Curve Since Deployment" (Figure 6 of the original paper) using a synthetic stream of 1,000 queries.
- **Outcome:** Lero consistently accumulated less execution time than PostgreSQL.
- **Speedup:** Approx. **1.48x** faster on the standard 113-query workload.

### 2. STATS Benchmark (Stack Exchange)
We reproduced the "Per-Query Latency Improvement" (Figure 5 of the original paper).
- **Outcome:** Lero achieved massive speedups on "tail latency" queries.
- **Highlight:** A single complex query saw a **372-second (6-minute)** reduction in execution time.
- **Safety:** Observed **zero functional regressions** (worst case < 0.01s slowdown), validating Lero's robustness.

## Usage

### Reproducing the Graphs
To regenerate the plots from our log files:

