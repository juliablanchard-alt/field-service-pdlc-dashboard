#!/bin/bash
# Manual on-demand dashboard refresh
# Run this anytime you want to push fresh data immediately (without waiting for cron)

echo "🔄 Manual PDLC Dashboard Refresh"
echo "================================"
echo ""

cd /Users/julia.blanchard/field-service-execution-dashboard || exit 1

# Run the auto-update script (which fetches, builds, commits, pushes)
./auto_update_dashboard.sh

echo ""
echo "✅ Manual refresh complete!"
echo "📊 View dashboard: https://julia-blanchard.github.io/field-service-pdlc-dashboard/"
