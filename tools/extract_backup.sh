#!/bin/bash
# Extract Android backup without ABE

if [ -z "$1" ]; then
    echo "Usage: $0 <backup.ab>"
    exit 1
fi

BACKUP_FILE="$1"
OUTPUT_DIR="backup_extracted"

# Skip the 24-byte header and decompress
dd if="$BACKUP_FILE" bs=24 skip=1 | openssl zlib -d > backup.tar 2>/dev/null

# Extract tar
mkdir -p "$OUTPUT_DIR"
tar -xvf backup.tar -C "$OUTPUT_DIR"

echo ""
echo "Extracted to: $OUTPUT_DIR"
echo "SharedPreferences location: $OUTPUT_DIR/apps/com.example.perseus/sp/"
