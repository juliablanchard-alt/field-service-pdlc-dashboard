#!/bin/bash
# Daily Phase 0 Data Sync - Runs at 6 AM PT
# Fetches data from Google Sheets and updates dashboard

cd "$(dirname "$0")"

SHEET_ID="1y5FS7MxqUT019bVRJuPOIH2H5Tc-8q9gH_6vXq4CMgk"
GID="1674131463"
EXPORT_URL="https://docs.google.com/spreadsheets/d/${SHEET_ID}/export?format=csv&gid=${GID}"

echo "=================================================="
echo "Phase 0 Daily Sync - $(date)"
echo "=================================================="

# Fetch CSV data from Google Sheets
echo "Fetching data from Google Sheets..."
CSV_DATA=$(curl -sL "$EXPORT_URL")

if [ -z "$CSV_DATA" ]; then
    echo "❌ Failed to fetch data from Google Sheets"
    exit 1
fi

echo "✅ Data fetched successfully"

# Run sync script
echo "Processing and saving data..."
echo "$CSV_DATA" | python3 sync_phase0_data.py

if [ $? -eq 0 ]; then
    echo "✅ Phase 0 data synced successfully!"
    echo "=================================================="
else
    echo "❌ Failed to sync Phase 0 data"
    echo "=================================================="
    exit 1
fi
