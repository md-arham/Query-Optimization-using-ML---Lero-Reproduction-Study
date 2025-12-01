#!/bin/bash

# 1. Define the correct tool paths (Crucial!)
PSQL="/home/arhamf123/lero_project/pgsql/bin/psql"
DB="stats"
HOST="localhost"

# 2. Define where the data is
BASE_DIR="/home/arhamf123/lero_project/stats_benchmark/End-to-End-CardEst-Benchmark-master/datasets/stats_simplified"

# 3. Run the SQL file to create tables
echo "Creating tables..."
$PSQL -h $HOST -d $DB -f "$BASE_DIR/stats.sql"

# 4. Load the CSV files
echo "Loading Badges..."
$PSQL -h $HOST -d $DB -c "\COPY badges FROM '$BASE_DIR/badges.csv' DELIMITER ',' CSV HEADER;"

echo "Loading Comments..."
$PSQL -h $HOST -d $DB -c "\COPY comments FROM '$BASE_DIR/comments.csv' DELIMITER ',' CSV HEADER;"

echo "Loading PostHistory..."
$PSQL -h $HOST -d $DB -c "\COPY postHistory FROM '$BASE_DIR/postHistory.csv' DELIMITER ',' CSV HEADER;"

echo "Loading PostLinks..."
$PSQL -h $HOST -d $DB -c "\COPY postLinks FROM '$BASE_DIR/postLinks.csv' DELIMITER ',' CSV HEADER;"

echo "Loading Posts..."
$PSQL -h $HOST -d $DB -c "\COPY posts FROM '$BASE_DIR/posts.csv' DELIMITER ',' CSV HEADER;"

echo "Loading Tags..."
$PSQL -h $HOST -d $DB -c "\COPY tags FROM '$BASE_DIR/tags.csv' DELIMITER ',' CSV HEADER;"

echo "Loading Users..."
$PSQL -h $HOST -d $DB -c "\COPY users FROM '$BASE_DIR/users.csv' DELIMITER ',' CSV HEADER;"

echo "Loading Votes..."
$PSQL -h $HOST -d $DB -c "\COPY votes FROM '$BASE_DIR/votes.csv' DELIMITER ',' CSV HEADER;"

# 5. Analyze (Important for optimization!)
echo "Analyzing database statistics..."
$PSQL -h $HOST -d $DB -c "ANALYZE;"

echo "SUCCESS! Stats dataset loaded."
