# Multipart Form Data Guide - Campaign Manager Creation

## Problem You Encountered

When sending a profile picture with the Campaign Manager creation request, you need to use `multipart/form-data` format. However, Django REST Framework doesn't automatically parse JSON strings in form fields, causing the error:

```json
{
  "campaign_assignments": ["This field is required."]
}
```

## Solution

The serializer now handles both:
1. **JSON payload** (Content-Type: application/json) - for requests without files
2. **Multipart payload** (Content-Type: multipart/form-data) - for requests with profile picture

---

## How to Send Requests

### Option 1: Without Profile Picture (JSON)

Use `application/json` - simple and straightforward:

```bash
curl -X POST http://localhost:8000/api/users/create-campaign-manager/ \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "John",
    "last_name": "Doe",
    "username": "johndoe",
    "email": "john@example.com",
    "phone_number": "+1234567890",
    "campaign_assignments": [
      {"campaign_name": "State of the Flock 2025"},
      {"campaign_name": "Soul Winning Initiative"}
    ]
  }'
```

---

### Option 2: With Profile Picture (Multipart)

Use `multipart/form-data` and **stringify the campaign_assignments**:

```bash
curl -X POST http://localhost:8000/api/users/create-campaign-manager/ \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -F "first_name=John" \
  -F "last_name=Doe" \
  -F "username=johndoe" \
  -F "email=john@example.com" \
  -F "phone_number=+1234567890" \
  -F "profile_picture=@/path/to/photo.jpg" \
  -F 'campaign_assignments=[{"campaign_name":"State of the Flock 2025"},{"campaign_name":"Soul Winning Initiative"}]'
```

**Key Point:** The `campaign_assignments` field is sent as a JSON **string**, not as a JavaScript object.

---

## Frontend Implementation

### React/JavaScript with FormData

```javascript
const createCampaignManager = async (formData) => {
  const fd = new FormData();
  
  // Add basic fields
  fd.append('first_name', formData.firstName);
  fd.append('last_name', formData.lastName);
  fd.append('username', formData.username);
  fd.append('email', formData.email);
  fd.append('phone_number', formData.phoneNumber);
  
  // Add profile picture if provided
  if (formData.profilePicture) {
    fd.append('profile_picture', formData.profilePicture);
  }
  
  // IMPORTANT: Stringify the campaign assignments
  const assignments = formData.selectedCampaigns.map(name => ({
    campaign_name: name
  }));
  fd.append('campaign_assignments', JSON.stringify(assignments));
  
  const response = await fetch('/api/users/create-campaign-manager/', {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${token}`
      // Don't set Content-Type - browser will set it automatically with boundary
    },
    body: fd
  });
  
  return await response.json();
};

// Usage example
const result = await createCampaignManager({
  firstName: 'John',
  lastName: 'Doe',
  username: 'johndoe',
  email: 'john@example.com',
  phoneNumber: '+1234567890',
  profilePicture: fileInputElement.files[0],
  selectedCampaigns: [
    'State of the Flock 2025',
    'Soul Winning Initiative',
    'Technology Upgrade'
  ]
});
```

---

### React Native / Expo

```javascript
const createCampaignManager = async (formData) => {
  const fd = new FormData();
  
  // Add basic fields
  fd.append('first_name', formData.firstName);
  fd.append('last_name', formData.lastName);
  fd.append('username', formData.username);
  fd.append('email', formData.email);
  fd.append('phone_number', formData.phoneNumber);
  
  // Add profile picture if provided
  if (formData.profilePicture) {
    fd.append('profile_picture', {
      uri: formData.profilePicture.uri,
      type: 'image/jpeg',
      name: 'profile.jpg'
    });
  }
  
  // Stringify campaign assignments
  const assignments = formData.selectedCampaigns.map(name => ({
    campaign_name: name
  }));
  fd.append('campaign_assignments', JSON.stringify(assignments));
  
  const response = await fetch('https://ssmg-backend.onrender.com/api/users/create-campaign-manager/', {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'multipart/form-data'
    },
    body: fd
  });
  
  return await response.json();
};
```

---

### Axios (JavaScript)

```javascript
import axios from 'axios';

const createCampaignManager = async (formData) => {
  const fd = new FormData();
  
  fd.append('first_name', formData.firstName);
  fd.append('last_name', formData.lastName);
  fd.append('username', formData.username);
  fd.append('email', formData.email);
  fd.append('phone_number', formData.phoneNumber);
  
  if (formData.profilePicture) {
    fd.append('profile_picture', formData.profilePicture);
  }
  
  // Stringify campaigns
  const assignments = formData.selectedCampaigns.map(name => ({
    campaign_name: name
  }));
  fd.append('campaign_assignments', JSON.stringify(assignments));
  
  const response = await axios.post(
    '/api/users/create-campaign-manager/',
    fd,
    {
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'multipart/form-data'
      }
    }
  );
  
  return response.data;
};
```

---

## Common Mistakes

### ❌ Mistake 1: Not Stringifying Campaign Assignments

```javascript
// WRONG
fd.append('campaign_assignments', [
  {campaign_name: "Campaign 1"}
]);

// RIGHT
fd.append('campaign_assignments', JSON.stringify([
  {campaign_name: "Campaign 1"}
]));
```

---

### ❌ Mistake 2: Invalid JSON String

```javascript
// WRONG - Single quotes in JSON
fd.append('campaign_assignments', "[{'campaign_name':'Campaign 1'}]");

// RIGHT - Double quotes in JSON
fd.append('campaign_assignments', '[{"campaign_name":"Campaign 1"}]');
```

---

### ❌ Mistake 3: Sending as Nested Objects (Doesn't Work in FormData)

```javascript
// WRONG - FormData doesn't support nested objects
fd.append('campaign_assignments[0][campaign_name]', 'Campaign 1');

// RIGHT - Send as JSON string
fd.append('campaign_assignments', JSON.stringify([
  {campaign_name: 'Campaign 1'}
]));
```

---

## Your Working Payload

Based on your example, here's the correct way to send it:

```javascript
const formData = new FormData();

formData.append('first_name', 'ddf');
formData.append('last_name', 'dfdf');
formData.append('username', 'dfdf');
formData.append('email', 'ackahkelvin45dfdf5@gmail.com');
formData.append('phone_number', '05067734343');
formData.append('profile_picture', profilePictureFile);  // Your binary file

// This is the key part - stringify it!
formData.append('campaign_assignments', JSON.stringify([
  {campaign_name: "Testimony Campaign"},
  {campaign_name: "Telepastoring Campaign"},
  {campaign_name: "Technology Campaign"}
]));

// Send it
await fetch('/api/users/create-campaign-manager/', {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${your_token}`
  },
  body: formData
});
```

---

## Testing with Postman

1. **Method:** POST
2. **URL:** `http://localhost:8000/api/users/create-campaign-manager/`
3. **Headers:**
   - `Authorization: Bearer YOUR_TOKEN`
4. **Body:** Select "form-data"
5. **Add fields:**
   - `first_name`: text → "John"
   - `last_name`: text → "Doe"
   - `username`: text → "johndoe"
   - `email`: text → "john@example.com"
   - `phone_number`: text → "+1234567890"
   - `profile_picture`: file → Select your image
   - `campaign_assignments`: text → `[{"campaign_name":"State of the Flock 2025"}]`

**Important:** Make sure `campaign_assignments` is set to "text" type and contains valid JSON!

---

## How the Backend Handles It

The serializer automatically detects and parses the JSON string:

```python
def validate_campaign_assignments(self, value):
    import json
    
    # If it's a string (from multipart), parse it
    if isinstance(value, str):
        try:
            value = json.loads(value)
        except json.JSONDecodeError:
            raise ValidationError("campaign_assignments must be valid JSON.")
    
    # Continue with validation...
```

---

## Summary

| Content Type | Campaign Assignments Format | Profile Picture |
|--------------|----------------------------|-----------------|
| `application/json` | JSON array | ❌ Not supported |
| `multipart/form-data` | **JSON string** | ✅ Supported |

**Key Takeaway:** When using multipart/form-data, **always stringify** the `campaign_assignments` field!

```javascript
// THE GOLDEN RULE
formData.append('campaign_assignments', JSON.stringify([...]));
```

Now your request should work perfectly! 🎉

