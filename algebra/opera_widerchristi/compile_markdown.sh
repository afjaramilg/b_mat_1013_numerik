#!/bin/bash

INPUT_DIR="output_final"
OUTPUT_FILE="irreducible_summary.md"

# Clear the output file if it already exists, or create it if it doesn't
> "$OUTPUT_FILE"

echo "Scanning for *_irr files in '$INPUT_DIR'..."
echo "Compiling into '$OUTPUT_FILE'..."
echo "--------------------------------------------------------"

# Enable nullglob so the loop doesn't fail if no *_irr files are found
shopt -s nullglob
files=("$INPUT_DIR"/*_irr.txt)

if [ ${#files[@]} -eq 0 ]; then
    echo "No files ending in '_irr' found in '$INPUT_DIR'."
    exit 0
fi

count=0

for file in "${files[@]}"; do
    # 1. Extract just the filename without the full folder path
    filename=$(basename "$file")
    
    # 2. Write the filename as a Markdown heading (##)
    echo "###$filename" >> "$OUTPUT_FILE"
    
    # 3. Open the block with three backticks
    echo "\`" >> "$OUTPUT_FILE"
    
    # 4. Join all lines with ", " and write them inside the block.
    # We use awk here because it safely handles joining strings without leaving a trailing comma.
    awk 'NR==1{printf "%s", $0; next} {printf ", %s", $0} END{print ""}' "$file" >> "$OUTPUT_FILE"
    
    # 5. Close the block and add a blank line for spacing
    echo "\`" >> "$OUTPUT_FILE"
    echo "" >> "$OUTPUT_FILE"
    
    echo "Added: $filename"
    ((count++))
done

echo "--------------------------------------------------------"
echo "Done! Successfully compiled $count files into '$OUTPUT_FILE'."
