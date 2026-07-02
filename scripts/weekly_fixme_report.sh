#!/bin/bash
# Weekly FIXME progress report generator

cd "$(dirname "$0")/.." || exit 1

echo "📊 Generating weekly FIXME progress report..."

# Generate progress report
python3 fixme_resolution_tracker.py --report

# Create date-stamped report
date_stamp=$(date +%Y-%m-%d)
cp FIXME_RESOLUTION_PROGRESS_REPORT.md "reports/weekly_report_$date_stamp.md"

# Generate easy wins summary
echo "🚀 Easy wins available:" >> "reports/weekly_report_$date_stamp.md"
python3 fixme_resolution_tracker.py --easy-wins >> "reports/weekly_report_$date_stamp.md"

echo "✅ Weekly report generated: reports/weekly_report_$date_stamp.md"
