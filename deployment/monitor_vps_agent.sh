#!/bin/bash
# Monitor the Autonomous Lead Agent running on Hostinger VPS

VPS_HOST="31.97.145.136"
VPS_USER="root"
VPS_PASS="Kidessa231.@#"

echo "========================================================================"
echo "📊 AUTONOMOUS LEAD AGENT - LIVE MONITORING"
echo "========================================================================"
echo ""

# Check if process is running
echo "🔍 Checking process status..."
PROCESS_COUNT=$(sshpass -p "$VPS_PASS" ssh -o StrictHostKeyChecking=no $VPS_USER@$VPS_HOST \
  'ps aux | grep autonomous_lead_agent.py | grep -v grep | wc -l')

if [ "$PROCESS_COUNT" -gt 0 ]; then
    echo "✅ Agent is RUNNING"
else
    echo "❌ Agent is NOT running"
    exit 1
fi

echo ""

# Get latest stats from logs
echo "📈 Latest Import Progress:"
echo "========================================================================"
sshpass -p "$VPS_PASS" ssh -o StrictHostKeyChecking=no $VPS_USER@$VPS_HOST << 'ENDSSH'
# Get the most recent log file
LOG_FILE=$(ls -t /root/lead_agent/logs/*.log 2>/dev/null | head -1)

if [ -f "$LOG_FILE" ]; then
    # Extract progress
    LAST_IMPORT=$(grep -o "\[[0-9]*/2000\]" "$LOG_FILE" | tail -1)
    LAST_NAME=$(grep "INFO - \[[0-9]*/2000\]" "$LOG_FILE" | tail -1 | sed 's/.*INFO - //')
    
    echo "Current Progress: $LAST_IMPORT"
    echo "Latest Import: $LAST_NAME"
    echo ""
    
    # Count successes
    IMPORTED=$(grep -c "✓ Imported to Instantly" "$LOG_FILE")
    FAILED=$(grep -c "✗" "$LOG_FILE")
    
    echo "✓ Successfully Imported: $IMPORTED"
    echo "✗ Failed/Skipped: $FAILED"
    
    # Calculate success rate
    if [ $IMPORTED -gt 0 ]; then
        TOTAL=$((IMPORTED + FAILED))
        SUCCESS_RATE=$(echo "scale=1; $IMPORTED * 100 / $TOTAL" | bc)
        echo "Success Rate: ${SUCCESS_RATE}%"
    fi
    
    echo ""
    echo "--- Last 10 Imports ---"
    grep "INFO - \[[0-9]*/2000\]" "$LOG_FILE" | tail -10
    
else
    echo "No log file found"
fi
ENDSSH

echo "========================================================================"
echo ""
echo "💡 Commands:"
echo "  • View live logs: ssh root@$VPS_HOST 'tail -f /root/lead_agent/logs/*.log'"
echo "  • Check progress: $0"
echo "  • Stop agent: ssh root@$VPS_HOST 'pkill -f autonomous_lead_agent.py'"
echo ""
echo "🔄 Refresh this view: watch -n 10 $0"
echo "========================================================================"

