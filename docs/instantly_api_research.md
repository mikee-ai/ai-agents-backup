# Instantly.ai API Research Findings

## API Overview
- **Version**: API V2 (V1 is deprecated)
- **Base URL**: https://api.instantly.ai/
- **Authentication**: Bearer token authentication
- **Documentation**: https://developer.instantly.ai/

## Authentication
- Uses Bearer token in Authorization header: `Authorization: Bearer {api_key}`
- Multiple API keys can be created
- API scopes for granular control
- Requires Hypergrowth plan or above to access API

## Key Endpoints

### Campaign Management
- **POST /api/v2/campaigns** - Create campaign
- **GET /api/v2/campaigns** - List campaigns
- **POST /api/v2/campaigns/{id}/activate** - Start/resume campaign
- **POST /api/v2/campaigns/{id}/pause** - Pause campaign
- **GET /api/v2/campaigns/{id}** - Get campaign details
- **PATCH /api/v2/campaigns/{id}** - Update campaign
- **DELETE /api/v2/campaigns/{id}** - Delete campaign

### Lead Management
- **POST /api/v2/leads** - Create lead (add to campaign)
- **POST /api/v2/leads/list** - List leads with filters
- **GET /api/v2/leads/{id}** - Get lead details
- **PATCH /api/v2/leads/{id}** - Update lead
- **DELETE /api/v2/leads/{id}** - Delete lead
- **POST /api/v2/leads/update-interest-status** - Update lead interest status

### Email Account Management
- **POST /api/v2/accounts** - Add email account
- **GET /api/v2/accounts** - List email accounts
- **GET /api/v2/accounts/{email}** - Get account details
- **PATCH /api/v2/accounts/{email}** - Update account
- **DELETE /api/v2/accounts/{email}** - Delete account

### Analytics
- **GET /api/v2/campaigns/analytics** - Get campaign analytics
- **GET /api/v2/campaigns/analytics/overview** - Get analytics overview
- **GET /api/v2/campaigns/analytics/daily** - Get daily analytics

## Campaign Schema Key Fields
- `name` - Campaign name (required)
- `campaign_schedule` - Schedule with timing, days, timezone (required)
- `sequences` - Email sequences/steps with variants (required)
- `email_list` - Array of sender email addresses
- `daily_limit` - Daily email sending limit
- `stop_on_reply` - Stop campaign when lead replies
- `link_tracking` - Track link clicks
- `open_tracking` - Track email opens
- `text_only` - Send as plain text
- `daily_max_leads` - Max new leads to contact daily

## Lead Schema Key Fields
- `email` - Lead email address (required)
- `first_name` - First name
- `last_name` - Last name
- `company_name` - Company name
- `campaign` - Campaign ID to add lead to
- `personalization` - Custom personalization text
- `payload` - Custom variables (key-value pairs)

## Lead Status Values
- 1: Active
- 2: Paused
- 3: Completed
- -1: Bounced
- -2: Unsubscribed
- -3: Skipped

## Campaign Status Values
- 0: Draft
- 1: Active
- 2: Paused
- 3: Completed
- 4: Running Subsequences
- -99: Account Suspended
- -1: Accounts Unhealthy
- -2: Bounce Protect

## API Capabilities for Cold Email Campaign
1. ✅ Create and manage campaigns
2. ✅ Add/sync leads to campaigns
3. ✅ Track email opens, clicks, replies
4. ✅ Manage email sending accounts
5. ✅ Schedule campaigns with timezone support
6. ✅ Set daily limits and sending rules
7. ✅ Get analytics and performance data
8. ✅ Update lead interest status
9. ✅ Stop on reply functionality
10. ✅ Custom variables/personalization

## Next Steps
1. Decode the provided API key
2. Test authentication
3. Create a cold email campaign
4. Add leads to the campaign
5. Activate the campaign

