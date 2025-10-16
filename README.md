# AI Agents Backup Repository

This repository contains all the autonomous AI agents and systems developed for lead generation, email outreach, and campaign management.

## Repository Structure

### 1. Distributable Package (`distributable-package/`)

This is the **complete, ready-to-distribute** Autonomous Lead Generation System. It includes everything needed to deploy the system on any VPS.

**Download:** `autonomous-lead-gen-system.tar.gz` (compressed version)

**Features:**
- Fully autonomous lead generation
- Automatic email account creation via Inframail
- Campaign management via Instantly.ai
- Lead discovery via Apollo.io
- Real-time monitoring dashboard
- Easy deployment scripts
- Comprehensive documentation

### 2. Lead Generation Agents (`lead-generation/`)

All versions of the autonomous lead generation agent:

- `autonomous_lead_agent.py` - Initial version
- `autonomous_lead_agent_v2.py` - Version 2 with improvements
- `autonomous_lead_agent_safe_ramp.py` - Safe ramping version
- `autonomous_lead_agent_production.py` - Production-ready version
- `autonomous_lead_agent_final.py` - **Final version (recommended)**

### 3. Apollo.io Integration (`apollo-integration/`)

Scripts for integrating with Apollo.io API for lead generation:

- `apollo_to_instantly_auto_importer.py` - Auto-imports leads from Apollo to Instantly
- `apollo_to_instantly_auto_importer_v2.py` - Improved version
- `apollo_business_owners_importer.py` - Targets business owners specifically
- `apollo_exact_match_importer.py` - Uses exact match criteria
- `apollo_api_notes.md` - API documentation and notes

### 4. Instantly.ai Integration (`instantly-integration/`)

Scripts for managing Instantly.ai campaigns:

- `instantly_campaign.py` - Basic campaign management
- `instantly_ai_agent_campaign.py` - AI agent campaign setup
- `create_ai_agent_campaign.py` - Campaign creation script
- `bulk_lead_import.py` - Bulk lead import functionality
- `add_sample_leads.py` - Add sample leads for testing
- Various `update_campaign_*.py` scripts for campaign modifications

### 5. Inframail Integration (`inframail-integration/`)

Scripts for managing email accounts via Inframail:

- `setup_inframail_accounts.py` - Automated email account setup

### 6. Dashboard (`dashboard/`)

Real-time monitoring dashboard for the lead generation system:

- `agent_dashboard.py` - Flask-based dashboard backend
- `dashboard.html` - Dashboard frontend interface
- `nginx_dashboard.conf` - Nginx configuration for the dashboard

### 7. Deployment Scripts (`deployment/`)

VPS deployment and monitoring scripts:

- `deploy_to_hostinger.sh` - Automated deployment to Hostinger VPS
- `monitor_vps_agent.sh` - VPS monitoring script

### 8. Documentation (`docs/`)

All documentation files including:

- Setup guides
- Configuration instructions
- Cost breakdowns
- Scaling strategies
- System architecture

## Quick Start

To deploy the complete system, use the distributable package:

```bash
# Extract the package
tar -xzf autonomous-lead-gen-system.tar.gz

# Run the installation
cd lead_gen_package
sudo bash scripts/install.sh

# Configure your API keys
nano /opt/lead_agent/config/config.py

# Run the setup wizard
sudo bash /opt/lead_agent/scripts/setup.sh

# Start the system
sudo systemctl start lead-agent lead-dashboard
```

## System Requirements

- VPS running Ubuntu 22.04 or similar Debian-based OS
- Root access
- API keys for:
  - Apollo.io
  - Instantly.ai
  - Inframail
- At least one domain name for email sending

## Key Features

- **Autonomous Operation:** Runs 24/7 without manual intervention
- **Scalable:** Can scale to thousands of emails per day
- **Safe Ramping:** Gradually increases sending volume to maintain reputation
- **Real-time Monitoring:** Web dashboard for tracking all activities
- **Production-Ready:** Battle-tested and deployed on live VPS

## Author

**Mikee Shattuck**

## License

MIT License - See individual package LICENSE files for details

