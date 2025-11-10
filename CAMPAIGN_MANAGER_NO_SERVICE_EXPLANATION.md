# Campaign Manager Service Assignment - Important Design Decision

## 🎯 Key Point

**Campaign Managers are NOT assigned to a specific service.**

---

## Why This Design?

### ❌ What We DON'T Want

```
Campaign Manager → Assigned to Service A only
                  → Can only submit data for Service A
                  → Cannot work with Service B, C, D, etc.
```

**Problem:** This would be too restrictive. A Campaign Manager managing "State of the Flock" campaign would be limited to only one church location.

---

### ✅ What We WANT (Current Implementation)

```
Campaign Manager → NOT tied to any service
                  → Assigned to: "State of the Flock" campaign
                  → Can submit data for Service A, B, C, D, etc.
                  → Works across ALL church locations
```

**Benefit:** Campaign Managers can collect and submit campaign data from ANY service/church location for their assigned campaigns.

---

## Practical Example

### Scenario
John is a Campaign Manager assigned to:
- State of the Flock Campaign
- Soul Winning Campaign

### With NO Service Assignment (Current Implementation) ✅

John can submit data for:
- State of the Flock at Service A (Downtown Church)
- State of the Flock at Service B (Suburb Church)
- State of the Flock at Service C (East Side Church)
- Soul Winning at Service A
- Soul Winning at Service B
- Soul Winning at Service C

**Flexibility:** John manages these campaigns across the entire organization.

---

### If We Had Service Assignment (NOT Implemented) ❌

If John was assigned to Service A only:
- ✅ Can submit State of the Flock for Service A
- ✅ Can submit Soul Winning for Service A
- ❌ CANNOT submit for Service B
- ❌ CANNOT submit for Service C

**Problem:** Too restrictive for campaign management needs.

---

## Implementation Details

### In the Database

```python
# Campaign Manager User
user = CustomerUser.objects.create_user(
    username="john_manager",
    role="CAMPAIGN_MANAGER",
    service=None,  # ← Intentionally set to None
)
```

### In the API Request

```json
{
  "first_name": "John",
  "last_name": "Manager",
  "username": "johnmanager",
  "email": "john@example.com",
  "phone_number": "+1234567890",
  "campaign_assignments": [
    {"campaign_type": "StateOfTheFlockCampaign", "campaign_id": 1}
  ]
  // Note: NO "service" field
  // Note: NO "password" field - auto-generated as "kelvin"
}
```

### In Submissions

When a Campaign Manager creates a submission:

```json
{
  "campaign": 1,  // ← The assigned campaign
  "service": 5,   // ← ANY service - not restricted
  "submission_period": "2025-11-01",
  "date": "2025-11-10",
  "total_membership": 150,
  ...
}
```

The Campaign Manager can choose ANY service when submitting data.

---

## Role Comparison

| User Type | Service Assignment | Campaign Assignment | Access Scope |
|-----------|-------------------|---------------------|--------------|
| **Pastor** | ✅ Assigned to ONE service | ❌ No campaign restriction | All campaigns at their service |
| **Helper** | ✅ Assigned to ONE service | ❌ No campaign restriction | All campaigns at their service |
| **Campaign Manager** | ❌ NO service assignment | ✅ Assigned to specific campaigns | Assigned campaigns at ALL services |
| **Admin** | ❌ No restrictions | ❌ No restrictions | Everything everywhere |

---

## Permission Model

### Campaign Managers Can:
1. ✅ View their assigned campaigns
2. ✅ Submit data for their assigned campaigns at **ANY service**
3. ✅ View submissions for their assigned campaigns across **ALL services**
4. ✅ Select which service they're submitting data for

### Campaign Managers Cannot:
1. ❌ View or submit data for campaigns they're NOT assigned to
2. ❌ Create new campaigns
3. ❌ Modify campaign settings
4. ❌ Manage users
5. ❌ Access admin functions

---

## Real-World Use Case

### Organization Structure
```
Church Organization
├── Service A (Downtown)
├── Service B (Suburb)
├── Service C (East Side)
└── Service D (North Branch)

Campaigns:
├── State of the Flock Campaign (ID: 1)
├── Soul Winning Campaign (ID: 2)
└── Technology Campaign (ID: 3)
```

### Campaign Manager Setup

**Sarah - State of the Flock Manager**
- Role: CAMPAIGN_MANAGER
- Service: None
- Assigned Campaign: State of the Flock (ID: 1)
- Can submit data for this campaign at Services A, B, C, and D

**Mike - Technology Manager**
- Role: CAMPAIGN_MANAGER
- Service: None
- Assigned Campaign: Technology (ID: 3)
- Can submit data for this campaign at Services A, B, C, and D

**Lisa - Multi-Campaign Manager**
- Role: CAMPAIGN_MANAGER
- Service: None
- Assigned Campaigns: 
  - Soul Winning (ID: 2)
  - Technology (ID: 3)
- Can submit data for BOTH campaigns at Services A, B, C, and D

---

## Code Flow

### 1. Creating a Campaign Manager

```python
# POST /api/users/create-campaign-manager/
{
    "first_name": "Sarah",
    "last_name": "Johnson",
    "username": "sarah_flock",
    "email": "sarah@church.org",
    "phone_number": "+1234567890",
    "campaign_assignments": [
        {
            "campaign_type": "StateOfTheFlockCampaign",
            "campaign_id": 1
        }
    ]
}

# Result:
# - User created with role=CAMPAIGN_MANAGER
# - service=None (not restricted)
# - password=auto-generated ("kelvin")
# - Assigned to State of the Flock campaign
```

### 2. Submitting Data

```python
# Sarah logs in and submits data
# POST /api/campaigns/state-of-the-flock-submissions/

{
    "campaign": 1,           # Her assigned campaign
    "service": 3,            # She chose Service C (East Side)
    "submission_period": "2025-11-01",
    "date": "2025-11-10",
    "total_membership": 200,
    "lost": 5,
    "stable": 150,
    "unstable": 45
}

# Backend validation:
# ✅ Sarah is assigned to campaign 1? YES
# ✅ Service 3 exists? YES
# ✅ Sarah can submit for Service 3? YES (no service restriction)
# → Submission accepted
```

### 3. Next Day - Different Service

```python
# Sarah submits for a different service
# POST /api/campaigns/state-of-the-flock-submissions/

{
    "campaign": 1,           # Same assigned campaign
    "service": 2,            # Now submitting for Service B (Suburb)
    "submission_period": "2025-11-01",
    "date": "2025-11-11",
    "total_membership": 180,
    "lost": 3,
    "stable": 135,
    "unstable": 42
}

# ✅ Still valid - Sarah can submit for ANY service
```

---

## Summary

### The Design Choice

**Campaign Managers are assigned to CAMPAIGNS, not SERVICES.**

This gives them:
- **Flexibility** to work across all church locations
- **Focus** on specific campaigns organization-wide
- **Efficiency** in managing campaign data collection
- **Scalability** for growing organizations

### In One Sentence

> Campaign Managers manage their assigned campaigns **organization-wide**, submitting data for any service/location, while Pastors/Helpers manage **all campaigns** at their specific service/location.

---

## Future Considerations

If you ever need to restrict a Campaign Manager to specific services, you could:

1. Add an optional `allowed_services` many-to-many field
2. Add validation in the submission view
3. Filter service dropdown in the UI

But for now, the unrestricted access across all services provides the most flexibility for campaign management.

