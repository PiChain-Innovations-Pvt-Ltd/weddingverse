#!/bin/bash

# Loop through the numbers 1 to 112
for i in {1..30}; do
    # Run each command in the background
    python scrape_photographers.py $i &
done

# Wait for all background processes to finish
wait

echo "All scraping tasks completed."

