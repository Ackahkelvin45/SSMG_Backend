# Campaign Manager User Type

## Overview

**Campaign Managers** are a specialized user type in the SSMG Backend system designed to manage specific campaigns across all services. Unlike Pastors and Helpers who are tied to a single service, Campaign Managers can be assigned to one or more campaigns and can fill data for those campaigns across **all services**.

---

## Key Features

### 🎯 **Multi-Campaign Assignment**
- Campaign Managers can be assigned to **multiple campaigns**
- Each assignment is independent and can span different campaign types
- Assignments are managed through the `CampaignManagerAssignment` model

### 🌐 **Cross-Service Access**
- Campaign Managers are **NOT tied to a specific service**
- They can submit data for their assigned campaigns for **any service**
- This allows centralized campaign management across the organization

### 🔒 **Restricted Access**
- Campaign Managers **only see** campaigns they're assigned to
- They can **only view** submissions for their assigned campaigns
- They can **only create** submissions for their assigned campaigns
- All other campaigns and submissions are hidden from them

### 📊 **Customized Dashboard**
- Campaign Managers get a specialized dashboard view
- Shows only their assigned campaigns
- Displays recent submissions filtered to assigned campaigns
- Provides quick access to campaign information

---

## Creating a Campaign Manager

### API Endpoint

**POST** `/api/users/create-campaign-manager/`

### Request Body

```json
{
  "first_name": "John",
  "last_name": "Doe",
  "username": "johndoe",
  "email": "john@example.com",
  "phone_number": "+1234567890",
  "profile_picture": "<binary file>",
  "campaign_assignments": "[{\"campaign_name\": \"State of the Flock 2025\"}, {\"campaign_name\": \"Soul Winning Initiative\"}]"
}
```

### Required Fields

| Field | Type | Description |
|-------|------|-------------|
| `first_name` | string | First name of the Campaign Manager |
| `last_name` | string | Last name of the Campaign Manager |
| `username` | string | Unique username |
| `email` | string | Email address (must be unique) |
| `phone_number` | string | Phone number |
| `campaign_assignments` | string (JSON) | JSON string array of campaign assignments |

### Optional Fields

| Field | Type | Description |
|-------|------|-------------|
| `profile_picture` | file | Profile picture image |

### Campaign Assignments Format

The `campaign_assignments` field must be a **JSON string** containing an array of objects:

```json
[
  {"campaign_name": "State of the Flock 2025"},
  {"campaign_name": "Soul Winning Initiative"},
  {"campaign_name": "Technology Campaign"}
]
```

**Important Notes:**
- Campaign names are **case-insensitive**
- The system automatically finds the campaign by name across all campaign types
- If a campaign name is not found, an error is returned
- You can assign multiple campaigns in a single request

### Password

- **Passwords are auto-generated** (default: "kelvin")
- Password field is **not exposed** in the API
- Campaign Managers should change their password after first login

### Service Assignment

- Campaign Managers are **NOT assigned to any service**
- The `service` field is set to `None`
- This allows them to work across all services

---

## Response Example

### Success Response (201 Created)

```json
{
  "id": 10,
  "username": "johndoe",
  "email": "john@example.com",
  "full_name": "John Doe",
  "role": "CAMPAIGN_MANAGER",
  "phone_number": "+1234567890",
  "profile_picture": "http://example.com/media/profile_pictures/john.jpg",
  "assigned_campaigns": [
    {
      "id": 1,
      "name": "State of the Flock 2025",
      "campaign_type": "StateOfTheFlockCampaign"
    },
    {
      "id": 5,
      "name": "Soul Winning Initiative",
      "campaign_type": "SoulWinningCampaign"
    }
  ]
}
```

### Error Response (400 Bad Request)

```json
{
  "status": 400,
  "data": {
    "campaign_assignments": [
      "Campaign 'Non-existent Campaign' not found."
    ]
  }
}
```

---

## Permissions and Access

### ✅ What Campaign Managers CAN Do

1. **View Assigned Campaigns**
   - Access `/api/campaigns/all/` to see only assigned campaigns
   - View campaign details for assigned campaigns only

2. **View Submissions**
   - View submissions for assigned campaigns only
   - Access all submission endpoints filtered to assigned campaigns
   - See submission history for their assigned campaigns

3. **Create Submissions**
   - Create submissions for assigned campaigns
   - Submit data for any service (not restricted to one service)
   - Fill data across all services for their assigned campaigns

4. **Access Dashboard**
   - View customized dashboard with assigned campaigns
   - See recent submissions filtered to assigned campaigns
   - Access user profile information

### ❌ What Campaign Managers CANNOT Do

1. **View Unassigned Campaigns**
   - Cannot see campaigns they're not assigned to
   - `/api/campaigns/all/` returns only assigned campaigns

2. **View Unassigned Submissions**
   - Cannot see submissions for campaigns they're not assigned to
   - All submission endpoints are filtered to assigned campaigns

3. **Create Submissions for Unassigned Campaigns**
   - Cannot create submissions for campaigns they're not assigned to
   - Attempting to do so returns: `{"campaign": "You are not assigned to this campaign."}`

4. **Service-Specific Restrictions**
   - Not applicable - Campaign Managers work across all services

---

## Dashboard

### Endpoint

**GET** `/api/users/dashboard/`

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
      "description": "Campaign description",
      "campaign_type": "StateOfTheFlockCampaign",
      "status": "Active",
      "created_at": "2025-01-01T00:00:00Z",
      "icon": "http://example.com/media/icons/sof.png"
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
    }
  ],
  "recent_campaigns": [
    {
      "id": 1,
      "name": "State of the Flock 2025",
      "description": "Campaign description",
      "campaign_type": "StateOfTheFlockCampaign",
      "status": "Active",
      "created_at": "2025-01-01T00:00:00Z",
      "icon": "http://example.com/media/icons/sof.png"
    }
  ]
}
```

### Dashboard Features

- **User Details**: Complete profile information
- **Total Assigned Campaigns**: Count of assigned campaigns
- **Assigned Campaigns**: Full list with details
- **Recent Submissions**: Last 10 submissions (filtered to assigned campaigns)
- **Recent Campaigns**: First 5 campaigns for quick access

---

## Campaign Filtering

### `/api/campaigns/all/` Endpoint

**For Campaign Managers:**
- Returns **only** campaigns assigned to the manager
- Filtered automatically based on `CampaignManagerAssignment` records
- Other campaigns are completely hidden

**For Other Roles:**
- Returns all campaigns (unchanged behavior)

### Example

**Campaign Manager Request:**
```bash
GET /api/campaigns/all/
Authorization: Bearer <campaign_manager_token>
```

**Response:**
```json
{
  "count": 2,
  "results": [
    {
      "id": 1,
      "name": "State of the Flock 2025",
      "campaign_type": "State of the Flock",
      ...
    },
    {
      "id": 5,
      "name": "Soul Winning Initiative",
      "campaign_type": "Soul Winning",
      ...
    }
  ]
}
```

---

## Submission Filtering

### All Submission Endpoints

All submission endpoints automatically filter results for Campaign Managers:

- `/api/campaigns/state-of-flock/submissions/`
- `/api/campaigns/soul-winning/submissions/`
- `/api/campaigns/technology/submissions/`
- ... (all 20 submission types)

**For Campaign Managers:**
- Returns **only** submissions for assigned campaigns
- Filtered by `campaign_id` matching assigned campaigns
- Other submissions are completely hidden

**For Other Roles:**
- Returns all submissions (unchanged behavior)

### Creating Submissions

When a Campaign Manager creates a submission:

1. **Validation Check**: System verifies the campaign is assigned to the manager
2. **Success**: If assigned, submission is created
3. **Error**: If not assigned, returns:
   ```json
   {
     "campaign": ["You are not assigned to this campaign."]
   }
   ```

### Example

**Campaign Manager Creating Submission:**
```bash
POST /api/campaigns/soul-winning/submissions/
Authorization: Bearer <campaign_manager_token>
Content-Type: multipart/form-data

campaign: 5
submission_period: 2025-11-01
date: 2025-11-10
no_of_crusades: 3
...
```

**If campaign 5 is assigned:**
- ✅ Submission created successfully

**If campaign 5 is NOT assigned:**
- ❌ Error: `{"campaign": ["You are not assigned to this campaign."]}`

---

## Comparison with Other User Types

| Feature | Campaign Manager | Pastor | Helper | Admin |
|---------|-----------------|--------|--------|-------|
| **Service Assignment** | None (works across all services) | Single service | Single service | None |
| **Campaign Access** | Only assigned campaigns | All campaigns | All campaigns | All campaigns |
| **Submission Viewing** | Only assigned campaigns | All (their service) | All (their service) | All |
| **Submission Creation** | Only assigned campaigns | Any campaign | Any campaign | Any campaign |
| **Cross-Service** | ✅ Yes | ❌ No | ❌ No | ✅ Yes |
| **Multiple Campaigns** | ✅ Yes | ❌ No | ❌ No | ✅ Yes |
| **Password** | Auto-generated | User-provided | User-provided | User-provided |

---

## Use Cases

### 1. **Centralized Campaign Management**
A Campaign Manager can be assigned to manage "Soul Winning Initiative" across all church services, collecting data from multiple locations.

### 2. **Specialized Campaign Focus**
Assign a Campaign Manager to a specific campaign type (e.g., "Technology Campaign") to ensure consistent data collection across all services.

### 3. **Multi-Campaign Coordination**
A single Campaign Manager can handle multiple related campaigns, providing a unified view and management approach.

### 4. **Temporary Campaign Management**
Assign Campaign Managers to time-bound campaigns without creating permanent service assignments.

---

## Getting Campaign Names

To assign campaigns, you need to know the exact campaign names. You can get them from:

### Option 1: List All Campaigns (Admin/Pastor/Helper)
```bash
GET /api/campaigns/all/
```

### Option 2: Check Database
Query the campaign models directly in Django admin or database.

### Option 3: Check Existing Campaign Manager
View an existing Campaign Manager's assigned campaigns to see campaign names.

---

## Best Practices

### 1. **Campaign Name Accuracy**
- Use exact campaign names (case-insensitive)
- Verify campaign names before assignment
- Check for typos in campaign names

### 2. **Multiple Assignments**
- Assign multiple campaigns in a single request for efficiency
- Use JSON string format for `campaign_assignments`

### 3. **Password Security**
- Campaign Managers should change password after first login
- Use strong passwords when changing
- Never share passwords

### 4. **Assignment Management**
- Regularly review campaign assignments
- Remove assignments when campaigns end
- Add new assignments as needed

### 5. **Service Selection**
- Campaign Managers can submit for any service
- Ensure they select the correct service when creating submissions
- Service field is optional but recommended for data organization

---

## Error Handling

### Common Errors

#### 1. Campaign Not Found
```json
{
  "status": 400,
  "data": {
    "campaign_assignments": [
      "Campaign 'Invalid Campaign Name' not found."
    ]
  }
}
```
**Solution**: Verify the campaign name exists and is spelled correctly.

#### 2. Not Assigned to Campaign
```json
{
  "campaign": ["You are not assigned to this campaign."]
}
```
**Solution**: Ensure the Campaign Manager is assigned to the campaign before creating submissions.

#### 3. Missing Required Fields
```json
{
  "status": 400,
  "data": {
    "first_name": ["This field is required."],
    "campaign_assignments": ["This field is required."]
  }
}
```
**Solution**: Provide all required fields in the request.

---

## Analytics

### Endpoint

**GET** `/api/users/analytics/`

### Description

Campaign Managers get a **simplified analytics view** showing only their submissions, totals over time, and basic data for assigned campaigns.

### Query Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| `period` | string | Time period: `week`, `month`, `quarter`, `year`, `all` | `month` |
| `start_date` | date | Custom start date (YYYY-MM-DD) | None |
| `end_date` | date | Custom end date (YYYY-MM-DD) | None |

### Response Structure

```json
{
  "user": {
    "id": 10,
    "username": "johndoe",
    "full_name": "John Doe",
    "role": "CAMPAIGN_MANAGER"
  },
  "period": {
    "type": "month",
    "start": "2025-11-01T00:00:00Z",
    "end": "2025-11-30T23:59:59Z"
  },
  "summary": {
    "total_submissions_all_time": 45,
    "total_submissions_this_period": 8,
    "assigned_campaigns_count": 3,
    "total_campaigns_assigned": 3
  },
  "submissions_by_type": {
    "State of the Flock": {
      "all_time": 12,
      "this_period": 2
    },
    "Soul Winning": {
      "all_time": 15,
      "this_period": 3
    },
    "Technology": {
      "all_time": 18,
      "this_period": 3
    }
  },
  "submissions_over_time": [
    {
      "period": "2025-09",
      "label": "Sep 2025",
      "count": 5
    },
    {
      "period": "2025-10",
      "label": "Oct 2025",
      "count": 7
    },
    {
      "period": "2025-11",
      "label": "Nov 2025",
      "count": 8
    }
  ],
  "recent_submissions": [
    {
      "id": 150,
      "campaign_name": "State of the Flock 2025",
      "campaign_type": "State of the Flock",
      "service_name": "Downtown Church",
      "submission_period": "2025-11-01",
      "date": null,
      "created_at": "2025-11-10T14:30:00Z"
    }
  ],
  "chart_data": {
    "labels": ["Sep 2025", "Oct 2025", "Nov 2025"],
    "data": [5, 7, 8],
    "color": "#2196F3"
  }
}
```

### Response Fields

| Field | Type | Description |
|-------|------|-------------|
| `user` | object | User information |
| `period` | object | Time period information |
| `summary` | object | Summary statistics |
| `summary.total_submissions_all_time` | integer | Total submissions across all time |
| `summary.total_submissions_this_period` | integer | Total submissions in selected period |
| `summary.assigned_campaigns_count` | integer | Number of campaign types assigned |
| `summary.total_campaigns_assigned` | integer | Total number of campaigns assigned |
| `submissions_by_type` | object | Submissions grouped by campaign type |
| `submissions_over_time` | array | Submissions over time (last 12 months) |
| `recent_submissions` | array | Last 10 submissions |
| `chart_data` | object | Chart data for visualization |

### Key Features

1. **Only Their Submissions**
   - Shows only submissions created by the Campaign Manager
   - Filtered to assigned campaigns only

2. **Totals Over Time**
   - Total submissions all time
   - Total submissions for selected period
   - Submissions over time (last 12 months)

3. **Basic Data**
   - Submissions by campaign type
   - Recent submissions list
   - Assigned campaigns count

4. **Chart Data**
   - Ready-to-use chart data for visualization
   - Labels and data points for line/bar charts

### Example Request

```bash
curl -X GET "http://localhost:8000/api/users/analytics/?period=month" \
  -H "Authorization: Bearer <campaign_manager_token>"
```

### Example Response

```json
{
  "user": {
    "id": 10,
    "username": "johndoe",
    "full_name": "John Doe",
    "role": "CAMPAIGN_MANAGER"
  },
  "period": {
    "type": "month",
    "start": "2025-11-01T00:00:00Z",
    "end": "2025-11-30T23:59:59Z"
  },
  "summary": {
    "total_submissions_all_time": 45,
    "total_submissions_this_period": 8,
    "assigned_campaigns_count": 3,
    "total_campaigns_assigned": 3
  },
  "submissions_by_type": {
    "State of the Flock": {
      "all_time": 12,
      "this_period": 2
    },
    "Soul Winning": {
      "all_time": 15,
      "this_period": 3
    },
    "Technology": {
      "all_time": 18,
      "this_period": 3
    }
  },
  "submissions_over_time": [
    {
      "period": "2025-09",
      "label": "Sep 2025",
      "count": 5
    },
    {
      "period": "2025-10",
      "label": "Oct 2025",
      "count": 7
    },
    {
      "period": "2025-11",
      "label": "Nov 2025",
      "count": 8
    }
  ],
  "recent_submissions": [
    {
      "id": 150,
      "campaign_name": "State of the Flock 2025",
      "campaign_type": "State of the Flock",
      "service_name": "Downtown Church",
      "submission_period": "2025-11-01",
      "date": null,
      "created_at": "2025-11-10T14:30:00Z"
    }
  ],
  "chart_data": {
    "labels": ["Sep 2025", "Oct 2025", "Nov 2025"],
    "data": [5, 7, 8],
    "color": "#2196F3"
  }
}
```

---

## API Endpoints Summary

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/users/create-campaign-manager/` | POST | Create a new Campaign Manager |
| `/api/users/dashboard/` | GET | Get Campaign Manager dashboard |
| `/api/users/analytics/` | GET | Get simplified analytics (only their submissions) |
| `/api/campaigns/all/` | GET | List campaigns (filtered for Campaign Managers) |
| `/api/campaigns/*/submissions/` | GET | List submissions (filtered for Campaign Managers) |
| `/api/campaigns/*/submissions/` | POST | Create submission (validated for Campaign Managers) |

---

## Technical Details

### Database Model

**CampaignManagerAssignment:**
```python
class CampaignManagerAssignment(models.Model):
    user = ForeignKey(CustomerUser)
    content_type = ForeignKey(ContentType)
    object_id = PositiveIntegerField()
    campaign = GenericForeignKey('content_type', 'object_id')
```

### User Role

Campaign Managers have `role = 'CAMPAIGN_MANAGER'` in the `CustomerUser` model.

### Filtering Logic

- Uses `ContentType` and `GenericForeignKey` for flexible campaign assignment
- Filters applied at queryset level for security
- Validation in `perform_create()` prevents unauthorized submissions

---

## Examples

### Example 1: Create Campaign Manager with Single Campaign

```bash
curl -X POST http://localhost:8000/api/users/create-campaign-manager/ \
  -H "Authorization: Bearer <admin_token>" \
  -H "Content-Type: multipart/form-data" \
  -F "first_name=John" \
  -F "last_name=Doe" \
  -F "username=johndoe" \
  -F "email=john@example.com" \
  -F "phone_number=+1234567890" \
  -F "campaign_assignments=[{\"campaign_name\": \"State of the Flock 2025\"}]"
```

### Example 2: Create Campaign Manager with Multiple Campaigns

```bash
curl -X POST http://localhost:8000/api/users/create-campaign-manager/ \
  -H "Authorization: Bearer <admin_token>" \
  -H "Content-Type: multipart/form-data" \
  -F "first_name=Jane" \
  -F "last_name=Smith" \
  -F "username=janesmith" \
  -F "email=jane@example.com" \
  -F "phone_number=+1234567891" \
  -F "campaign_assignments=[{\"campaign_name\": \"Soul Winning Initiative\"}, {\"campaign_name\": \"Technology Campaign\"}]"
```

### Example 3: Campaign Manager Viewing Dashboard

```bash
curl -X GET http://localhost:8000/api/users/dashboard/ \
  -H "Authorization: Bearer <campaign_manager_token>"
```

### Example 4: Campaign Manager Creating Submission

```bash
curl -X POST http://localhost:8000/api/campaigns/soul-winning/submissions/ \
  -H "Authorization: Bearer <campaign_manager_token>" \
  -H "Content-Type: multipart/form-data" \
  -F "campaign=5" \
  -F "submission_period=2025-11-01" \
  -F "date=2025-11-10" \
  -F "no_of_crusades=3" \
  -F "no_of_massive_organised_outreaches=2"
```

---

## Summary

Campaign Managers provide a flexible, cross-service approach to campaign management:

- ✅ **Multi-campaign assignment** - Manage multiple campaigns
- ✅ **Cross-service access** - Work across all services
- ✅ **Restricted visibility** - Only see assigned campaigns
- ✅ **Secure filtering** - Automatic filtering at API level
- ✅ **Customized dashboard** - Specialized view for managers
- ✅ **Easy creation** - Simple API endpoint with campaign name-based assignment

Perfect for organizations that need centralized campaign management across multiple services! 🎉

