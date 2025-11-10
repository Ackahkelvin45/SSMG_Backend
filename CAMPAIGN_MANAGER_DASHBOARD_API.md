# Campaign Manager Dashboard API

## Overview

The dashboard endpoint provides role-specific data. Campaign Managers receive a customized dashboard showing only their assigned campaigns and related submissions.

---

## Endpoint

**URL:** `GET /api/users/dashboard/`

**Authentication:** Required

**Description:** Returns dashboard data based on user role. Campaign Managers see only their assigned campaigns.

---

## Campaign Manager Dashboard Response

### Request

```bash
curl -X GET http://ssmg-backend.onrender.com/api/users/dashboard/ \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### Response Structure

```json
{
  "user": {
    "id": 10,
    "username": "johndoe",
    "email": "john@example.com",
    "full_name": "John Doe",
    "role": "CAMPAIGN_MANAGER",
    "phone_number": "+1234567890",
    "profile_picture": "http://example.com/media/profile_pictures/john.jpg"
  },
  "total_assigned_campaigns": 3,
  "assigned_campaigns": [
    {
      "id": 1,
      "name": "State of the Flock 2025",
      "description": "Campaign description here",
      "campaign_type": "StateOfTheFlockCampaign",
      "status": "Active",
      "created_at": "2025-01-01T00:00:00Z",
      "icon": "http://example.com/media/icons/sof.png"
    },
    {
      "id": 5,
      "name": "Soul Winning Initiative",
      "description": "Campaign description here",
      "campaign_type": "SoulWinningCampaign",
      "status": "Active",
      "created_at": "2025-01-15T00:00:00Z",
      "icon": "http://example.com/media/icons/sw.png"
    },
    {
      "id": 10,
      "name": "Technology Upgrade",
      "description": "Campaign description here",
      "campaign_type": "TechnologyCampaign",
      "status": "Active",
      "created_at": "2025-02-01T00:00:00Z",
      "icon": "http://example.com/media/icons/tech.png"
    }
  ],
  "recent_submissions": [
    {
      "id": 150,
      "campaign_name": "State of the Flock 2025",
      "campaign_type": "State of the Flock",
      "service_name": "Downtown Church",
      "submission_period": "2025-11-01",
      "created_at": "2025-11-10T14:30:00Z"
    },
    {
      "id": 148,
      "campaign_name": "Soul Winning Initiative",
      "campaign_type": "Soul Winning",
      "service_name": "Suburb Church",
      "submission_period": "2025-11-01",
      "created_at": "2025-11-09T10:15:00Z"
    }
  ],
  "recent_campaigns": [
    {
      "id": 1,
      "name": "State of the Flock 2025",
      "description": "Campaign description here",
      "campaign_type": "StateOfTheFlockCampaign",
      "status": "Active",
      "created_at": "2025-01-01T00:00:00Z",
      "icon": "http://example.com/media/icons/sof.png"
    }
  ]
}
```

---

## Response Fields

### User Object

| Field | Type | Description |
|-------|------|-------------|
| `id` | integer | User ID |
| `username` | string | Username |
| `email` | string | Email address |
| `full_name` | string | First name + Last name |
| `role` | string | User role (always "CAMPAIGN_MANAGER") |
| `phone_number` | string | Phone number |
| `profile_picture` | string (URL) | Full URL to profile picture (null if not set) |

### Top Level Fields

| Field | Type | Description |
|-------|------|-------------|
| `total_assigned_campaigns` | integer | Total number of campaigns assigned to this manager |
| `assigned_campaigns` | array | List of all campaigns assigned to this manager |
| `recent_submissions` | array | Most recent 10 submissions made by this manager (only for assigned campaigns) |
| `recent_campaigns` | array | First 5 assigned campaigns (for quick access) |

### Campaign Object (in assigned_campaigns)

| Field | Type | Description |
|-------|------|-------------|
| `id` | integer | Campaign ID |
| `name` | string | Campaign name |
| `description` | string | Campaign description |
| `campaign_type` | string | Campaign model class name |
| `status` | string | Campaign status ("Active" or "Inactive") |
| `created_at` | datetime | Campaign creation date |
| `icon` | string (URL) | Full URL to campaign icon (null if not set) |

### Submission Object (in recent_submissions)

| Field | Type | Description |
|-------|------|-------------|
| `id` | integer | Submission ID |
| `campaign_name` | string | Name of the campaign |
| `campaign_type` | string | Human-readable campaign type |
| `service_name` | string | Name of the service/church |
| `submission_period` | date | Submission period (YYYY-MM-DD) |
| `created_at` | datetime | When the submission was created |

---

## Key Features

### 1. **Filtered Data**
- Campaign Managers only see campaigns they're assigned to
- Recent submissions are filtered to assigned campaigns only
- No access to campaigns they're not managing

### 2. **Comprehensive User Info**
- Full user profile details
- Role identification
- Profile picture URL (if set)

### 3. **Campaign Overview**
- Total count of assigned campaigns
- Complete list of assigned campaigns with details
- Campaign icons and status

### 4. **Recent Activity**
- Last 10 submissions (across all assigned campaigns)
- Sorted by creation date (most recent first)
- Shows which service each submission is for

### 5. **Quick Access**
- `recent_campaigns` provides first 5 assigned campaigns
- Useful for displaying in a "Quick Access" section

---

## Use Cases

### Dashboard UI Example

```javascript
const fetchDashboard = async () => {
  const response = await fetch('/api/users/dashboard/', {
    headers: {
      'Authorization': `Bearer ${token}`
    }
  });
  
  const data = await response.json();
  
  // Display user info
  console.log(`Welcome, ${data.user.full_name}`);
  console.log(`You manage ${data.total_assigned_campaigns} campaigns`);
  
  // Display assigned campaigns
  data.assigned_campaigns.forEach(campaign => {
    console.log(`- ${campaign.name} (${campaign.status})`);
  });
  
  // Display recent submissions
  console.log('\nRecent Submissions:');
  data.recent_submissions.forEach(sub => {
    console.log(`${sub.campaign_name} at ${sub.service_name}`);
  });
};
```

---

### React Component Example

```javascript
import React, { useEffect, useState } from 'react';

const CampaignManagerDashboard = () => {
  const [dashboard, setDashboard] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch('/api/users/dashboard/', {
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('token')}`
      }
    })
      .then(res => res.json())
      .then(data => {
        setDashboard(data);
        setLoading(false);
      });
  }, []);

  if (loading) return <div>Loading...</div>;

  return (
    <div className="dashboard">
      {/* User Profile */}
      <div className="user-profile">
        <img src={dashboard.user.profile_picture} alt="Profile" />
        <h1>Welcome, {dashboard.user.full_name}</h1>
        <p>Role: {dashboard.user.role}</p>
      </div>

      {/* Campaign Summary */}
      <div className="campaign-summary">
        <h2>Your Campaigns ({dashboard.total_assigned_campaigns})</h2>
        <div className="campaigns-grid">
          {dashboard.assigned_campaigns.map(campaign => (
            <div key={campaign.id} className="campaign-card">
              <img src={campaign.icon} alt={campaign.name} />
              <h3>{campaign.name}</h3>
              <p>{campaign.description}</p>
              <span className={`status ${campaign.status.toLowerCase()}`}>
                {campaign.status}
              </span>
            </div>
          ))}
        </div>
      </div>

      {/* Recent Submissions */}
      <div className="recent-submissions">
        <h2>Recent Submissions</h2>
        <table>
          <thead>
            <tr>
              <th>Campaign</th>
              <th>Service</th>
              <th>Period</th>
              <th>Date</th>
            </tr>
          </thead>
          <tbody>
            {dashboard.recent_submissions.map(sub => (
              <tr key={sub.id}>
                <td>{sub.campaign_name}</td>
                <td>{sub.service_name}</td>
                <td>{sub.submission_period}</td>
                <td>{new Date(sub.created_at).toLocaleDateString()}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* Quick Access */}
      <div className="quick-access">
        <h2>Quick Access</h2>
        {dashboard.recent_campaigns.map(campaign => (
          <button key={campaign.id} onClick={() => navigateTo(campaign.id)}>
            {campaign.name}
          </button>
        ))}
      </div>
    </div>
  );
};

export default CampaignManagerDashboard;
```

---

## Comparison: Campaign Manager vs Other Roles

| Feature | Campaign Manager | Pastor/Helper | Admin |
|---------|-----------------|---------------|-------|
| **Campaigns Shown** | Only assigned campaigns | All campaigns | All campaigns |
| **Submissions Shown** | Only for assigned campaigns | All user's submissions | All submissions |
| **Service Restriction** | None (can submit for any service) | Restricted to their service | None |
| **User Details** | Yes | Yes | Yes |
| **Total Count** | Assigned campaigns only | All campaigns | All campaigns |

---

## Error Handling

### Not Authenticated

```json
{
  "detail": "Authentication credentials were not provided."
}
```

**Status Code:** 401 Unauthorized

---

### No Assigned Campaigns

If a Campaign Manager has no assigned campaigns:

```json
{
  "user": { ... },
  "total_assigned_campaigns": 0,
  "assigned_campaigns": [],
  "recent_submissions": [],
  "recent_campaigns": []
}
```

**Status Code:** 200 OK

---

## Testing

### Test 1: Campaign Manager Dashboard

```bash
# Login as Campaign Manager
TOKEN=$(curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username":"johndoe","password":"kelvin"}' \
  | jq -r '.access')

# Get dashboard
curl -X GET http://localhost:8000/api/users/dashboard/ \
  -H "Authorization: Bearer $TOKEN"
```

**Expected:** Dashboard with assigned campaigns only

---

### Test 2: Pastor Dashboard (Standard)

```bash
# Login as Pastor
TOKEN=$(curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username":"pastor","password":"password"}' \
  | jq -r '.access')

# Get dashboard
curl -X GET http://localhost:8000/api/users/dashboard/ \
  -H "Authorization: Bearer $TOKEN"
```

**Expected:** Standard dashboard with all campaigns

---

## Notes

- Campaign Managers automatically get a customized dashboard
- The dashboard intelligently filters based on user role
- No additional configuration needed - it just works!
- Profile pictures and campaign icons return full URLs for easy display
- Recent submissions are limited to 10 for performance
- Submissions are filtered to only show those for assigned campaigns

---

## Summary

The Campaign Manager dashboard provides:
- ✅ User profile details
- ✅ Total assigned campaigns count
- ✅ Complete list of assigned campaigns
- ✅ Recent submissions (filtered to assigned campaigns)
- ✅ Quick access to recent campaigns

Perfect for building a Campaign Manager-specific UI! 🎉

