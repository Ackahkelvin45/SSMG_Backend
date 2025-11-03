# Dashboard API Endpoint Documentation

This document describes the dashboard API endpoint that provides all data needed for your mobile app dashboard.

---

## Endpoint

```
GET /auth/users/dashboard/
```

**Authentication:** Required (Bearer Token)

---

## Response Structure

```json
{
  "service": {
    "id": 1,
    "name": "Accra Central Service",
    "location": "Accra Central",
    "total_members": 1250
  },
  "statistics": {
    "active_campaigns": 5,
    "submissions_this_month": 12
  },
  "recent_submissions": [
    {
      "id": 42,
      "campaign_id": 5,
      "campaign_name": "Youth Outreach Program",
      "campaign_type": "Soul Winning",
      "submission_period": "2025-01-15",
      "created_at": "2025-01-15T10:30:00Z",
      "submission_count": 188,
      "preview_data": {
        "no_of_souls_won": 25,
        "no_of_crusades": 3
      }
    }
  ],
  "active_campaigns": [
    {
      "id": 5,
      "name": "Member Registration",
      "campaign_type": "Testimony",
      "status": "ACTIVE",
      "icon": "http://your-domain.com/media/icons/testimony.png",
      "last_accessed": "2025-01-20T14:45:00Z",
      "submission_count": 180
    }
  ]
}
```

---

## Field Descriptions

### Service Object

| Field | Type | Description |
|-------|------|-------------|
| `id` | integer | Service ID |
| `name` | string | Service name |
| `location` | string | Service location |
| `total_members` | integer | Total number of members in the service |

**Note:** If user has no service assigned, `service` will be `null`.

---

### Statistics Object

| Field | Type | Description |
|-------|------|-------------|
| `active_campaigns` | integer | Number of campaigns the user has submitted to |
| `submissions_this_month` | integer | Total submissions made by user in the current month |

---

### Recent Submissions Array

Each item in `recent_submissions` contains:

| Field | Type | Description |
|-------|------|-------------|
| `id` | integer | Submission ID |
| `campaign_id` | integer | Campaign ID this submission belongs to |
| `campaign_name` | string | Name of the campaign |
| `campaign_type` | string | Type of campaign (e.g., "Soul Winning", "State of the Flock") |
| `submission_period` | date (YYYY-MM-DD) | The period this submission covers |
| `created_at` | datetime | When the submission was created |
| `submission_count` | integer | Total number of submissions for this campaign |
| `preview_data` | object | Campaign-specific preview data (varies by type) |

**Note:** Returns up to 5 most recent submissions, one per unique campaign.

---

### Active Campaigns Array

Each item in `active_campaigns` contains:

| Field | Type | Description |
|-------|------|-------------|
| `id` | integer | Campaign ID |
| `name` | string | Campaign name |
| `campaign_type` | string | Type of campaign |
| `status` | string | Campaign status (e.g., "ACTIVE", "INACTIVE") |
| `icon` | string or null | URL to campaign icon image |
| `last_accessed` | datetime | When user last submitted to this campaign |
| `submission_count` | integer | Total submissions user has made to this campaign |

**Note:** Returns up to 5 most recently accessed campaigns.

---

## Example Request

### JavaScript/React Native

```javascript
const fetchDashboard = async () => {
  try {
    const response = await fetch('http://your-domain.com/auth/users/dashboard/', {
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${authToken}`,
        'Content-Type': 'application/json'
      }
    });

    if (!response.ok) {
      throw new Error('Failed to fetch dashboard data');
    }

    const data = await response.json();
    return data;
  } catch (error) {
    console.error('Dashboard fetch error:', error);
    throw error;
  }
};
```

### Axios

```javascript
import axios from 'axios';

const getDashboard = async () => {
  try {
    const response = await axios.get('http://your-domain.com/auth/users/dashboard/', {
      headers: {
        'Authorization': `Bearer ${authToken}`
      }
    });
    return response.data;
  } catch (error) {
    console.error('Dashboard fetch error:', error);
    throw error;
  }
};
```

---

## Data Mapping for Mobile App UI

### Your Service Card

```javascript
// From API response
const service = response.service;

// Map to UI
serviceCard = {
  name: service?.name || "No Service Assigned",
  location: service?.location || "Location not specified",
  totalMembers: service?.total_members || 0
}
```

### Statistics Cards

```javascript
// From API response
const stats = response.statistics;

// Active Campaigns Card
activeCampaignsCard = {
  title: "Active Campaigns",
  value: stats.active_campaigns,
  icon: "🎯",
  subtitle: "Currently participating"
}

// Monthly Submissions Card
monthlySubmissionsCard = {
  title: "Monthly Submissions",
  value: stats.submissions_this_month,
  icon: "📝",
  subtitle: "This month's reports"
}
```

### Recent Submissions Section

```javascript
// From API response
const recentSubmissions = response.recent_submissions;

// Map each item
recentSubmissions.map(submission => ({
  campaignType: submission.campaign_type,        // Badge label
  campaignName: submission.campaign_name,        // Submission name
  submissionCount: submission.submission_count   // Count display
}))
```

### Active Campaigns Section

```javascript
// From API response
const activeCampaigns = response.active_campaigns;

// Map each item
activeCampaigns.map(campaign => ({
  campaignType: campaign.campaign_type,      // Badge label
  campaignName: campaign.name,                // Campaign name
  submissionCount: campaign.submission_count  // Submission count
}))
```

---

## Empty States Handling

### No Service Assigned
```json
{
  "service": null,
  ...
}
```

**UI Display:**
- Show "No Service Assigned" message
- Display placeholder text for location and members

### No Recent Submissions
```json
{
  "recent_submissions": [],
  ...
}
```

**UI Display:**
- Show empty state message
- Display "Browse Campaigns" button

### No Active Campaigns
```json
{
  "active_campaigns": [],
  ...
}
```

**UI Display:**
- Show empty state message
- Display "View All Campaigns" button

---

## Error Responses

### 401 Unauthorized
```json
{
  "detail": "Authentication credentials were not provided."
}
```

### 500 Internal Server Error
```json
{
  "detail": "A server error occurred."
}
```

---


---

## Preview Data Examples

Preview data varies by campaign type. Here are some examples:

### Soul Winning
```json
{
  "preview_data": {
    "no_of_souls_won": 25,
    "no_of_crusades": 3
  }
}
```

### State of the Flock
```json
{
  "preview_data": {
    "total_membership": 150,
    "stable": 120
  }
}
```

### Testimony
```json
{
  "preview_data": {
    "number_of_testimonies_shared": 5
  }
}
```

---

## Testing the Endpoint

### Using cURL
```bash
curl -X GET http://your-domain.com/auth/users/dashboard/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json"
```

### Using Postman/Insomnia
1. Method: `GET`
2. URL: `http://your-domain.com/auth/users/dashboard/`
3. Headers:
   - `Authorization: Bearer YOUR_ACCESS_TOKEN`
   - `Content-Type: application/json`

---

## Notes

1. **Authentication Required:** All requests must include a valid Bearer token
2. **Caching:** Consider caching dashboard data on the mobile app for offline viewing
3. **Refresh:** Implement pull-to-refresh to update dashboard data
4. **Error Handling:** Always handle null/empty responses gracefully
5. **Loading States:** Show skeleton loaders while fetching data

---

## Response Example (Full)

```json
{
  "service": {
    "id": 1,
    "name": "Accra Central Service",
    "location": "Accra Central",
    "total_members": 1250
  },
  "statistics": {
    "active_campaigns": 5,
    "submissions_this_month": 12
  },
  "recent_submissions": [
    {
      "id": 42,
      "campaign_id": 5,
      "campaign_name": "Youth Outreach Program",
      "campaign_type": "Soul Winning",
      "submission_period": "2025-01-15",
      "created_at": "2025-01-15T10:30:00Z",
      "submission_count": 188,
      "preview_data": {
        "no_of_souls_won": 25,
        "no_of_crusades": 3
      }
    },
    {
      "id": 38,
      "campaign_id": 3,
      "campaign_name": "Monthly Flock Report",
      "campaign_type": "State of the Flock",
      "submission_period": "2025-01-10",
      "created_at": "2025-01-10T09:15:00Z",
      "submission_count": 95,
      "preview_data": {
        "total_membership": 150,
        "stable": 120
      }
    }
  ],
  "active_campaigns": [
    {
      "id": 5,
      "name": "Youth Outreach Program",
      "campaign_type": "Soul Winning",
      "status": "ACTIVE",
      "icon": "http://your-domain.com/media/icons/soul-winning.png",
      "last_accessed": "2025-01-15T10:30:00Z",
      "submission_count": 188
    },
    {
      "id": 3,
      "name": "Monthly Flock Report",
      "campaign_type": "State of the Flock",
      "status": "ACTIVE",
      "icon": "http://your-domain.com/media/icons/state-of-flock.png",
      "last_accessed": "2025-01-10T09:15:00Z",
      "submission_count": 95
    }
  ]
}
```

---

This endpoint provides all the data needed for your mobile app dashboard UI!
