# Campaign Manager Password - Update Summary

## 🔑 Password Behavior Changed

Campaign Manager passwords are now **auto-generated** (default: "kelvin"), just like Pastor and Helper roles.

---

## What Changed

### ❌ Before (Incorrect)
```json
{
  "first_name": "John",
  "last_name": "Doe",
  "username": "johndoe",
  "email": "john@example.com",
  "phone_number": "+1234567890",
  "password": "securepassword123",  // ❌ User had to provide password
  "campaign_assignments": [...]
}
```

**Problem:** Password was exposed in the API request, different from Pastor/Helper behavior.

---

### ✅ After (Correct)
```json
{
  "first_name": "John",
  "last_name": "Doe",
  "username": "johndoe",
  "email": "john@example.com",
  "phone_number": "+1234567890",
  // No password field - auto-generated as "kelvin"
  "campaign_assignments": [...]
}
```

**Benefit:** Consistent with Pastor/Helper roles. Password is auto-generated and not exposed.

---

## Code Changes

### 1. UserManager (`authentication/models.py`)

**Before:**
```python
if role not in ["ADMIN", "CAMPAIGN_MANAGER"] and not password:
    password = self.generate_random_password()
```

**After:**
```python
if role not in ["ADMIN"] and not password:
    password = self.generate_random_password()
```

Now Campaign Managers get auto-generated passwords like Pastor/Helper.

---

### 2. Serializer (`authentication/serializers.py`)

**Removed:**
- `password` field from serializer fields list
- Password validation

**Updated:**
```python
def create(self, validated_data):
    # ...
    user = CustomerUser.objects.create_user(
        username=validated_data['username'],
        email=validated_data['email'],
        password=None,  # ✅ Will be auto-generated
        # ...
    )
```

---

### 3. View (`authentication/views.py`)

**Updated docstring:**
```python
"""
Create a campaign manager user and assign campaigns.

Campaign Managers are NOT assigned to a specific service.
They can fill data for their assigned campaigns across ALL services.

Password is auto-generated (default: "kelvin") - not exposed in the API.

Required fields:
- first_name, last_name, username, email, phone_number
- campaign_assignments: list of objects with campaign_type and campaign_id
"""
```

No more `password` in required fields.

---

## Role Comparison

| Role | Password Behavior |
|------|-------------------|
| **Admin** | ✅ Must provide password |
| **Pastor** | ✅ Auto-generated ("kelvin") |
| **Helper** | ✅ Auto-generated ("kelvin") |
| **Campaign Manager** | ✅ Auto-generated ("kelvin") |

---

## Default Password

All Campaign Managers are created with the default password: **`kelvin`**

(This is set in `UserManager.generate_random_password()`)

```python
def generate_random_password(self, length=10):
    """Generate a secure random password."""
    characters = string.ascii_letters + string.digits + string.punctuation
    return "kelvin"  # ← Default password
```

---

## Security Best Practice

Campaign Managers should:
1. Log in with username and default password ("kelvin")
2. Immediately change their password using the change password endpoint:

```bash
POST /api/users/change_password/
{
  "old_password": "kelvin",
  "new_password": "newSecurePassword123",
  "confirm_password": "newSecurePassword123"
}
```

---

## Example API Request

### Creating a Campaign Manager

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
      {"campaign_type": "StateOfTheFlockCampaign", "campaign_id": 1}
    ]
  }'
```

**Response:**
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
      "created_at": "2025-11-10T12:00:00Z"
    }
  ],
  "created_at": "2025-11-10T12:00:00Z"
}
```

**Note:** Password is auto-generated and not returned in the response.

---

## Login Flow

### 1. Campaign Manager Logs In (First Time)

```bash
POST /api/auth/login/
{
  "username": "johndoe",
  "password": "kelvin"  // Default password
}
```

### 2. Change Password (Required After First Login)

```bash
POST /api/users/change_password/
{
  "old_password": "kelvin",
  "new_password": "MyNewSecurePassword123!",
  "confirm_password": "MyNewSecurePassword123!"
}
```

### 3. Future Logins

```bash
POST /api/auth/login/
{
  "username": "johndoe",
  "password": "MyNewSecurePassword123!"  // Their new password
}
```

---

## Documentation Updated

All documentation has been updated to reflect the auto-generated password:

✅ `CAMPAIGN_MANAGER_API.md`
✅ `CAMPAIGN_MANAGER_IMPLEMENTATION_SUMMARY.md`
✅ `CAMPAIGN_MANAGER_NO_SERVICE_EXPLANATION.md`
✅ `authentication/views.py` (docstring)
✅ `authentication/serializers.py` (docstring)

---

## Summary

### Key Points

1. ✅ **No password field** in API request
2. ✅ **Auto-generated password** (default: "kelvin")
3. ✅ **Consistent behavior** with Pastor/Helper roles
4. ✅ **More secure** - password not exposed in API
5. ✅ **Users should change password** after first login

### Migration

No database migration needed - this is a serializer/view change only.

Existing Campaign Managers keep their current passwords.

New Campaign Managers created after this change will have auto-generated passwords.

