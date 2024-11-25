# Note: Portions of this code may have been generated with AI assistance.
#
# Show columns in a CSV file
#
#!/bin/bash

# Check if the input CSV file is provided
if [ "$#" -ne 1 ]; then
    echo "Usage: $0 input.csv"
    exit 1
fi

input_file="$1"

# Ensure the input file exists
if [ ! -f "$input_file" ]; then
    echo "Error: Input file '$input_file' not found!"
    exit 1
fi

# Extract the header row and display as a list of columns
echo "Columns in $input_file:"
head -n 1 "$input_file" | tr ',' '\n'
