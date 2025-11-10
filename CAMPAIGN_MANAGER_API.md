# Campaign Manager API Documentation

## Overview

Campaign Managers are special users who can be assigned to one or more campaigns. They have limited access to only submit data for their assigned campaigns **across ALL services**.

**Important:** Campaign Managers are **NOT assigned to a specific service**. They work across all services and can submit data for any service for their assigned campaigns.

---

## Create Campaign Manager

**Endpoint:** `POST /api/users/create-campaign-manager/`

**Authentication:** Required

**Description:** Create a new Campaign Manager user and assign one or more campaigns to them.

**Note:** Campaign Managers are NOT assigned to a service. They can submit data for their assigned campaigns across ALL services.

### Request Body

```json
{
  "first_name": "John",
  "last_name": "Doe",
  "username": "johndoe",
  "email": "john@example.com",
  "phone_number": "+1234567890",
  "campaign_assignments": [
    {"campaign_name": "State of the Flock 2025"},
    {"campaign_name": "Soul Winning Initiative"},
    {"campaign_name": "Technology Upgrade"}
  ]
}
```

**Notes:** 
- Password is auto-generated (default: "kelvin") and is NOT included in the request
- Just provide campaign names - the system auto-detects the campaign type!
- Campaign names are case-insensitive

### Request Fields

#### Required Fields

| Field | Type | Description |
|-------|------|-------------|
| `first_name` | string | Campaign manager's first name |
| `last_name` | string | Campaign manager's last name |
| `username` | string | Unique username for login |
| `email` | string | Unique email address |
| `phone_number` | string | Unique phone number |
| `campaign_assignments` | array | List of campaign assignments (minimum 1 required) |

**Password Note:** Password is auto-generated (default: "kelvin") and should NOT be included in the request. It works the same way as for Pastor and Helper roles.

#### Campaign Assignment Object

Each object in `campaign_assignments` array must contain:

| Field | Type | Description |
|-------|------|-------------|
| `campaign_name` | string | Name of the campaign (case-insensitive, system auto-detects campaign type) |

**Note:** You no longer need to specify `campaign_type` - the system automatically determines which campaign type the name belongs to! Campaign names are matched case-insensitively.

#### Optional Fields

| Field | Type | Description |
|-------|------|-------------|
| `profile_picture` | file | Profile picture (multipart/form-data) |

**Note:** There is NO `service` field. Campaign Managers are not assigned to a specific service and can work across all services.

### How to Get Campaign Names

To get the names of available campaigns, query the campaign endpoints:

- `GET /api/campaigns/state-of-the-flock/` - State of the Flock campaigns
- `GET /api/campaigns/soul-winning/` - Soul Winning campaigns
- `GET /api/campaigns/servants-armed-trained/` - Servants Armed campaigns
- `GET /api/campaigns/antibrutish/` - Antibrutish campaigns
- `GET /api/campaigns/hearing-seeing/` - Hearing and Seeing campaigns
- `GET /api/campaigns/honour-your-prophet/` - Honour Your Prophet campaigns
- `GET /api/campaigns/basonta-proliferation/` - Basonta Proliferation campaigns
- `GET /api/campaigns/intimate-counseling/` - Intimate Counseling campaigns
- `GET /api/campaigns/technology/` - Technology campaigns
- `GET /api/campaigns/sheperding-control/` - Sheperding Control campaigns
- `GET /api/campaigns/multiplication/` - Multiplication campaigns
- `GET /api/campaigns/understanding/` - Understanding campaigns
- `GET /api/campaigns/sheep-seeking/` - Sheep Seeking campaigns
- `GET /api/campaigns/testimony/` - Testimony campaigns
- `GET /api/campaigns/telepastoring/` - Telepastoring campaigns
- `GET /api/campaigns/gathering-bus/` - Gathering Bus campaigns
- `GET /api/campaigns/organised-creative-arts/` - Organised Creative Arts campaigns
- `GET /api/campaigns/tangerine/` - Tangerine campaigns
- `GET /api/campaigns/swollen-sunday/` - Swollen Sunday campaigns
- `GET /api/campaigns/sunday-management/` - Sunday Management campaigns

Each endpoint returns campaigns with their `name` field - use these names in the `campaign_assignments` array. Campaign names are case-insensitive, so "State of the Flock 2025" and "state of the flock 2025" are treated the same.

### Response

**Status Code:** `201 Created`

```json
{
  "id": 10,
  "first_name": "John",
  "last_name": "Doe",
  "username": "johndoe",
  "email": "john@example.com",
  "phone_number": "+1234567890",
  "assigned_campaigns": [
    {
      "id": 1,
      "campaign_type": "StateOfTheFlockCampaign",
      "campaign_id": 1,
      "campaign_name": "State of the Flock 2025",
      "created_at": "2025-11-10T10:30:00Z"
    },
    {
      "id": 2,
      "campaign_type": "SoulWinningCampaign",
      "campaign_id": 1,
      "campaign_name": "Soul Winning Initiative",
      "created_at": "2025-11-10T10:30:00Z"
    }
  ],
  "created_at": "2025-11-10T10:30:00Z"
}
```

### Error Responses

#### 400 Bad Request - Missing Required Fields

```json
{
  "first_name": ["This field is required."],
  "campaign_assignments": ["This field is required."]
}
```

#### 400 Bad Request - Campaign Does Not Exist

```json
{
  "campaign_assignments": [
    "Campaign with name 'Non Existent Campaign' does not exist in any campaign type."
  ]
}
```

#### 400 Bad Request - Username Already Exists

```json
{
  "username": ["A user with that username already exists."]
}
```

#### 400 Bad Request - Email Already Exists

```json
{
  "email": ["customer user with this email already exists."]
}
```

---

## How Campaign Managers Work

### User Role

Campaign Managers are created with the role `CAMPAIGN_MANAGER`. This role:
- Is automatically assigned during creation via the endpoint
- Cannot be changed to another role through normal user update endpoints
- Has specific permissions tailored for campaign data entry

### Campaign Assignments

- A Campaign Manager can be assigned to **one or more campaigns**
- Each assignment links the manager to a specific campaign instance
- Assignments are permanent until deleted by an admin
- Campaign Managers can only view and submit data for their assigned campaigns

### Permissions

Campaign Managers can:
- Submit data for their assigned campaigns **across ALL services**
- View submissions for their assigned campaigns
- Work with any service/church location for their assigned campaigns

Campaign Managers cannot:
- View or modify campaigns they're not assigned to
- Access admin functions
- Create or delete campaigns
- Modify other users

**Key Feature:** Campaign Managers are NOT tied to a specific service. They have access to submit data for their assigned campaigns regardless of which service the submission is for.

---

## Database Schema

### CampaignManagerAssignment Model

The `CampaignManagerAssignment` model tracks which campaigns a manager is assigned to:

| Field | Type | Description |
|-------|------|-------------|
| `id` | integer | Primary key |
| `user` | ForeignKey | Reference to Campaign Manager user |
| `content_type` | ForeignKey | Campaign type (Django ContentType) |
| `object_id` | integer | ID of specific campaign |
| `campaign` | GenericForeignKey | Generic link to any campaign |
| `created_at` | datetime | Assignment creation timestamp |
| `updated_at` | datetime | Last update timestamp |

**Unique Constraint:** A user cannot be assigned to the same campaign twice (`user`, `content_type`, `object_id` must be unique together).

---

## Usage Examples

### Example 1: Create Manager for Single Campaign

```bash
curl -X POST http://localhost:8000/api/users/create-campaign-manager/ \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "Jane",
    "last_name": "Smith",
    "username": "janesmith",
    "email": "jane@example.com",
    "phone_number": "+1234567891",
    "campaign_assignments": [
      {"campaign_name": "State of the Flock 2025"}
    ]
  }'
```

**Note:** Just provide the campaign name - system auto-detects the campaign type!

### Example 2: Create Manager for Multiple Campaigns

```bash
curl -X POST http://localhost:8000/api/users/create-campaign-manager/ \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "Bob",
    "last_name": "Johnson",
    "username": "bobjohnson",
    "email": "bob@example.com",
    "phone_number": "+1234567892",
    "campaign_assignments": [
      {"campaign_name": "State of the Flock 2025"},
      {"campaign_name": "Soul Winning Initiative"},
      {"campaign_name": "Technology Upgrade"}
    ]
  }'
```

**Note:** Simple and clean - just provide campaign names!

### Example 3: Create Manager with Profile Picture (Multipart)

When sending a profile picture, you must use `multipart/form-data` format. The `campaign_assignments` should be sent as a JSON string:

```bash
curl -X POST http://localhost:8000/api/users/create-campaign-manager/ \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -F "first_name=Alice" \
  -F "last_name=Williams" \
  -F "username=alicewilliams" \
  -F "email=alice@example.com" \
  -F "phone_number=+1234567893" \
  -F "profile_picture=@/path/to/photo.jpg" \
  -F 'campaign_assignments=[{"campaign_name":"Technology Upgrade"},{"campaign_name":"Soul Winning Initiative"}]'
```

**Important Notes for Multipart:**
- Send `campaign_assignments` as a JSON string (it will be automatically parsed)
- Make sure the JSON is valid
- Campaign names work the same way (case-insensitive)

**Frontend Example (JavaScript/FormData):**
```javascript
const formData = new FormData();
formData.append('first_name', 'Alice');
formData.append('last_name', 'Williams');
formData.append('username', 'alicewilliams');
formData.append('email', 'alice@example.com');
formData.append('phone_number', '+1234567893');
formData.append('profile_picture', fileInput.files[0]);

// Important: Stringify the campaign assignments array
const assignments = [
  {campaign_name: "Technology Upgrade"},
  {campaign_name: "Soul Winning Initiative"}
];
formData.append('campaign_assignments', JSON.stringify(assignments));

await fetch('/api/users/create-campaign-manager/', {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${token}`
    // Don't set Content-Type - browser will set it with boundary
  },
  body: formData
});
```

---

## Best Practices

1. **Password Management**: Passwords are auto-generated (default: "kelvin"). Campaign Managers should change their password after first login using the change password endpoint.

2. **Unique Identifiers**: Ensure username, email, and phone_number are unique across all users.

3. **No Service Assignment**: Campaign Managers are deliberately NOT assigned to a service. They work across all services.

4. **Campaign Validation**: Always verify that the campaign IDs exist before attempting to create assignments.

5. **Multiple Assignments**: Assign multiple campaigns at creation time rather than making multiple API calls.

6. **Cross-Service Access**: Remember that Campaign Managers can submit data for their campaigns at ANY service location.

---

## Admin Management

Campaign Manager assignments can also be managed via the Django Admin interface at `/admin/campaigns/campaignmanagerassignment/`.

Admin features:
- View all campaign manager assignments
- Create, edit, and delete assignments
- Filter by campaign type, user, and creation date
- Search by user name, username, and email

---

## Related Endpoints

- **List All Users**: `GET /api/users/` (includes campaign managers)
- **Get User Profile**: `GET /api/users/get_profile/`
- **Update User**: `PUT/PATCH /api/users/{id}/`
- **Delete User**: `DELETE /api/users/{id}/` (deletes associated assignments)

---

## Notes

- Campaign Managers are created with `role='CAMPAIGN_MANAGER'` automatically
- Password is auto-generated (default: "kelvin"), same as Pastor/Helper roles
- Campaign Managers should change their password after first login
- Deleting a Campaign Manager user will cascade delete all their campaign assignments
- Campaign assignments use Django's ContentType framework to support all 20 campaign types

