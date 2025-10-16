# Apollo.io API Notes

## People Search Endpoint

**URL:** `POST https://api.apollo.io/api/v1/mixed_people/search`

**Authentication:** Bearer token in header

**Key Parameters for Your Use Case:**

### Job Title Filter
```json
"person_seniorities[]": ["owner", "founder"]
```

### Revenue Filter
```json
"revenue_range": {
  "min": 1000000  // $1M minimum
}
```

### Location Filter
```json
"person_locations[]": ["Florida"]
// or
"organization_locations[]": ["Florida"]
```

### Example Request Body
```json
{
  "person_seniorities[]": ["owner"],
  "revenue_range": {
    "min": 1000000
  },
  "person_locations[]": ["Florida"],
  "page": 1,
  "per_page": 100
}
```

## Rate Limits
- Display limit: 50,000 records (100 records per page, up to 500 pages)
- Requires Apollo pricing plan (not available on free tier)

## Response Format
Returns people with:
- name
- email
- title
- company
- location
- etc.

## Next Steps
1. Get Apollo API key
2. Test search with filters
3. Auto-import to Instantly

