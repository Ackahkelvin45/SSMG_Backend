# Change Log: Campaign Manager Update & Delete Functionality

**Date:** November 10, 2025  
**Feature:** Added update and delete endpoints for Campaign Manager users

---

## Summary

Implemented full CRUD operations for Campaign Manager users. Campaign Managers can now be updated (info and campaign assignments) and deleted through dedicated API endpoints.

---

## Changes Made

### 1. New Serializer (`authentication/serializers.py`)

#### Added `CampaignManagerUpdateSerializer`:
```python
class CampaignManagerUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for updating Campaign Manager users.
    Allows updating basic info and campaign assignments.
    
    Note: 
    - Cannot change role (must remain CAMPAIGN_MANAGER)
    - Cannot assign a service (Campaign Managers work across all services)
    - Can update campaign assignments (add/remove campaigns)
    """
    profile_picture = serializers.ImageField(...)
    campaign_assignments = serializers.CharField(...)  # Accept as string for multipart
    assigned_campaigns = serializers.SerializerMethodField(read_only=True)
    
    # Update logic:
    # 1. Update basic user fields
    # 2. Handle profile picture
    # 3. Delete existing campaign assignments
    # 4. Create new campaign assignments
```

**Key Features:**
- Supports both JSON and multipart/form-data
- Validates campaign names across all campaign types
- Username is read-only (cannot be changed)
- Completely replaces campaign assignments (not incremental)
- Returns updated user with assigned campaigns

### 2. New Endpoints (`authentication/views.py`)

#### Update Campaign Manager Endpoint:
```python
@action(detail=True, methods=['put', 'patch'], url_path='update-campaign-manager')
def update_campaign_manager(self, request, pk=None):
    """
    Update a Campaign Manager user and their campaign assignments.
    
    PUT: Full update (all fields required)
    PATCH: Partial update (only include fields to change)
    """
```

**URL:** `PUT/PATCH /api/auth/users/{id}/update-campaign-manager/`

**Allowed Updates:**
- `first_name`, `last_name`, `email`, `phone_number`
- `profile_picture`
- `campaign_assignments` (replaces all existing)

**Not Allowed:**
- `username` (read-only)
- `role` (must remain CAMPAIGN_MANAGER)
- `service` (Campaign Managers have no service)

#### Delete Campaign Manager Endpoint:
```python
@action(detail=True, methods=['delete'], url_path='delete-campaign-manager')
def delete_campaign_manager(self, request, pk=None):
    """
    Delete a Campaign Manager user.
    
    This will:
    1. Delete all campaign assignments for this user
    2. Delete all submissions made by this user
    3. Delete the user account
    
    Warning: This action cannot be undone!
    """
```

**URL:** `DELETE /api/auth/users/{id}/delete-campaign-manager/`

**What Gets Deleted:**
1. User account
2. All `CampaignManagerAssignment` records
3. All submissions made by this user (cascade)
4. Profile picture file

### 3. Import Updates (`authentication/views.py`)

Added `CampaignManagerUpdateSerializer` to imports:
```python
from .serializers import (
    UserSerializer,
    UserCreateSerializer,
    UserUpdateSerializer,
    ServiceSerializer,
    ServiceCreateSerializer,
    ChangePasswordSerializer,
    CampaignManagerCreateSerializer,
    CampaignManagerUpdateSerializer,  # NEW
    CustomTokenObtainPairSerializer
)
```

---

## API Examples

### Update Campaign Manager (JSON)

**Request:**
```http
PATCH /api/auth/users/15/update-campaign-manager/
Content-Type: application/json
Authorization: Bearer YOUR_ACCESS_TOKEN

{
  "email": "newemail@example.com",
  "phone_number": "+9999999999",
  "campaign_assignments": [
    {"campaign_name": "Technology Campaign"},
    {"campaign_name": "Equipment Campaign"}
  ]
}
```

**Response:**
```json
{
  "id": 15,
  "first_name": "Jane",
  "last_name": "Doe",
  "username": "janecm",
  "email": "newemail@example.com",
  "phone_number": "+9999999999",
  "assigned_campaigns": [
    {
      "id": 45,
      "campaign_type": "TechnologyCampaign",
      "campaign_id": 3,
      "campaign_name": "Technology Campaign",
      "created_at": "2025-11-10T12:30:00Z"
    },
    {
      "id": 46,
      "campaign_type": "EquipmentCampaign",
      "campaign_id": 21,
      "campaign_name": "Equipment Campaign",
      "created_at": "2025-11-10T12:30:00Z"
    }
  ],
  "updated_at": "2025-11-10T12:45:00Z"
}
```

### Update Campaign Manager (Multipart with Profile Picture)

**Request:**
```http
PATCH /api/auth/users/15/update-campaign-manager/
Content-Type: multipart/form-data
Authorization: Bearer YOUR_ACCESS_TOKEN

first_name: Jane
last_name: Doe Updated
email: jane@example.com
phone_number: +1234567890
profile_picture: (binary file)
campaign_assignments: [{"campaign_name":"State of the Flock 2025"}]
```

### Delete Campaign Manager

**Request:**
```http
DELETE /api/auth/users/15/delete-campaign-manager/
Authorization: Bearer YOUR_ACCESS_TOKEN
```

**Response:**
```json
{
  "message": "Campaign Manager 'janecm' has been successfully deleted."
}
```

---

## Campaign Assignments Behavior

### Important: Replace, Not Merge!

When updating `campaign_assignments`, it **completely replaces** all existing assignments. This is not an incremental update.

#### Example: Adding a Campaign
```javascript
// Current: ["Campaign A", "Campaign B"]
// To add "Campaign C", send ALL campaigns:
{
  "campaign_assignments": [
    {"campaign_name": "Campaign A"},     // Keep
    {"campaign_name": "Campaign B"},     // Keep
    {"campaign_name": "Campaign C"}      // Add
  ]
}
```

#### Example: Removing a Campaign
```javascript
// Current: ["Campaign A", "Campaign B", "Campaign C"]
// To remove "Campaign B", send only campaigns to keep:
{
  "campaign_assignments": [
    {"campaign_name": "Campaign A"},
    {"campaign_name": "Campaign C"}
  ]
}
```

#### Example: Replacing All Campaigns
```javascript
// Current: ["Campaign A", "Campaign B"]
// To completely replace:
{
  "campaign_assignments": [
    {"campaign_name": "Campaign X"},
    {"campaign_name": "Campaign Y"}
  ]
}
```

---

## Frontend Integration

### React - Update Hook

```typescript
const useUpdateCampaignManager = () => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const updateCampaignManager = async (
    userId: number,
    data: UpdateCampaignManagerData,
    accessToken: string
  ) => {
    setLoading(true);
    setError(null);

    try {
      const response = await axios.patch(
        `/api/auth/users/${userId}/update-campaign-manager/`,
        data,
        {
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${accessToken}`
          }
        }
      );
      return response.data;
    } catch (err: any) {
      const errorMessage = err.response?.data?.detail || 'Update failed';
      setError(errorMessage);
      throw new Error(errorMessage);
    } finally {
      setLoading(false);
    }
  };

  return { updateCampaignManager, loading, error };
};
```

### React - Delete Hook

```typescript
const useDeleteCampaignManager = () => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const deleteCampaignManager = async (
    userId: number,
    accessToken: string
  ) => {
    setLoading(true);
    setError(null);

    try {
      await axios.delete(
        `/api/auth/users/${userId}/delete-campaign-manager/`,
        {
          headers: {
            'Authorization': `Bearer ${accessToken}`
          }
        }
      );
    } catch (err: any) {
      const errorMessage = err.response?.data?.detail || 'Delete failed';
      setError(errorMessage);
      throw new Error(errorMessage);
    } finally {
      setLoading(false);
    }
  };

  return { deleteCampaignManager, loading, error };
};
```

### Usage Example

```tsx
const CampaignManagerEditForm = ({ userId, currentData }) => {
  const { updateCampaignManager, loading } = useUpdateCampaignManager();
  const navigate = useNavigate();

  const handleSubmit = async (formData) => {
    try {
      const result = await updateCampaignManager(
        userId,
        formData,
        localStorage.getItem('accessToken')
      );
      alert('Campaign Manager updated successfully!');
      navigate('/campaign-managers');
    } catch (error) {
      alert('Update failed: ' + error.message);
    }
  };

  return <Form onSubmit={handleSubmit} initialData={currentData} />;
};

const CampaignManagerList = () => {
  const { deleteCampaignManager } = useDeleteCampaignManager();

  const handleDelete = async (userId: number) => {
    const confirmed = window.confirm(
      'Are you sure? This cannot be undone!'
    );
    
    if (!confirmed) return;

    try {
      await deleteCampaignManager(
        userId,
        localStorage.getItem('accessToken')
      );
      alert('Campaign Manager deleted successfully!');
      // Refresh list
    } catch (error) {
      alert('Delete failed: ' + error.message);
    }
  };

  return <Table onDelete={handleDelete} />;
};
```

---

## Validation Rules

### Update Validation

1. **Email:** Must be unique across all users
2. **Phone Number:** Must be unique across all users
3. **Username:** Cannot be changed (read-only)
4. **Campaign Assignments:** Must be valid campaign names (case-insensitive)
5. **Profile Picture:** Must be a valid image file
6. **User Role:** Must be a Campaign Manager (endpoint validates this)

### Delete Validation

1. **User Role:** Must be a Campaign Manager
2. **User Existence:** User must exist

---

## Error Responses

### 400 Bad Request - Not a Campaign Manager
```json
{
  "error": "This endpoint is only for Campaign Manager users."
}
```

### 400 Bad Request - Validation Error
```json
{
  "email": ["user with this email already exists."],
  "campaign_assignments": [
    "Campaign with name 'Invalid Campaign' does not exist in any campaign type."
  ]
}
```

### 404 Not Found
```json
{
  "detail": "Not found."
}
```

---

## Breaking Changes

### ⚠️ None

This is a new feature with no breaking changes to existing APIs.

---

## Testing Checklist

- [ ] Create a Campaign Manager
- [ ] Update Campaign Manager email (PATCH)
- [ ] Update Campaign Manager phone number (PATCH)
- [ ] Update Campaign Manager with profile picture (multipart)
- [ ] Update Campaign Manager campaign assignments
- [ ] Add a campaign to existing assignments
- [ ] Remove a campaign from existing assignments
- [ ] Replace all campaign assignments
- [ ] Try to update non-Campaign Manager user (should fail)
- [ ] Try to change username (should be ignored/fail)
- [ ] Delete a Campaign Manager
- [ ] Verify cascade deletion of assignments
- [ ] Verify cascade deletion of submissions
- [ ] Try to delete non-Campaign Manager user (should fail)

---

## Database Impact

### On Update:
1. User record is updated in `authentication_customeruser`
2. Old assignments are deleted from `campaigns_campaignmanagerassignment`
3. New assignments are created in `campaigns_campaignmanagerassignment`

### On Delete:
1. Assignments deleted from `campaigns_campaignmanagerassignment` (CASCADE)
2. Submissions deleted from all submission tables (CASCADE)
3. User deleted from `authentication_customeruser`
4. Profile picture file deleted from media storage

---

## Security Considerations

1. **Role Verification:** Endpoints verify user is a Campaign Manager
2. **Authentication Required:** Both endpoints require valid JWT token
3. **Cascade Deletion:** Ensures no orphaned records
4. **Unique Constraints:** Email and phone number remain unique
5. **Username Protection:** Username cannot be changed (prevents identity confusion)

---

## Performance Notes

- **Update:** O(n) where n = number of campaigns being assigned
- **Delete:** O(m) where m = total number of related records (assignments + submissions)
- **Campaign Search:** Searches across all campaign models (20+ models)
- **Consider Indexing:** `CampaignManagerAssignment.user` for faster lookups

---

## Documentation

Full API documentation: [`CAMPAIGN_MANAGER_UPDATE_DELETE_API.md`](./CAMPAIGN_MANAGER_UPDATE_DELETE_API.md)

Includes:
- Detailed endpoint specifications
- Request/response examples
- Frontend integration examples (React, React Native)
- Error handling strategies
- Use case examples

---

## Future Enhancements

1. **Incremental Campaign Updates:** Support adding/removing individual campaigns without full replacement
2. **Bulk Operations:** Update multiple Campaign Managers at once
3. **Soft Delete:** Add `is_deleted` flag instead of hard delete
4. **Audit Trail:** Log all updates and deletions
5. **Notification:** Email Campaign Manager when assignments change

---

**Status:** ✅ Deployed  
**Version:** 2.3.0  
**Endpoints:**
- `PUT/PATCH /api/auth/users/{id}/update-campaign-manager/`
- `DELETE /api/auth/users/{id}/delete-campaign-manager/`


