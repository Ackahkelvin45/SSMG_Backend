# How to Get Campaign IDs for Assignment

When creating Campaign Managers, you need to know the campaign IDs and types. Here's how to get them.

---

## Get All Campaigns of Each Type

### 1. State of the Flock Campaigns
```bash
GET /api/campaigns/state-of-the-flock/
```

**Response:**
```json
{
  "results": [
    {
      "id": 1,
      "name": "State of the Flock 2025",
      "campaign_id": "SOF001",
      "description": "...",
      "status": "Active"
    }
  ]
}
```

Use `"campaign_type": "StateOfTheFlockCampaign"` with the `id` value.

---

### 2. Soul Winning Campaigns
```bash
GET /api/campaigns/soul-winning/
```
Use `"campaign_type": "SoulWinningCampaign"`

---

### 3. Servants Armed and Trained Campaigns
```bash
GET /api/campaigns/servants-armed-trained/
```
Use `"campaign_type": "ServantsArmedTrainedCampaign"`

---

### 4. Antibrutish Campaigns
```bash
GET /api/campaigns/antibrutish/
```
Use `"campaign_type": "AntibrutishCampaign"`

---

### 5. Hearing and Seeing Campaigns
```bash
GET /api/campaigns/hearing-seeing/
```
Use `"campaign_type": "HearingSeeingCampaign"`

---

### 6. Honour Your Prophet Campaigns
```bash
GET /api/campaigns/honour-your-prophet/
```
Use `"campaign_type": "HonourYourProphetCampaign"`

---

### 7. Basonta Proliferation Campaigns
```bash
GET /api/campaigns/basonta-proliferation/
```
Use `"campaign_type": "BasontaProliferationCampaign"`

---

### 8. Intimate Counseling Campaigns
```bash
GET /api/campaigns/intimate-counseling/
```
Use `"campaign_type": "IntimateCounselingCampaign"`

---

### 9. Technology Campaigns
```bash
GET /api/campaigns/technology/
```
Use `"campaign_type": "TechnologyCampaign"`

---

### 10. Sheperding Control Campaigns
```bash
GET /api/campaigns/sheperding-control/
```
Use `"campaign_type": "SheperdingControlCampaign"`

---

### 11. Multiplication Campaigns
```bash
GET /api/campaigns/multiplication/
```
Use `"campaign_type": "MultiplicationCampaign"`

---

### 12. Understanding Campaigns
```bash
GET /api/campaigns/understanding/
```
Use `"campaign_type": "UnderstandingCampaign"`

---

### 13. Sheep Seeking Campaigns
```bash
GET /api/campaigns/sheep-seeking/
```
Use `"campaign_type": "SheepSeekingCampaign"`

---

### 14. Testimony Campaigns
```bash
GET /api/campaigns/testimony/
```
Use `"campaign_type": "TestimonyCampaign"`

---

### 15. Telepastoring Campaigns
```bash
GET /api/campaigns/telepastoring/
```
Use `"campaign_type": "TelepastoringCampaign"`

---

### 16. Gathering Bus Campaigns
```bash
GET /api/campaigns/gathering-bus/
```
Use `"campaign_type": "GatheringBusCampaign"`

---

### 17. Organised Creative Arts Campaigns
```bash
GET /api/campaigns/organised-creative-arts/
```
Use `"campaign_type": "OrganisedCreativeArtsCampaign"`

---

### 18. Tangerine Campaigns
```bash
GET /api/campaigns/tangerine/
```
Use `"campaign_type": "TangerineCampaign"`

---

### 19. Swollen Sunday Campaigns
```bash
GET /api/campaigns/swollen-sunday/
```
Use `"campaign_type": "SwollenSundayCampaign"`

---

### 20. Sunday Management Campaigns
```bash
GET /api/campaigns/sunday-management/
```
Use `"campaign_type": "SundayManagementCampaign"`

---

## Quick Reference Table

| Campaign Type | Endpoint Path | campaign_type Value |
|---------------|--------------|---------------------|
| State of the Flock | `/state-of-the-flock/` | `StateOfTheFlockCampaign` |
| Soul Winning | `/soul-winning/` | `SoulWinningCampaign` |
| Servants Armed and Trained | `/servants-armed-trained/` | `ServantsArmedTrainedCampaign` |
| Antibrutish | `/antibrutish/` | `AntibrutishCampaign` |
| Hearing and Seeing | `/hearing-seeing/` | `HearingSeeingCampaign` |
| Honour Your Prophet | `/honour-your-prophet/` | `HonourYourProphetCampaign` |
| Basonta Proliferation | `/basonta-proliferation/` | `BasontaProliferationCampaign` |
| Intimate Counseling | `/intimate-counseling/` | `IntimateCounselingCampaign` |
| Technology | `/technology/` | `TechnologyCampaign` |
| Sheperding Control | `/sheperding-control/` | `SheperdingControlCampaign` |
| Multiplication | `/multiplication/` | `MultiplicationCampaign` |
| Understanding | `/understanding/` | `UnderstandingCampaign` |
| Sheep Seeking | `/sheep-seeking/` | `SheepSeekingCampaign` |
| Testimony | `/testimony/` | `TestimonyCampaign` |
| Telepastoring | `/telepastoring/` | `TelepastoringCampaign` |
| Gathering Bus | `/gathering-bus/` | `GatheringBusCampaign` |
| Organised Creative Arts | `/organised-creative-arts/` | `OrganisedCreativeArtsCampaign` |
| Tangerine | `/tangerine/` | `TangerineCampaign` |
| Swollen Sunday | `/swollen-sunday/` | `SwollenSundayCampaign` |
| Sunday Management | `/sunday-management/` | `SundayManagementCampaign` |

---

## Example Workflow

### Step 1: Get Campaign IDs

```bash
# Get State of the Flock campaigns
curl -X GET "http://localhost:8000/api/campaigns/state-of-the-flock/" \
  -H "Authorization: Bearer YOUR_TOKEN"

# Response:
# { "results": [{ "id": 1, "name": "SOF 2025", ... }] }

# Get Soul Winning campaigns
curl -X GET "http://localhost:8000/api/campaigns/soul-winning/" \
  -H "Authorization: Bearer YOUR_TOKEN"

# Response:
# { "results": [{ "id": 1, "name": "SW Initiative", ... }] }
```

### Step 2: Create Campaign Manager with Those IDs

```bash
curl -X POST "http://localhost:8000/api/users/create-campaign-manager/" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "John",
    "last_name": "Doe",
    "username": "johndoe",
    "email": "john@example.com",
    "phone_number": "+1234567890",
    "password": "securepass123",
    "campaign_assignments": [
      {
        "campaign_type": "StateOfTheFlockCampaign",
        "campaign_id": 1
      },
      {
        "campaign_type": "SoulWinningCampaign",
        "campaign_id": 1
      }
    ]
  }'
```

---

## Python Helper Function

```python
import requests

def get_all_campaign_ids(base_url, token):
    """
    Fetch all campaign IDs for easy reference.
    
    Returns a dictionary mapping campaign types to their instances.
    """
    headers = {"Authorization": f"Bearer {token}"}
    
    campaign_endpoints = {
        "StateOfTheFlockCampaign": "state-of-the-flock",
        "SoulWinningCampaign": "soul-winning",
        "ServantsArmedTrainedCampaign": "servants-armed-trained",
        "AntibrutishCampaign": "antibrutish",
        "HearingSeeingCampaign": "hearing-seeing",
        "HonourYourProphetCampaign": "honour-your-prophet",
        "BasontaProliferationCampaign": "basonta-proliferation",
        "IntimateCounselingCampaign": "intimate-counseling",
        "TechnologyCampaign": "technology",
        "SheperdingControlCampaign": "sheperding-control",
        "MultiplicationCampaign": "multiplication",
        "UnderstandingCampaign": "understanding",
        "SheepSeekingCampaign": "sheep-seeking",
        "TestimonyCampaign": "testimony",
        "TelepastoringCampaign": "telepastoring",
        "GatheringBusCampaign": "gathering-bus",
        "OrganisedCreativeArtsCampaign": "organised-creative-arts",
        "TangerineCampaign": "tangerine",
        "SwollenSundayCampaign": "swollen-sunday",
        "SundayManagementCampaign": "sunday-management",
    }
    
    all_campaigns = {}
    
    for campaign_type, endpoint in campaign_endpoints.items():
        url = f"{base_url}/api/campaigns/{endpoint}/"
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            campaigns = data.get('results', [])
            all_campaigns[campaign_type] = [
                {"id": c["id"], "name": c["name"], "campaign_id": c.get("campaign_id")}
                for c in campaigns
            ]
    
    return all_campaigns


# Usage
campaigns = get_all_campaign_ids("http://localhost:8000", "your_token_here")

# Create assignments
assignments = [
    {"campaign_type": "StateOfTheFlockCampaign", "campaign_id": campaigns["StateOfTheFlockCampaign"][0]["id"]},
    {"campaign_type": "SoulWinningCampaign", "campaign_id": campaigns["SoulWinningCampaign"][0]["id"]},
]

# Use in create campaign manager request
payload = {
    "first_name": "Jane",
    "last_name": "Smith",
    "username": "janesmith",
    "email": "jane@example.com",
    "phone_number": "+1234567890",
    "password": "securepass123",
    "campaign_assignments": assignments
}
```

---

## Notes

- All campaign list endpoints require authentication
- Use the `id` field from the response as `campaign_id` in assignments
- Campaign names and IDs are for display/reference only
- The `campaign_type` must exactly match the model class name (case-sensitive)

