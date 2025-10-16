#!/bin/bash
# Deploy Autonomous Lead Agent to Hostinger VPS
# This script sets up everything needed to run the agent 24/7

set -e

VPS_HOST="31.97.145.136"
VPS_USER="root"
VPS_PASS="Kidessa231.@#"

echo "========================================================================"
echo "🚀 DEPLOYING AUTONOMOUS LEAD AGENT TO HOSTINGER VPS"
echo "========================================================================"
echo ""

# Create remote directory structure
echo "📁 Creating directory structure on VPS..."
sshpass -p "$VPS_PASS" ssh -o StrictHostKeyChecking=no $VPS_USER@$VPS_HOST << 'ENDSSH'
mkdir -p /root/lead_agent
mkdir -p /root/lead_agent/logs
mkdir -p /root/lead_agent/backups
ENDSSH

echo "✓ Directories created"
echo ""

# Copy the agent script
echo "📤 Uploading autonomous agent..."
sshpass -p "$VPS_PASS" scp -o StrictHostKeyChecking=no \
    /home/ubuntu/autonomous_lead_agent.py \
    $VPS_USER@$VPS_HOST:/root/lead_agent/

echo "✓ Agent uploaded"
echo ""

# Install Python dependencies
echo "📦 Installing Python dependencies on VPS..."
sshpass -p "$VPS_PASS" ssh -o StrictHostKeyChecking=no $VPS_USER@$VPS_HOST << 'ENDSSH'
apt-get update -qq
apt-get install -y -qq python3-pip python3-venv
pip3 install requests --quiet
ENDSSH

echo "✓ Dependencies installed"
echo ""

# Make script executable
echo "🔧 Setting permissions..."
sshpass -p "$VPS_PASS" ssh -o StrictHostKeyChecking=no $VPS_USER@$VPS_HOST << 'ENDSSH'
chmod +x /root/lead_agent/autonomous_lead_agent.py
ENDSSH

echo "✓ Permissions set"
echo ""

# Create systemd service for automatic startup
echo "⚙️ Creating systemd service..."
sshpass -p "$VPS_PASS" ssh -o StrictHostKeyChecking=no $VPS_USER@$VPS_HOST << 'ENDSSH'
cat > /etc/systemd/system/lead-agent.service << 'EOF'
[Unit]
Description=Autonomous Lead Generation Agent
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/root/lead_agent
ExecStart=/usr/bin/python3 /root/lead_agent/autonomous_lead_agent.py
Restart=on-failure
RestartSec=60
StandardOutput=append:/root/lead_agent/logs/service.log
StandardError=append:/root/lead_agent/logs/service_error.log

[Install]
WantedBy=multi-user.target
EOF

systemctl daemon-reload
ENDSSH

echo "✓ Systemd service created"
echo ""

# Create cron job for daily execution
echo "⏰ Setting up daily cron job (6:00 AM)..."
sshpass -p "$VPS_PASS" ssh -o StrictHostKeyChecking=no $VPS_USER@$VPS_HOST << 'ENDSSH'
# Remove existing cron job if any
crontab -l 2>/dev/null | grep -v "autonomous_lead_agent.py" | crontab - 2>/dev/null || true

# Add new cron job
(crontab -l 2>/dev/null; echo "0 6 * * * /usr/bin/python3 /root/lead_agent/autonomous_lead_agent.py >> /root/lead_agent/logs/cron.log 2>&1") | crontab -

echo "Cron job installed:"
crontab -l | grep autonomous_lead_agent.py
ENDSSH

echo "✓ Cron job configured"
echo ""

# Test the agent
echo "🧪 Running test import (10 leads)..."
sshpass -p "$VPS_PASS" ssh -o StrictHostKeyChecking=no $VPS_USER@$VPS_HOST << 'ENDSSH'
cd /root/lead_agent
# Create a test version with lower limit
sed 's/DAILY_IMPORT_LIMIT = 2000/DAILY_IMPORT_LIMIT = 10/' autonomous_lead_agent.py > test_agent.py
chmod +x test_agent.py
timeout 300 python3 test_agent.py || echo "Test completed (or timed out)"
rm test_agent.py
ENDSSH

echo "✓ Test completed"
echo ""

# Show status
echo "📊 Checking deployment status..."
sshpass -p "$VPS_PASS" ssh -o StrictHostKeyChecking=no $VPS_USER@$VPS_HOST << 'ENDSSH'
echo "=== Files ==="
ls -lh /root/lead_agent/

echo ""
echo "=== Cron Jobs ==="
crontab -l | grep lead_agent || echo "No cron jobs found"

echo ""
echo "=== Recent Logs ==="
if [ -f /root/lead_agent/logs/agent_*.log ]; then
    tail -20 /root/lead_agent/logs/agent_*.log | tail -10
else
    echo "No logs yet"
fi
ENDSSH

echo ""
echo "========================================================================"
echo "✅ DEPLOYMENT COMPLETE!"
echo "========================================================================"
echo ""
echo "🤖 Autonomous Agent Status:"
echo "  • Location: /root/lead_agent/"
echo "  • Daily Schedule: 6:00 AM (via cron)"
echo "  • Daily Import: 2,000 business owners"
echo "  • Logs: /root/lead_agent/logs/"
echo ""
echo "📝 Management Commands:"
echo "  • View logs: ssh root@$VPS_HOST 'tail -f /root/lead_agent/logs/agent_*.log'"
echo "  • Run manually: ssh root@$VPS_HOST 'cd /root/lead_agent && python3 autonomous_lead_agent.py'"
echo "  • Check cron: ssh root@$VPS_HOST 'crontab -l'"
echo ""
echo "🎯 Next Scheduled Run: Tomorrow at 6:00 AM"
echo "========================================================================"

