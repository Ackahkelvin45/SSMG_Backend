# Campaign Submissions API Documentation

This README provides documentation for the Campaign Submissions API endpoints, including how to list submissions by campaign, get submission details, and filter by date ranges.

## Table of Contents
- [Authentication](#authentication)
- [Base URL](#base-url)
- [Available Campaigns](#available-campaigns)
- [List Submissions by Campaign](#list-submissions-by-campaign)
- [Get Submission Detail](#get-submission-detail)
- [Date Range Filtering](#date-range-filtering)
- [Combined Filtering](#combined-filtering)
- [Response Format](#response-format)
- [Error Handling](#error-handling)
- [Example Requests](#example-requests)

---

## Authentication

All endpoints require authentication. Include the authentication token in your request headers:

```
Authorization: Bearer <your-access-token>
```

---

## Base URL

```
http://your-domain.com/campaigns/
```

---

## Available Campaigns

The following campaign types are available. Replace `{campaign-type}` in the URLs below with one of these:

1. `state-of-flock`
2. `soul-winning`
3. `servants-armed-trained`
4. `antibrutish`
5. `hearing-seeing`
6. `honour-your-prophet`
7. `basonta-proliferation`
8. `intimate-counseling`
9. `technology`
10. `sheperding-control`
11. `multiplication`
12. `understanding`
13. `sheep-seeking`
14. `testimony`
15. `telepastoring`
16. `gathering-bus`
17. `organised-creative-arts`
18. `tangerine`
19. `swollen-sunday`
20. `sunday-management`

---

## List Submissions by Campaign

### Endpoint

```
GET /campaigns/{campaign-type}/submissions/
```

### Query Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `campaign` | integer | No | Filter submissions by specific campaign ID |
| `start_date` | string (YYYY-MM-DD) | No | Filter submissions with submission_period >= start_date |
| `end_date` | string (YYYY-MM-DD) | No | Filter submissions with submission_period <= end_date |
| `page` | integer | No | Page number for pagination (default: 1) |
| `page_size` | integer | No | Number of results per page (default: 10) |

### Example Request

```javascript
// Get all testimony submissions
fetch('http://your-domain.com/campaigns/testimony/submissions/', {
  method: 'GET',
  headers: {
    'Authorization': 'Bearer your-token-here',
    'Content-Type': 'application/json'
  }
})

// Get submissions for a specific campaign
fetch('http://your-domain.com/campaigns/testimony/submissions/?campaign=5', {
  method: 'GET',
  headers: {
    'Authorization': 'Bearer your-token-here',
    'Content-Type': 'application/json'
  }
})
```

### Example Response

```json
{
  "count": 25,
  "next": "http://your-domain.com/campaigns/testimony/submissions/?page=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "campaign": 5,
      "submitted_by": 3,
      "submitted_by_name": "John Doe",
      "service": 2,
      "service_name": "Service Name",
      "submission_period": "2025-01-15",
      "date": "2025-01-15",
      "number_of_testimonies_shared": 5,
      "type_of_testimony_shared": "Healings and miracles",
      "created_at": "2025-01-15T10:30:00Z",
      "updated_at": "2025-01-15T10:30:00Z"
    },
    {
      "id": 2,
      "campaign": 5,
      "submitted_by": 4,
      "submitted_by_name": "Jane Smith",
      "service": 1,
      "service_name": "Another Service",
      "submission_period": "2025-01-20",
      "date": "2025-01-20",
      "number_of_testimonies_shared": 3,
      "type_of_testimony_shared": "Financial breakthrough",
      "created_at": "2025-01-20T14:45:00Z",
      "updated_at": "2025-01-20T14:45:00Z"
    }
  ]
}
```

### Submissions with Pictures

For campaigns that support picture uploads, the response includes a `pictures` array:

```json
{
  "id": 1,
  "campaign": 5,
  "submitted_by": 3,
  "submitted_by_name": "John Doe",
  "service": 2,
  "service_name": "Service Name",
  "submission_period": "2025-01-15",
  "date": "2025-01-15",
  "no_of_souls_won": 10,
  "no_of_crusades": 2,
  "pictures": [
    {
      "id": 1,
      "file": "http://your-domain.com/media/campaign_submissions/image1.jpg",
      "uploaded_at": "2025-01-15T10:30:00Z"
    },
    {
      "id": 2,
      "file": "http://your-domain.com/media/campaign_submissions/image2.jpg",
      "uploaded_at": "2025-01-15T10:31:00Z"
    }
  ],
  "created_at": "2025-01-15T10:30:00Z",
  "updated_at": "2025-01-15T10:30:00Z"
}
```

**Campaigns with Pictures:**
- Soul Winning
- Servants Armed and Trained
- Antibrutish
- Honour Your Prophet
- Basonta Proliferation
- Technology
- Multiplication
- Understanding
- Sheep Seeking
- Telepastoring
- Gathering Bus
- Swollen Sunday
- Sunday Management

---

## Get Submission Detail

### Endpoint

```
GET /campaigns/{campaign-type}/submissions/{submission-id}/
```

### Path Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `campaign-type` | string | Yes | The campaign type (see Available Campaigns) |
| `submission-id` | integer | Yes | The ID of the submission to retrieve |

### Example Request

```javascript
// Get specific testimony submission
fetch('http://your-domain.com/campaigns/testimony/submissions/42/', {
  method: 'GET',
  headers: {
    'Authorization': 'Bearer your-token-here',
    'Content-Type': 'application/json'
  }
})
```

### Example Response

```json
{
  "id": 42,
  "campaign": 5,
  "submitted_by": 3,
  "submitted_by_name": "John Doe",
  "service": 2,
  "service_name": "Service Name",
  "submission_period": "2025-01-15",
  "date": "2025-01-15",
  "number_of_testimonies_shared": 5,
  "type_of_testimony_shared": "Healings and miracles",
  "created_at": "2025-01-15T10:30:00Z",
  "updated_at": "2025-01-15T10:30:00Z"
}
```

---

## Date Range Filtering

### Using Start Date Only

Filter submissions from a specific date onwards:

```javascript
fetch('http://your-domain.com/campaigns/testimony/submissions/?start_date=2025-01-01', {
  method: 'GET',
  headers: {
    'Authorization': 'Bearer your-token-here',
    'Content-Type': 'application/json'
  }
})
```

This returns all submissions with `submission_period >= 2025-01-01`.

### Using End Date Only

Filter submissions up to a specific date:

```javascript
fetch('http://your-domain.com/campaigns/testimony/submissions/?end_date=2025-01-31', {
  method: 'GET',
  headers: {
    'Authorization': 'Bearer your-token-here',
    'Content-Type': 'application/json'
  }
})
```

This returns all submissions with `submission_period <= 2025-01-31`.

### Using Date Range

Filter submissions within a date range:

```javascript
fetch('http://your-domain.com/campaigns/testimony/submissions/?start_date=2025-01-01&end_date=2025-01-31', {
  method: 'GET',
  headers: {
    'Authorization': 'Bearer your-token-here',
    'Content-Type': 'application/json'
  }
})
```

This returns all submissions with `submission_period` between 2025-01-01 and 2025-01-31 (inclusive).

---

## Combined Filtering

You can combine all filters together:

### Campaign + Date Range

```javascript
fetch('http://your-domain.com/campaigns/testimony/submissions/?campaign=5&start_date=2025-01-01&end_date=2025-01-31', {
  method: 'GET',
  headers: {
    'Authorization': 'Bearer your-token-here',
    'Content-Type': 'application/json'
  }
})
```

This returns submissions for campaign ID 5 that were submitted between January 1-31, 2025.

---

## Response Format

### List Response Structure

```json
{
  "count": <total_count>,
  "next": <next_page_url_or_null>,
  "previous": <previous_page_url_or_null>,
  "results": [
    {
      // Submission object
    }
  ]
}
```

### Submission Object Structure

All submissions include these common fields:

| Field | Type | Description |
|-------|------|-------------|
| `id` | integer | Unique submission ID |
| `campaign` | integer | Campaign ID (read-only) |
| `submitted_by` | integer | User ID who submitted (read-only) |
| `submitted_by_name` | string | Full name of submitter (read-only) |
| `service` | integer | Service ID (read-only) |
| `service_name` | string | Service name (read-only) |
| `submission_period` | string (date) | The first day of the month this submission is for |
| `created_at` | string (datetime) | Creation timestamp (read-only) |
| `updated_at` | string (datetime) | Last update timestamp (read-only) |

Additional fields vary by campaign type. See your serializer definitions for complete field lists.

---

## Error Handling

### Common Error Responses

#### 401 Unauthorized

```json
{
  "detail": "Authentication credentials were not provided."
}
```

**Solution:** Include a valid authentication token in the Authorization header.

#### 404 Not Found

```json
{
  "detail": "Not found."
}
```

**Solution:** Check that the submission ID exists and the campaign type is correct.

#### 400 Bad Request

```json
{
  "campaign": ["This field is required."]
}
```

**Solution:** Provide all required fields when creating submissions.

---

## Example Requests

### React/JavaScript Examples

```javascript
// Function to get all submissions for a campaign
async function getCampaignSubmissions(campaignType, campaignId = null) {
  let url = `http://your-domain.com/campaigns/${campaignType}/submissions/`;
  
  if (campaignId) {
    url += `?campaign=${campaignId}`;
  }
  
  const response = await fetch(url, {
    method: 'GET',
    headers: {
      'Authorization': `Bearer ${localStorage.getItem('token')}`,
      'Content-Type': 'application/json'
    }
  });
  
  if (!response.ok) {
    throw new Error('Failed to fetch submissions');
  }
  
  return await response.json();
}

// Function to get submissions with date filter
async function getSubmissionsByDateRange(campaignType, startDate, endDate) {
  const url = `http://your-domain.com/campaigns/${campaignType}/submissions/?start_date=${startDate}&end_date=${endDate}`;
  
  const response = await fetch(url, {
    method: 'GET',
    headers: {
      'Authorization': `Bearer ${localStorage.getItem('token')}`,
      'Content-Type': 'application/json'
    }
  });
  
  if (!response.ok) {
    throw new Error('Failed to fetch submissions');
  }
  
  return await response.json();
}

// Function to get submission detail
async function getSubmissionDetail(campaignType, submissionId) {
  const url = `http://your-domain.com/campaigns/${campaignType}/submissions/${submissionId}/`;
  
  const response = await fetch(url, {
    method: 'GET',
    headers: {
      'Authorization': `Bearer ${localStorage.getItem('token')}`,
      'Content-Type': 'application/json'
    }
  });
  
  if (!response.ok) {
    throw new Error('Failed to fetch submission');
  }
  
  return await response.json();
}

// Usage examples
try {
  // Get all testimony submissions
  const allSubmissions = await getCampaignSubmissions('testimony');
  console.log('All submissions:', allSubmissions);
  
  // Get submissions for campaign ID 5
  const campaignSubmissions = await getCampaignSubmissions('testimony', 5);
  console.log('Campaign submissions:', campaignSubmissions);
  
  // Get submissions for January 2025
  const janSubmissions = await getSubmissionsByDateRange('testimony', '2025-01-01', '2025-01-31');
  console.log('January submissions:', janSubmissions);
  
  // Get specific submission
  const submission = await getSubmissionDetail('testimony', 42);
  console.log('Submission detail:', submission);
} catch (error) {
  console.error('Error:', error);
}
```

### Axios Examples

```javascript
import axios from 'axios';

// Setup axios instance with base config
const api = axios.create({
  baseURL: 'http://your-domain.com/campaigns',
  headers: {
    'Content-Type': 'application/json'
  }
});

// Add token to requests
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Get all submissions for a campaign
export const getCampaignSubmissions = async (campaignType, campaignId = null) => {
  const params = campaignId ? { campaign: campaignId } : {};
  const response = await api.get(`/${campaignType}/submissions/`, { params });
  return response.data;
};

// Get submissions with date filter
export const getSubmissionsByDateRange = async (campaignType, startDate, endDate, campaignId = null) => {
  const params = {
    start_date: startDate,
    end_date: endDate,
    ...(campaignId && { campaign: campaignId })
  };
  const response = await api.get(`/${campaignType}/submissions/`, { params });
  return response.data;
};

// Get submission detail
export const getSubmissionDetail = async (campaignType, submissionId) => {
  const response = await api.get(`/${campaignType}/submissions/${submissionId}/`);
  return response.data;
};
```

---

## Notes

1. **Date Format:** Always use `YYYY-MM-DD` format for dates (e.g., `2025-01-15`)
2. **Pagination:** Results are paginated. Use the `next` and `previous` URLs in the response to navigate pages
3. **Campaign Types:** Use the hyphenated campaign type names in URLs (e.g., `soul-winning`, not `soulWinning`)
4. **Read-Only Fields:** Fields like `id`, `campaign`, `submitted_by`, `created_at`, etc., are read-only and cannot be modified
5. **Pictures:** For campaigns that support pictures, the `pictures` array will be empty if no images were uploaded

---

## Quick Reference

### Get All Submissions
```
GET /campaigns/{campaign-type}/submissions/
```

### Get Submissions by Campaign
```
GET /campaigns/{campaign-type}/submissions/?campaign={campaign-id}
```

### Get Submissions by Date Range
```
GET /campaigns/{campaign-type}/submissions/?start_date={date}&end_date={date}
```

### Get Submission Detail
```
GET /campaigns/{campaign-type}/submissions/{submission-id}/
```

### Combined Filters
```
GET /campaigns/{campaign-type}/submissions/?campaign={campaign-id}&start_date={date}&end_date={date}
```

---

For more information or issues, contact your backend team.

## Campaign Submission POST Fields

- All submission endpoints require authentication.
- Provide `campaign` (integer ID) either in the request body or as a query param. The server will set it even though the serializer marks it read-only.
- Fields `submitted_by`, `service`, `id`, `created_at`, `updated_at` are set by the server.
- For endpoints that accept images, send as `multipart/form-data` and include `picture_files` as a list of image files.
- IMPORTANT: All non-image fields are REQUIRED. Image uploads (`picture_files`) are OPTIONAL.

### Common Fields for Most Submissions
- campaign: integer (required; body or query param)
- service: integer (required for Campaign Managers ONLY; auto-set for others)
  - Campaign Managers: Provide the ID of the service this submission is for
  - Pastors/Helpers: Do NOT provide this field (automatically set)
- submission_period: string($date) (required)
  The first day of the month this submission is for.
- date: string($date) (required)

Every submission type below includes the two common required date fields above; per-type lists only show additional fields.

---

### State of the Flock Submission
Endpoint: StateOfTheFlockSubmissionViewSet
- submission_period: string($date) (required)
  The first day of the month this submission is for.
- date: string($date) (required)
- total_membership: integer (required)
- lost: integer (required)
- stable: integer (required)
- unstable: integer (required)

### Soul Winning Submission
Endpoint: SoulWinningSubmissionViewSet (multipart supported)
- submission_period: string($date) (required)
  The first day of the month this submission is for.
- date: string($date) (required)
- no_of_crusades: integer (required)
- no_of_massive_organised_outreaches: integer (required)
- no_of_dance_outreach: integer (required)
- no_of_souls_won: integer (required)
- no_of_missionaries_in_training: integer (required)
- no_of_missionaries_sent: integer (required)
- picture_files: [image, ...] (optional)

### Servants Armed and Trained Submission
Endpoint: ServantsArmedTrainedSubmissionViewSet (multipart supported)
- submission_period: string($date) (required)
  The first day of the month this submission is for.
- date: string($date) (required)
- no_of_teachings_done_by_pastor: integer (required)
- average_attendance_during_meetings_by_pastor: integer (required)
- no_of_leaders_who_have_makarios: integer (required)
- no_of_leaders_who_own_dakes_bible: integer (required)
- no_of_leaders_who_own_thompson_chain: integer (required)
- no_of_pose_certified_leaders: integer (required)
- no_of_leaders_in_iptp_training: integer (required)
- picture_files: [image, ...] (optional)

### Antibrutish Submission
Endpoint: AntibrutishSubmissionViewSet (multipart supported)
- submission_period: string($date) (required)
  The first day of the month this submission is for.
- date: string($date) (required)
- type_of_prayer: string (required)
- hours_prayed: decimal (required)
- number_of_people_who_prayed: integer (required)
- picture_files: [image, ...] (optional)

### Hearing and Seeing Submission
Endpoint: HearingSeeingSubmissionViewSet
- submission_period: string($date) (required)
  The first day of the month this submission is for.
- date: string($date) (required)
- avg_number_of_leaders_that_join_flow: integer (required)
- no_of_people_subscribed_bishop_dag_youtube: integer (required)
- no_of_people_subscribed_es_joys_podcast: integer (required)
- no_of_messages_listened_to: integer (required)
- titles_of_messages_listened_to: text (required)

### Honour Your Prophet Submission
Endpoint: HonourYourProphetSubmissionViewSet (multipart supported)
- submission_period: string($date) (required)
  The first day of the month this submission is for.
- date: string($date) (required)
- no_of_people_who_honoured_with_offering: integer (required)
- activities_done_to_honour_prophet: text (required)
- picture_files: [image, ...] (optional)

### Basonta Proliferation Submission
Endpoint: BasontaProliferationSubmissionViewSet (multipart supported)
- submission_period: string($date) (required)
  The first day of the month this submission is for.
- date: string($date) (required)
- no_of_bacentas_at_beginning_of_month: integer (required)
- current_number_of_bacentas: integer (required)
- no_of_new_bacentas: integer (required)
- no_of_leaders_who_are_leavers: integer (required)
- no_of_replacements_new_leaders_available: integer (required)
- average_no_of_people_at_bacenta_meeting: integer (required)
- no_of_basontas: integer (required)
- average_number_of_people_at_basonta_meetings: integer (required)
- avg_no_of_members_saturday_service: integer (required)
- avg_no_of_members_sunday_service: integer (required)
- picture_files: [image, ...] (optional)

### Intimate Counseling Submission
Endpoint: IntimateCounselingSubmissionViewSet
- submission_period: string($date) (required)
  The first day of the month this submission is for.
- date: string($date) (required)
- total_number_of_members: integer (required)
- total_number_of_members_counseled: integer (required)
- no_of_members_counseled_via_calls: integer (required)
- no_of_members_counseled_in_person: integer (required)

### Technology Submission
Endpoint: TechnologySubmissionViewSet (multipart supported)
- submission_period: string($date) (required)
  The first day of the month this submission is for.
- date: string($date) (required)
- list_of_equipments_in_church: text (required)
- picture_files: [image, ...] (optional)

### Sheperding Control Submission
Endpoint: SheperdingControlSubmissionViewSet
- submission_period: string($date) (required)
  The first day of the month this submission is for.
- date: string($date) (required)
- current_no_of_leaders: integer (required)
- no_of_cos: integer (required)
- no_of_bos: integer (required)
- no_of_bls: integer (required)
- no_of_fls: integer (required)
- no_of_potential_leaders: integer (required)
- no_of_leaders_who_have_been_sacked: integer (required)

### Multiplication Submission
Endpoint: MultiplicationSubmissionViewSet (multipart supported)
- submission_period: string($date) (required)
  The first day of the month this submission is for.
- date: string($date) (required)
- no_of_outreaches: integer (required)
- type_of_outreaches: text (required)
- no_of_members_who_came_from_outreaches_to_church: integer (required)
- no_of_invites_done: integer (required)
- avg_number_of_people_invited_per_week: integer (required)
- picture_files: [image, ...] (optional)

### Understanding Submission
Endpoint: UnderstandingSubmissionViewSet (multipart supported)
- submission_period: string($date) (required)
  The first day of the month this submission is for.
- date: string($date) (required)
- lay_school_material_being_taught: string (required)
- no_of_lay_school_teachers: integer (required)
- average_attendance_at_lay_school_meeting: integer (required)
- picture_files: [image, ...] (optional)

### Sheep Seeking Submission
Endpoint: SheepSeekingSubmissionViewSet (multipart supported)
- submission_period: string($date) (required)
  The first day of the month this submission is for.
- date: string($date) (required)
- no_of_people_visited: integer (required)
- types_of_visits_done: text (required)
- no_of_idl_visits_done: integer (required)
- no_of_first_time_retained: integer (required)
- no_of_convert_visits_done: integer (required)
- no_of_converts_retained: integer (required)
- picture_files: [image, ...] (optional)

### Testimony Submission
Endpoint: TestimonySubmissionViewSet
- submission_period: string($date) (required)
  The first day of the month this submission is for.
- date: string($date) (required)
- number_of_testimonies_shared: integer (required)
- type_of_testimony_shared: text (required)

### Telepastoring Submission
Endpoint: TelepastoringSubmissionViewSet (multipart supported)
- submission_period: string($date) (required)
  The first day of the month this submission is for.
- date: string($date) (required)
- no_of_telepastors: integer (required)
- total_no_of_calls_made: integer (required)
- categories_of_people_called: text (required)
- picture_files: [image, ...] (optional)

### Gathering Bus Submission
Endpoint: GatheringBusSubmissionViewSet (multipart supported)
- submission_period: string($date) (required)
  The first day of the month this submission is for.
- date: string($date) (required)
- avg_number_of_members_bused: integer (required)
- avg_number_of_members_who_walk_in: integer (required)
- avg_number_of_buses_for_service: integer (required)
- avg_attendance_for_the_service: integer (required)
- avg_number_of_first_timers: integer (required)
- picture_files: [image, ...] (optional)

### Organised Creative Arts Submission
Endpoint: OrganisedCreativeArtsSubmissionViewSet
- submission_period: string($date) (required)
  The first day of the month this submission is for.
- date: string($date) (required)
- was_there_any_organisation_of_creative_arts: boolean (required)
- which_basonta_was_responsible: string (required)

### Tangerine Submission
Endpoint: TangerineSubmissionViewSet
- submission_period: string($date) (required)
  The first day of the month this submission is for.
- date: string($date) (required)
- no_of_tangerines: integer (required)
- types_of_tangerines: text (required)

### Swollen Sunday Submission
Endpoint: SwollenSundaySubmissionViewSet (multipart supported)
- submission_period: string($date) (required)
  The first day of the month this submission is for.
- date: string($date) (required)
- attendance_for_swollen_sunday: integer (required)
- no_of_converts_for_swollen_sunday: integer (required)
- picture_files: [image, ...] (optional)

### Sunday Management Submission
Endpoint: SundayManagementSubmissionViewSet (multipart supported)
- submission_period: string($date) (required)
  The first day of the month this submission is for.
- date: string($date) (required)
- month: date (required meaning month anchor; YYYY-MM-DD)
- no_of_meetings_per_month: integer (required)
- picture_files: [image, ...] (optional)

---

### Notes
- Required campaign parameter: pass `campaign` (ID) in body or as `?campaign=ID`.
- For image uploads, set header `Content-Type: multipart/form-data` and include `picture_files` as repeated parts or an array key depending on client.
- Date format: use ISO `YYYY-MM-DD`.
