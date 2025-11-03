# Dashboard API Documentation

## Overview

The Dashboard API provides a unified view of the logged-in user's activity, including their profile, recent submissions, recently accessed campaigns, and statistics.

---

## Endpoint

**GET** `/auth/users/dashboard/`

**Authentication:** Required (JWT Token)

**Method:** GET

**Permissions:** Authenticated users only

---

## Response Structure

```json
{
  "user": {
    "id": 1,
    "first_name": "John",
    "username": "john_doe",
    "last_name": "Doe",
    "email": "john@example.com",
    "phone_number": "+1234567890",
    "service": {
      "id": 5,
      "name": "Downtown Service",
      "location": "Downtown Area",
      "total_members": 150,
      "created_at": "2025-01-01T00:00:00Z",
      "updated_at": "2025-10-18T00:00:00Z"
    },
    "created_at": "2025-01-01T00:00:00Z",
    "role": "PASTOR",
    "profile_picture": "http://example.com/media/profile_pictures/photo.jpg",
    "password_changed": true
  },
  "recent_submissions": [
    {
      "id": 45,
      "campaign_id": 2,
      "campaign_name": "Downtown Soul Winning",
      "campaign_type": "Soul Winning",
      "submission_period": "2025-10-01",
      "created_at": "2025-10-18T10:00:00Z",
      "preview_data": {
        "no_of_souls_won": 25,
        "no_of_crusades": 3
      }
    },
    {
      "id": 44,
      "campaign_id": 1,
      "campaign_name": "October State of Flock",
      "campaign_type": "State of the Flock",
      "submission_period": "2025-10-01",
      "created_at": "2025-10-17T14:30:00Z",
      "preview_data": {
        "total_membership": 150,
        "stable": 120
      }
    },
    {
      "id": 43,
      "campaign_id": 3,
      "campaign_name": "Prayer Campaign",
      "campaign_type": "Antibrutish",
      "submission_period": "2025-10-01",
      "created_at": "2025-10-16T09:00:00Z",
      "preview_data": {
        "type_of_prayer": "Intercession",
        "hours_prayed": "5.50"
      }
    },
    {
      "id": 42,
      "campaign_id": 4,
      "campaign_name": "Community Multiplication",
      "campaign_type": "Multiplication",
      "submission_period": "2025-10-01",
      "created_at": "2025-10-15T16:20:00Z",
      "preview_data": {
        "no_of_outreaches": 8
      }
    },
    {
      "id": 41,
      "campaign_id": 5,
      "campaign_name": "Testimony Sharing",
      "campaign_type": "Testimony",
      "submission_period": "2025-10-01",
      "created_at": "2025-10-14T11:15:00Z",
      "preview_data": {
        "number_of_testimonies_shared": 12
      }
    }
  ],
  "recent_campaigns": [
    {
      "id": 2,
      "name": "Downtown Soul Winning",
      "campaign_type": "Soul Winning",
      "status": "Active",
      "icon": "http://example.com/media/icons/soul_winning.png",
      "last_accessed": "2025-10-18T10:00:00Z"
    },
    {
      "id": 1,
      "name": "October State of Flock",
      "campaign_type": "State of the Flock",
      "status": "Active",
      "icon": "http://example.com/media/icons/state_of_flock.png",
      "last_accessed": "2025-10-17T14:30:00Z"
    },
    {
      "id": 3,
      "name": "Prayer Campaign",
      "campaign_type": "Antibrutish",
      "status": "Active",
      "icon": "http://example.com/media/icons/prayer.png",
      "last_accessed": "2025-10-16T09:00:00Z"
    },
    {
      "id": 4,
      "name": "Community Multiplication",
      "campaign_type": "Multiplication",
      "status": "Active",
      "icon": null,
      "last_accessed": "2025-10-15T16:20:00Z"
    },
    {
      "id": 5,
      "name": "Testimony Sharing",
      "campaign_type": "Testimony",
      "status": "Inactive",
      "icon": "http://example.com/media/icons/testimony.png",
      "last_accessed": "2025-10-14T11:15:00Z"
    }
  ],
  "statistics": {
    "total_submissions": 47,
    "active_campaigns": 12,
    "submissions_this_month": 8
  }
}
```

---

## Field Descriptions

### User Object
| Field | Type | Description |
|-------|------|-------------|
| `id` | Integer | User's unique identifier |
| `first_name` | String | User's first name |
| `last_name` | String | User's last name |
| `username` | String | User's username |
| `email` | String | User's email address |
| `phone_number` | String | User's phone number |
| `service` | Object | User's assigned service information |
| `role` | String | User's role (ADMIN, PASTOR, HELPER) |
| `profile_picture` | String/URL | URL to user's profile picture |
| `password_changed` | Boolean | Whether user has changed their default password |
| `created_at` | DateTime | When the user account was created |

### Recent Submissions Array
Shows the **5 most recent submissions** created by the user across **all 20 campaign types**, sorted by creation date (newest first).

| Field | Type | Description |
|-------|------|-------------|
| `id` | Integer | Submission's unique identifier |
| `campaign_id` | Integer | ID of the campaign this submission belongs to |
| `campaign_name` | String | Name of the campaign |
| `campaign_type` | String | Type of campaign (e.g., "Soul Winning", "State of the Flock") |
| `submission_period` | Date | The period this submission covers (nullable) |
| `created_at` | DateTime | When the submission was created |
| `preview_data` | Object | Key metrics from the submission (varies by campaign type) |

### Recent Campaigns Array
Shows the **5 campaigns** the user most recently submitted to, sorted by the timestamp of their last submission to each campaign.

| Field | Type | Description |
|-------|------|-------------|
| `id` | Integer | Campaign's unique identifier |
| `name` | String | Campaign name |
| `campaign_type` | String | Type of campaign |
| `status` | String | Campaign status (Active/Inactive) |
| `icon` | String/URL | URL to campaign icon (null if none) |
| `last_accessed` | DateTime | When user last submitted to this campaign |

### Statistics Object
| Field | Type | Description |
|-------|------|-------------|
| `total_submissions` | Integer | Total number of submissions by this user (all time, all types) |
| `active_campaigns` | Integer | Number of unique campaigns the user has submitted to |
| `submissions_this_month` | Integer | Number of submissions created this month |

---

## Preview Data by Campaign Type

Different campaign types show different preview fields:

### Soul Winning
- `no_of_souls_won`: Number of souls won
- `no_of_crusades`: Number of crusades held

### State of the Flock
- `total_membership`: Total membership count
- `stable`: Number of stable members

### Antibrutish
- `type_of_prayer`: Type of prayer session
- `hours_prayed`: Hours spent in prayer

### Multiplication
- `no_of_outreaches`: Number of outreaches conducted

### Testimony
- `number_of_testimonies_shared`: Number of testimonies shared

*Other campaign types will show relevant fields based on their model structure*

---

## Usage Examples

### cURL Example

```bash
curl -X GET http://localhost:8000/auth/users/dashboard/ \
  -H "Authorization: Bearer <your-jwt-token>" \
  -H "Content-Type: application/json"
```

### JavaScript/Fetch Example

```javascript
fetch('http://localhost:8000/auth/users/dashboard/', {
  method: 'GET',
  headers: {
    'Authorization': `Bearer ${token}`,
    'Content-Type': 'application/json'
  }
})
.then(response => response.json())
.then(data => {
  console.log('User:', data.user);
  console.log('Recent Submissions:', data.recent_submissions);
  console.log('Recent Campaigns:', data.recent_campaigns);
  console.log('Statistics:', data.statistics);
})
.catch(error => console.error('Error:', error));
```

### Python/Requests Example

```python
import requests

url = 'http://localhost:8000/auth/users/dashboard/'
headers = {
    'Authorization': f'Bearer {token}',
    'Content-Type': 'application/json'
}

response = requests.get(url, headers=headers)
dashboard_data = response.json()

print(f"Total Submissions: {dashboard_data['statistics']['total_submissions']}")
print(f"Recent Submissions: {len(dashboard_data['recent_submissions'])}")
print(f"Recent Campaigns: {len(dashboard_data['recent_campaigns'])}")
```

---

## Important Notes

### Recent Submissions Logic
- Queries **all 20 submission types** (State of Flock, Soul Winning, Servants Armed and Trained, etc.)
- Combines all submissions from all types into one list
- Sorts by `created_at` timestamp (newest first)
- Returns the **top 5 most recent**

**Example:** If you submitted to Soul Winning today, State of Flock yesterday, and Testimony last week, they will all appear mixed together in chronological order.

### Recent Campaigns Logic
- For each submission type, finds the most recent submission to each campaign
- Campaigns are sorted by the timestamp of the user's **last submission** to that campaign
- Returns the **top 5 campaigns** you've most recently interacted with

**Example:** If your last Soul Winning submission was today and your last State of Flock submission was yesterday, "Soul Winning Campaign" will appear first.

### Performance Considerations
- The endpoint queries all 20 submission models
- Uses `select_related('campaign')` for optimization
- Limits initial queries to 5 per model type
- Total query time is typically under 500ms for average usage

### Edge Cases
- **No submissions:** All arrays will be empty, statistics will show 0
- **No service:** Service field will be `null`
- **Campaign deleted:** Submissions to deleted campaigns are skipped
- **Null submission periods:** Some campaigns don't require submission periods

---

## Error Responses

### 401 Unauthorized
```json
{
  "detail": "Authentication credentials were not provided."
}
```

### 401 Invalid Token
```json
{
  "detail": "Given token not valid for any token type"
}
```

---

## Integration Tips

### Frontend Dashboard Display

```javascript
// Display user info
const { user, recent_submissions, recent_campaigns, statistics } = dashboardData;

// Show welcome message
console.log(`Welcome ${user.first_name} ${user.last_name}`);
console.log(`Service: ${user.service.name}`);

// Display statistics cards
console.log(`Total Submissions: ${statistics.total_submissions}`);
console.log(`Active Campaigns: ${statistics.active_campaigns}`);
console.log(`This Month: ${statistics.submissions_this_month}`);

// Recent activity feed
recent_submissions.forEach(submission => {
  console.log(`${submission.campaign_type}: ${submission.campaign_name}`);
  console.log(`Submitted: ${new Date(submission.created_at).toLocaleDateString()}`);
  console.log(`Preview:`, submission.preview_data);
});

// Quick access to campaigns
recent_campaigns.forEach(campaign => {
  console.log(`${campaign.name} (${campaign.campaign_type})`);
  console.log(`Last accessed: ${new Date(campaign.last_accessed).toLocaleDateString()}`);
});
```

---

## Caching Recommendations

For production use, consider caching the dashboard response:

```python
from django.core.cache import cache

# In the view
cache_key = f'dashboard_{user.id}'
cached_data = cache.get(cache_key)

if cached_data:
    return Response(cached_data)

# ... generate dashboard_data ...

cache.set(cache_key, dashboard_data, timeout=300)  # 5 minutes
return Response(dashboard_data)
```

---

## Related Endpoints

- `GET /auth/users/get_profile/` - Get detailed user profile
- `GET /campaigns/all/` - List all available campaigns
- `GET /campaigns/{campaign-type}/submissions/` - List submissions for specific campaign type

---

## Support

For issues or questions about the Dashboard API, please contact the development team or refer to the main API documentation.

