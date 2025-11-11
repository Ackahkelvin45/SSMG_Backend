# Change Log: Campaign Manager Service Selection

**Date:** November 10, 2025  
**Feature:** Campaign Managers can now select which service they're submitting data for

---

## Summary

Campaign Managers are not assigned to a specific service and can work across multiple services for their assigned campaigns. This update allows them to specify which service each submission is for.

---

## Changes Made

### 1. Backend Logic (`campaigns/views.py`)

#### Added Helper Function:
```python
def get_service_for_submission(user, request_data):
    """
    Helper function to determine which service to use for a submission.
    Campaign Managers must provide a service ID in request data.
    Other users use their assigned service.
    """
    if user.is_campaign_manager:
        service_id = request_data.get('service')
        if not service_id:
            raise serializers.ValidationError({
                "service": "Campaign Managers must specify a service."
            })
        try:
            from authentication.models import Service
            service = Service.objects.get(id=service_id)
        except Service.DoesNotExist:
            raise serializers.ValidationError({
                "service": "Invalid service id."
            })
        return service
    else:
        return getattr(user, 'service', None)
```

#### Updated All 21 ViewSets:
- `StateOfTheFlockSubmissionViewSet`
- `SoulWinningSubmissionViewSet`
- `ServantsArmedTrainedSubmissionViewSet`
- `AntibrutishSubmissionViewSet`
- `HearingSeeingSubmissionViewSet`
- `HonourYourProphetSubmissionViewSet`
- `BasontaProliferationSubmissionViewSet`
- `IntimateCounselingSubmissionViewSet`
- `TechnologySubmissionViewSet`
- `SheperdingControlSubmissionViewSet`
- `MultiplicationSubmissionViewSet`
- `UnderstandingSubmissionViewSet`
- `SheepSeekingSubmissionViewSet`
- `TestimonySubmissionViewSet`
- `TelepastoringSubmissionViewSet`
- `GatheringBusSubmissionViewSet`
- `OrganisedCreativeArtsSubmissionViewSet`
- `TangerineSubmissionViewSet`
- `SwollenSundaySubmissionViewSet`
- `SundayManagementSubmissionViewSet`
- `EquipmentSubmissionViewSet`

All now use: `service = get_service_for_submission(user, self.request.data)`

---

### 2. Documentation Updates

#### `campaigns/README.md`
- Updated POST fields section to clarify:
  - Campaign Managers MUST provide `service` field
  - Pastors/Helpers should NOT provide `service` field (auto-set)
- Added `service` to common fields with role-based requirements

#### `CAMPAIGN_MANAGER_SERVICE_SELECTION.md` (NEW)
Comprehensive guide covering:
- How service selection works
- API examples for both Campaign Managers and Pastors
- Frontend implementation examples (React/React Native)
- Validation rules and error scenarios
- Best practices and FAQ

---

## Breaking Changes

### ⚠️ FOR CAMPAIGN MANAGERS ONLY

**Before this update:**
```json
{
  "campaign": 1,
  "submission_period": "2025-11-01",
  "date": "2025-11-10",
  "total_membership": 200
}
```
✅ This worked (but service was set to null)

**After this update:**
```json
{
  "campaign": 1,
  "service": 5,
  "submission_period": "2025-11-01",
  "date": "2025-11-10",
  "total_membership": 200
}
```
✅ Now `service` is REQUIRED

Without `service`:
```json
{
  "service": ["Campaign Managers must specify a service."]
}
```
❌ Error response

### ✅ NO BREAKING CHANGES FOR PASTORS/HELPERS

Pastors and Helpers continue to work exactly as before. The `service` field is still automatically set from their user profile.

---

## Migration Guide

### For Mobile/Web Frontends

#### Step 1: Check User Role
```typescript
const user = getCurrentUser(); // Your auth context
const isCampaignManager = user.role === 'CAMPAIGN_MANAGER';
```

#### Step 2: Conditionally Show Service Selector
```typescript
{isCampaignManager && (
  <ServiceSelector
    required
    value={formData.service}
    onChange={(value) => setFormData({...formData, service: value})}
  />
)}
```

#### Step 3: Fetch Services List (Campaign Managers Only)
```typescript
useEffect(() => {
  if (isCampaignManager) {
    fetchServices();
  }
}, [isCampaignManager]);

const fetchServices = async () => {
  const response = await api.get('/api/auth/services/');
  setServices(response.data.results);
};
```

#### Step 4: Include Service in Submission (Campaign Managers Only)
```typescript
const submitData = {
  campaign: formData.campaign,
  ...(isCampaignManager && { service: formData.service }),
  submission_period: formData.submission_period,
  date: formData.date,
  // ... other fields
};

await api.post('/api/campaigns/state-of-flock/submissions/', submitData);
```

---

## Testing Checklist

### Campaign Manager Tests
- [ ] Submit WITH `service` field → Success (201)
- [ ] Submit WITHOUT `service` field → Error (400)
- [ ] Submit with INVALID `service` ID → Error (400)
- [ ] Submit for service with different campaigns → Success
- [ ] Fetch services list → Success (200)

### Pastor/Helper Tests
- [ ] Submit WITHOUT `service` field → Success (201, service auto-set)
- [ ] Submit WITH `service` field → Success (201, provided service ignored)
- [ ] Verify service matches user's assigned service

### Admin Tests
- [ ] View all submissions → See correct service assignments
- [ ] Filter by service → Works correctly
- [ ] Analytics → Services correctly attributed

---

## API Endpoint Reference

### Get Services List
```
GET /api/auth/services/
Authorization: Token <your-token>
```

### Create Submission (Campaign Manager)
```
POST /api/campaigns/{campaign-type}/submissions/
Authorization: Token <campaign-manager-token>
Content-Type: application/json

{
  "campaign": 1,
  "service": 5,    // REQUIRED for Campaign Managers
  "submission_period": "2025-11-01",
  "date": "2025-11-10",
  // ... other fields
}
```

### Create Submission (Pastor/Helper)
```
POST /api/campaigns/{campaign-type}/submissions/
Authorization: Token <pastor-token>
Content-Type: application/json

{
  "campaign": 1,
  // NO service field needed
  "submission_period": "2025-11-01",
  "date": "2025-11-10",
  // ... other fields
}
```

---

## Rollback Plan

If issues arise, revert the following changes in `campaigns/views.py`:

1. Remove `get_service_for_submission` function (lines 199-216)
2. Restore old logic in all `perform_create` methods:
   ```python
   service = getattr(self.request.user, 'service', None)
   serializer.save(submitted_by=self.request.user, service=service, campaign=campaign)
   ```

---

## Future Enhancements

1. **Service Permissions:** Restrict Campaign Managers to only submit for specific services (optional)
2. **Service History:** Track which services a Campaign Manager has submitted for
3. **Default Service:** Allow Campaign Managers to set a default service
4. **Bulk Submissions:** Submit for multiple services in one API call
5. **Service Validation:** Ensure service is active/exists before submission

---

## Support

For questions or issues, contact:
- Backend Team: backend@ssmg.org
- Documentation: See `CAMPAIGN_MANAGER_SERVICE_SELECTION.md`

---

**Status:** ✅ Deployed  
**Version:** 2.1.0  
**Affects:** Campaign Managers only


