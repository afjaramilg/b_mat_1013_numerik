#!/bin/bash

# Check if a folder path was provided
if [ -z "$1" ]; then
    echo "Error: Please provide a relative path to a folder."
    echo "Usage: ./filter_files.sh <relative_folder_path>"
    exit 1
fi

TARGET_DIR="$1"
DEST_DIR="output_final"

# Check if the provided path is actually a valid directory
if [ ! -d "$TARGET_DIR" ]; then
    echo "Error: Directory '$TARGET_DIR' does not exist."
    exit 1
fi

# Create the destination folder
mkdir -p "$DEST_DIR"

echo "Scanning files in '$TARGET_DIR'..."
echo "Copying files with 1 to 29 lines to '$DEST_DIR'..."
echo "--------------------------------------------------------"

count=0

# Loop through all items in the target directory
for file in "$TARGET_DIR"/*; do
    if [ -f "$file" ]; then
        
        # Count the lines in the file
        lines=$(wc -l < "$file")
        
        # NEW: If the file has MORE than 0 lines AND FEWER than 30 lines, copy it
        if [ "$lines" -gt 0 ] && [ "$lines" -lt 30 ]; then
            cp "$file" "$DEST_DIR/"
            echo "Copied: $(basename "$file") ($lines lines)"
            ((count++))
        fi
    fi
done

echo "--------------------------------------------------------"
echo "Done! Successfully copied $count files to '$DEST_DIR'."













































