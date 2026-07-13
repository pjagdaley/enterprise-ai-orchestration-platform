#!/usr/bin/env bash

set -e

PLANTUML_JAR="tools/plantuml.jar"
DIAGRAM_ROOT="docs/diagrams"

echo "==============================================="
echo " Enterprise AI Orchestration Platform"
echo " PlantUML Diagram Generator"
echo "==============================================="
echo

# -------------------------------------------------
# Check Java
# -------------------------------------------------

if ! command -v java >/dev/null 2>&1; then
    echo "ERROR: Java is not installed."
    exit 1
fi

# -------------------------------------------------
# Check PlantUML
# -------------------------------------------------

if [ ! -f "$PLANTUML_JAR" ]; then
    echo "ERROR: $PLANTUML_JAR not found."
    exit 1
fi

# -------------------------------------------------
# Diagram folders
# -------------------------------------------------

FOLDERS=(
    executive
    c4
    ai
    data
    deployment
    domain
    network
    operations
    security
    sequence
    ui
)

TOTAL=0
FAILED=0

# -------------------------------------------------
# Generate SVGs
# -------------------------------------------------

for folder in "${FOLDERS[@]}"
do

    DIR="$DIAGRAM_ROOT/$folder"

    if [ ! -d "$DIR" ]; then
        continue
    fi

    echo
    echo "Generating diagrams from: $folder"

    while IFS= read -r file
    do
        echo "  -> $(basename "$file")"

        if java -jar "$PLANTUML_JAR" -tsvg "$file"
        then
            TOTAL=$((TOTAL+1))
        else
            echo "     FAILED"
            FAILED=$((FAILED+1))
        fi

    done < <(find "$DIR" -name "*.puml" | sort)

done

echo
echo "==============================================="
echo "Generation Complete"
echo "==============================================="
echo

echo "Generated : $TOTAL"

echo "Failed    : $FAILED"

echo