#!/bin/bash

set -eu
# Define the folder path to check
# Replace with the actual folder path

FOLDER_PATH="$1" 
echo "Checking for changed files in: $FOLDER_PATH"

# Call the Python script with --output-format bash
# The output will be a list of changed/new files, one per line
SCRIPT_DIR=$(cd `dirname $0`; pwd)
CHANGED_FILES=$(python $SCRIPT_DIR/../zip_hasher.py "$FOLDER_PATH" --output-format bash)

if [ -z "$CHANGED_FILES" ]; then
    echo "No changed or new files detected."
else
    echo "Changed or new files:"
    echo "$CHANGED_FILES"
    
    # You can loop through the files
    echo "Processing each file:"
    while IFS= read -r file; do
        echo "  - $file"
        # Add your custom logic here for each changed/new file
        # For example, copy them, log them, etc.
    done <<< "$CHANGED_FILES"
fi
