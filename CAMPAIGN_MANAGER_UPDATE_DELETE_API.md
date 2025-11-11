# Campaign Manager Update & Delete API

## Overview

This document describes the API endpoints for updating and deleting Campaign Manager users.

---

## Endpoints

### 1. Update Campaign Manager

**PUT/PATCH** `/api/auth/users/{id}/update-campaign-manager/`

Updates a Campaign Manager's information and campaign assignments.

---

## Update Campaign Manager

### Endpoint
```
PUT /api/auth/users/{id}/update-campaign-manager/
PATCH /api/auth/users/{id}/update-campaign-manager/
```

- **PUT:** Full update (all fields required except `campaign_assignments`)
- **PATCH:** Partial update (only include fields to change)

### Headers
```
Content-Type: application/json
Authorization: Bearer <access_token>
```

### URL Parameters
| Parameter | Type | Description |
|-----------|------|-------------|
| `id` | integer | Campaign Manager user ID |

### Request Body (JSON)

#### Full Update (PUT)
```json
{
  "first_name": "Jane",
  "last_name": "Doe Updated",
  "email": "jane.updated@example.com",
  "phone_number": "+9876543210",
  "campaign_assignments": [
    {"campaign_name": "State of the Flock 2025"},
    {"campaign_name": "Soul Winning Initiative"},
    {"campaign_name": "Equipment Campaign"}
  ]
}
```

#### Partial Update (PATCH)
```json
{
  "email": "newemail@example.com",
  "phone_number": "+1111111111"
}
```

#### Update Only Campaign Assignments
```json
{
  "campaign_assignments": [
    {"campaign_name": "Technology Campaign"},
    {"campaign_name": "Testimony Campaign"}
  ]
}
```

#### Update with Profile Picture (multipart/form-data)
```
Content-Type: multipart/form-data

first_name: Jane
last_name: Doe Updated
email: jane.updated@example.com
phone_number: +9876543210
profile_picture: (binary file)
campaign_assignments: [{"campaign_name":"State of the Flock 2025"}]
```

### Request Fields

| Field | Type | Required (PUT) | Required (PATCH) | Description |
|-------|------|----------------|------------------|-------------|
| `first_name` | string | Yes | No | First name |
| `last_name` | string | Yes | No | Last name |
| `email` | string | Yes | No | Email address (must be unique) |
| `phone_number` | string | Yes | No | Phone number (must be unique) |
| `profile_picture` | file | No | No | Profile picture (image file) |
| `campaign_assignments` | array | No | No | List of campaign assignments (replaces all existing) |

**Note:** 
- `username` is **read-only** and cannot be changed
- `role` cannot be changed (must remain `CAMPAIGN_MANAGER`)
- `service` cannot be assigned (Campaign Managers work across all services)

### Response (200 OK)

```json
{
  "id": 15,
  "first_name": "Jane",
  "last_name": "Doe Updated",
  "username": "janecm",
  "email": "jane.updated@example.com",
  "phone_number": "+9876543210",
  "assigned_campaigns": [
    {
      "id": 45,
      "campaign_type": "StateOfTheFlockCampaign",
      "campaign_id": 1,
      "campaign_name": "State of the Flock 2025",
      "created_at": "2025-11-10T10:30:00Z"
    },
    {
      "id": 46,
      "campaign_type": "SoulWinningCampaign",
      "campaign_id": 2,
      "campaign_name": "Soul Winning Initiative",
      "created_at": "2025-11-10T10:30:00Z"
    }
  ],
  "updated_at": "2025-11-10T12:45:00Z"
}
```

### Error Responses

#### 400 Bad Request - Not a Campaign Manager
```json
{
  "error": "This endpoint is only for Campaign Manager users."
}
```

#### 400 Bad Request - Validation Error
```json
{
  "email": ["This field is required."],
  "campaign_assignments": [
    "Campaign with name 'Invalid Campaign' does not exist in any campaign type."
  ]
}
```

#### 404 Not Found
```json
{
  "detail": "Not found."
}
```

---

## Delete Campaign Manager

### Endpoint
```
DELETE /api/auth/users/{id}/delete-campaign-manager/
```

Permanently deletes a Campaign Manager and all their associated data.

### Headers
```
Authorization: Bearer <access_token>
```

### URL Parameters
| Parameter | Type | Description |
|-----------|------|-------------|
| `id` | integer | Campaign Manager user ID |

### Request Body
None required.

### What Gets Deleted

1. **User account** - Campaign Manager user
2. **Campaign assignments** - All `CampaignManagerAssignment` records
3. **Submissions** - All submissions made by this Campaign Manager
4. **Profile picture** - Uploaded profile picture (if any)

**⚠️ Warning:** This action cannot be undone!

### Response (204 No Content)

```json
{
  "message": "Campaign Manager 'janecm' has been successfully deleted."
}
```

### Error Responses

#### 400 Bad Request - Not a Campaign Manager
```json
{
  "error": "This endpoint is only for Campaign Manager users."
}
```

#### 404 Not Found
```json
{
  "detail": "Not found."
}
```

---

## Use Cases

### Use Case 1: Update Email and Phone
```bash
curl -X PATCH http://localhost:8000/api/auth/users/15/update-campaign-manager/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -d '{
    "email": "newemail@example.com",
    "phone_number": "+9999999999"
  }'
```

### Use Case 2: Reassign Campaigns
```bash
curl -X PATCH http://localhost:8000/api/auth/users/15/update-campaign-manager/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -d '{
    "campaign_assignments": [
      {"campaign_name": "Technology Campaign"},
      {"campaign_name": "Equipment Campaign"}
    ]
  }'
```

### Use Case 3: Update Profile Picture (Multipart)
```bash
curl -X PATCH http://localhost:8000/api/auth/users/15/update-campaign-manager/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -F "first_name=Jane" \
  -F "last_name=Doe" \
  -F "email=jane@example.com" \
  -F "phone_number=+1234567890" \
  -F "profile_picture=@/path/to/image.jpg" \
  -F 'campaign_assignments=[{"campaign_name":"State of the Flock 2025"}]'
```

### Use Case 4: Delete Campaign Manager
```bash
curl -X DELETE http://localhost:8000/api/auth/users/15/delete-campaign-manager/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

---

## Frontend Implementation Examples

### React - Update Campaign Manager

```typescript
import axios from 'axios';

interface UpdateCampaignManagerData {
  first_name?: string;
  last_name?: string;
  email?: string;
  phone_number?: string;
  campaign_assignments?: Array<{ campaign_name: string }>;
  profile_picture?: File;
}

const updateCampaignManager = async (
  userId: number,
  data: UpdateCampaignManagerData,
  accessToken: string
) => {
  const isMultipart = !!data.profile_picture;
  
  let payload: FormData | object;
  let headers: any = {
    Authorization: `Bearer ${accessToken}`,
  };

  if (isMultipart) {
    // Multipart form data (with profile picture)
    payload = new FormData();
    Object.entries(data).forEach(([key, value]) => {
      if (key === 'campaign_assignments' && value) {
        payload.append(key, JSON.stringify(value));
      } else if (key === 'profile_picture' && value) {
        payload.append(key, value as File);
      } else if (value !== undefined) {
        payload.append(key, value as string);
      }
    });
    headers['Content-Type'] = 'multipart/form-data';
  } else {
    // JSON payload
    payload = data;
    headers['Content-Type'] = 'application/json';
  }

  try {
    const response = await axios.patch(
      `/api/auth/users/${userId}/update-campaign-manager/`,
      payload,
      { headers }
    );
    return response.data;
  } catch (error: any) {
    throw new Error(error.response?.data || 'Update failed');
  }
};

// Usage
const handleUpdate = async () => {
  try {
    const result = await updateCampaignManager(
      15,
      {
        email: 'newemail@example.com',
        campaign_assignments: [
          { campaign_name: 'Technology Campaign' },
          { campaign_name: 'Equipment Campaign' }
        ]
      },
      accessToken
    );
    console.log('Updated:', result);
  } catch (error) {
    console.error('Error:', error);
  }
};
```

### React - Delete Campaign Manager

```typescript
const deleteCampaignManager = async (
  userId: number,
  accessToken: string
) => {
  try {
    const response = await axios.delete(
      `/api/auth/users/${userId}/delete-campaign-manager/`,
      {
        headers: {
          Authorization: `Bearer ${accessToken}`,
        }
      }
    );
    return response.data;
  } catch (error: any) {
    throw new Error(error.response?.data || 'Delete failed');
  }
};

// Usage with confirmation
const handleDelete = async (userId: number) => {
  const confirmed = window.confirm(
    'Are you sure you want to delete this Campaign Manager? This action cannot be undone!'
  );
  
  if (!confirmed) return;

  try {
    await deleteCampaignManager(userId, accessToken);
    alert('Campaign Manager deleted successfully');
    // Redirect or refresh list
  } catch (error) {
    console.error('Error:', error);
    alert('Failed to delete Campaign Manager');
  }
};
```

### React Native - Update Form Component

```tsx
import React, { useState } from 'react';
import {
  View,
  Text,
  TextInput,
  TouchableOpacity,
  Alert,
  ScrollView,
  StyleSheet
} from 'react-native';
import axios from 'axios';
import AsyncStorage from '@react-native-async-storage/async-storage';

const UpdateCampaignManagerScreen = ({ route, navigation }) => {
  const { userId, currentData } = route.params;
  
  const [firstName, setFirstName] = useState(currentData.first_name);
  const [lastName, setLastName] = useState(currentData.last_name);
  const [email, setEmail] = useState(currentData.email);
  const [phoneNumber, setPhoneNumber] = useState(currentData.phone_number);
  const [loading, setLoading] = useState(false);

  const handleUpdate = async () => {
    setLoading(true);
    
    try {
      const token = await AsyncStorage.getItem('accessToken');
      
      const response = await axios.patch(
        `/api/auth/users/${userId}/update-campaign-manager/`,
        {
          first_name: firstName,
          last_name: lastName,
          email: email,
          phone_number: phoneNumber
        },
        {
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
          }
        }
      );
      
      Alert.alert('Success', 'Campaign Manager updated successfully');
      navigation.goBack();
    } catch (error: any) {
      const errorMsg = error.response?.data?.detail || 'Update failed';
      Alert.alert('Error', errorMsg);
    } finally {
      setLoading(false);
    }
  };

  return (
    <ScrollView style={styles.container}>
      <Text style={styles.title}>Update Campaign Manager</Text>

      <TextInput
        style={styles.input}
        placeholder="First Name"
        value={firstName}
        onChangeText={setFirstName}
      />

      <TextInput
        style={styles.input}
        placeholder="Last Name"
        value={lastName}
        onChangeText={setLastName}
      />

      <TextInput
        style={styles.input}
        placeholder="Email"
        value={email}
        onChangeText={setEmail}
        keyboardType="email-address"
        autoCapitalize="none"
      />

      <TextInput
        style={styles.input}
        placeholder="Phone Number"
        value={phoneNumber}
        onChangeText={setPhoneNumber}
        keyboardType="phone-pad"
      />

      <TouchableOpacity
        style={[styles.button, loading && styles.buttonDisabled]}
        onPress={handleUpdate}
        disabled={loading}
      >
        <Text style={styles.buttonText}>
          {loading ? 'Updating...' : 'Update'}
        </Text>
      </TouchableOpacity>
    </ScrollView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    padding: 20,
    backgroundColor: '#fff',
  },
  title: {
    fontSize: 24,
    fontWeight: 'bold',
    marginBottom: 20,
  },
  input: {
    borderWidth: 1,
    borderColor: '#ddd',
    padding: 12,
    marginBottom: 15,
    borderRadius: 8,
    fontSize: 16,
  },
  button: {
    backgroundColor: '#2196F3',
    padding: 15,
    borderRadius: 8,
    alignItems: 'center',
    marginTop: 10,
  },
  buttonDisabled: {
    backgroundColor: '#ccc',
  },
  buttonText: {
    color: '#fff',
    fontSize: 16,
    fontWeight: 'bold',
  },
});

export default UpdateCampaignManagerScreen;
```

---

## Important Notes

### Campaign Assignments Behavior

1. **Replace, Not Merge:** When you update `campaign_assignments`, it **completely replaces** all existing assignments
2. **Always Provide Full List:** If you want to keep existing campaigns, include them in the update
3. **Empty Not Allowed:** Cannot update to an empty campaign list (must have at least one campaign)

#### Example - Adding a Campaign
```javascript
// Current assignments: ["Campaign A", "Campaign B"]
// To add "Campaign C", you must send:
{
  "campaign_assignments": [
    {"campaign_name": "Campaign A"},
    {"campaign_name": "Campaign B"},
    {"campaign_name": "Campaign C"}  // New one
  ]
}
```

#### Example - Removing a Campaign
```javascript
// Current assignments: ["Campaign A", "Campaign B", "Campaign C"]
// To remove "Campaign B", send:
{
  "campaign_assignments": [
    {"campaign_name": "Campaign A"},
    {"campaign_name": "Campaign C"}
  ]
}
```

### Field Constraints

- **Username:** Cannot be changed (read-only)
- **Role:** Cannot be changed (must remain `CAMPAIGN_MANAGER`)
- **Service:** Cannot be assigned (Campaign Managers have no service)
- **Email:** Must be unique across all users
- **Phone Number:** Must be unique across all users

### Deletion Cascade

When a Campaign Manager is deleted, the following are automatically deleted:

1. All `CampaignManagerAssignment` records
2. All submissions (`StateOfTheFlockSubmission`, `SoulWinningSubmission`, etc.)
3. All associated files (profile pictures, submission images)

---

## Testing

### Test Update
```bash
# 1. Create a Campaign Manager
POST /api/auth/users/create-campaign-manager/

# 2. Update email
PATCH /api/auth/users/{id}/update-campaign-manager/
{
  "email": "newemail@example.com"
}

# 3. Verify in response
```

### Test Delete
```bash
# 1. Delete Campaign Manager
DELETE /api/auth/users/{id}/delete-campaign-manager/

# 2. Try to fetch (should return 404)
GET /api/auth/users/{id}/
```

---

## Error Handling

```typescript
try {
  await updateCampaignManager(userId, data, token);
} catch (error: any) {
  if (error.response?.status === 400) {
    // Validation error or not a Campaign Manager
    console.error('Validation:', error.response.data);
  } else if (error.response?.status === 404) {
    // User not found
    console.error('User not found');
  } else {
    // Other error
    console.error('Unexpected error:', error);
  }
}
```

---

## See Also

- [Campaign Manager API](./CAMPAIGN_MANAGER_API.md)
- [Campaign Manager Service Selection](./CAMPAIGN_MANAGER_SERVICE_SELECTION.md)
- [Custom Login API](./CUSTOM_LOGIN_API.md)

---

**Implementation Date:** November 10, 2025  
**Last Updated:** November 10, 2025


