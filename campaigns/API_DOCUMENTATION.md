# Campaigns API Documentation

This document describes the campaigns API endpoints for the SSMG Backend.

## Overview

The system supports 20 different campaign types, each with its own submission endpoint. All endpoints require authentication.

## Base URL

All campaign endpoints are prefixed with `/campaigns/`

## Endpoints

### 1. List All Campaigns

**GET** `/campaigns/all/`

Returns a unified list of all campaigns across all 20 campaign types.

**Query Parameters:**
- `status` (optional): Filter by campaign status (e.g., "ACTIVE", "INACTIVE")

**Response:**
```json
{
  "count": 20,
  "results": [
    {
      "id": 1,
      "name": "Sample Campaign",
      "description": "Campaign description",
      "icon": "http://example.com/media/icons/image.png",
      "campaign_id": "CAMP001",
      "status": "Active",
      "campaign_type": "Soul Winning",
      "created_at": "2025-01-01T00:00:00Z",
      "updated_at": "2025-01-01T00:00:00Z"
    }
  ]
}
```

---

## Campaign Submission Endpoints

Each campaign type has its own submission endpoints following REST conventions:

### General Pattern

For each campaign type, replace `{campaign-type}` with the appropriate campaign type slug:

- **GET** `/campaigns/{campaign-type}/submissions/` - List all submissions
- **POST** `/campaigns/{campaign-type}/submissions/` - Create a new submission
- **GET** `/campaigns/{campaign-type}/submissions/{id}/` - Retrieve a specific submission
- **PUT** `/campaigns/{campaign-type}/submissions/{id}/` - Update a submission
- **PATCH** `/campaigns/{campaign-type}/submissions/{id}/` - Partial update
- **DELETE** `/campaigns/{campaign-type}/submissions/{id}/` - Delete a submission

**Query Parameters:**
- `campaign` (optional): Filter submissions by campaign ID

---

## Campaign Types and Endpoints

### 1. State of the Flock
**Endpoint:** `/campaigns/state-of-flock/submissions/`

**Fields:**
- `campaign` (required): ID of the campaign
- `service` (optional): ID of the service
- `submission_period` (optional): Date field (YYYY-MM-DD)
- `date` (optional): Date field (YYYY-MM-DD)
- `total_membership` (optional): Integer
- `lost` (optional): Integer
- `stable` (optional): Integer
- `unstable` (optional): Integer

---

### 2. Soul Winning
**Endpoint:** `/campaigns/soul-winning/submissions/`

**Fields:**
- `campaign` (required): ID of the campaign
- `service` (optional): ID of the service
- `submission_period` (optional): Date field (YYYY-MM-DD)
- `date` (optional): Date field (YYYY-MM-DD)
- `no_of_crusades` (optional): Integer
- `no_of_massive_organised_outreaches` (optional): Integer
- `no_of_dance_outreach` (optional): Integer
- `no_of_souls_won` (optional): Integer
- `no_of_missionaries_in_training` (optional): Integer
- `no_of_missionaries_sent` (optional): Integer
- `picture_files` (optional): Array of image files

**Note:** Supports multipart/form-data for file uploads.

---

### 3. Servants Armed and Trained
**Endpoint:** `/campaigns/servants-armed-trained/submissions/`

**Fields:**
- `campaign` (required): ID of the campaign
- `service` (optional): ID of the service
- `submission_period` (optional): Date field (YYYY-MM-DD)
- `date` (optional): Date field (YYYY-MM-DD)
- `no_of_teachings_done_by_pastor` (optional): Integer
- `average_attendance_during_meetings_by_pastor` (optional): Integer
- `no_of_leaders_who_have_makarios` (optional): Integer
- `no_of_leaders_who_own_dakes_bible` (optional): Integer
- `no_of_leaders_who_own_thompson_chain` (optional): Integer
- `no_of_pose_certified_leaders` (optional): Integer
- `no_of_leaders_in_iptp_training` (optional): Integer
- `picture_files` (optional): Array of image files

---

### 4. Antibrutish
**Endpoint:** `/campaigns/antibrutish/submissions/`

**Fields:**
- `campaign` (required): ID of the campaign
- `service` (optional): ID of the service
- `submission_period` (optional): Date field (YYYY-MM-DD)
- `date` (optional): Date field (YYYY-MM-DD)
- `type_of_prayer` (required): String (max 500 chars)
- `hours_prayed` (required): Decimal (max 5 digits, 2 decimal places)
- `number_of_people_who_prayed` (optional): Integer
- `picture_files` (optional): Array of image files

---

### 5. Hearing and Seeing
**Endpoint:** `/campaigns/hearing-seeing/submissions/`

**Fields:**
- `campaign` (required): ID of the campaign
- `service` (optional): ID of the service
- `submission_period` (optional): Date field (YYYY-MM-DD)
- `date` (optional): Date field (YYYY-MM-DD)
- `avg_number_of_leaders_that_join_flow` (optional): Integer
- `no_of_people_subscribed_bishop_dag_youtube` (optional): Integer
- `no_of_people_subscribed_es_joys_podcast` (optional): Integer
- `no_of_messages_listened_to` (optional): Integer
- `titles_of_messages_listened_to` (optional): Text

---

### 6. Honour Your Prophet
**Endpoint:** `/campaigns/honour-your-prophet/submissions/`

**Fields:**
- `campaign` (required): ID of the campaign
- `service` (optional): ID of the service
- `submission_period` (optional): Date field (YYYY-MM-DD)
- `date` (optional): Date field (YYYY-MM-DD)
- `no_of_people_who_honoured_with_offering` (optional): Integer
- `activities_done_to_honour_prophet` (optional): Text
- `picture_files` (optional): Array of image files

---

### 7. Basonta Proliferation
**Endpoint:** `/campaigns/basonta-proliferation/submissions/`

**Fields:**
- `campaign` (required): ID of the campaign
- `service` (optional): ID of the service
- `submission_period` (optional): Date field (YYYY-MM-DD)
- `no_of_bacentas_at_beginning_of_month` (optional): Integer
- `current_number_of_bacentas` (optional): Integer
- `no_of_new_bacentas` (optional): Integer
- `no_of_leaders_who_are_leavers` (optional): Integer
- `no_of_replacements_new_leaders_available` (optional): Integer
- `average_no_of_people_at_bacenta_meeting` (optional): Integer
- `no_of_basontas` (optional): Integer
- `average_number_of_people_at_basonta_meetings` (optional): Integer
- `avg_no_of_members_saturday_service` (optional): Integer
- `avg_no_of_members_sunday_service` (optional): Integer
- `picture_files` (optional): Array of image files

---

### 8. Intimate Counseling
**Endpoint:** `/campaigns/intimate-counseling/submissions/`

**Fields:**
- `campaign` (required): ID of the campaign
- `service` (optional): ID of the service
- `submission_period` (optional): Date field (YYYY-MM-DD)
- `total_number_of_members` (optional): Integer
- `total_number_of_members_counseled` (optional): Integer
- `no_of_members_counseled_via_calls` (optional): Integer
- `no_of_members_counseled_in_person` (optional): Integer

---

### 9. Technology
**Endpoint:** `/campaigns/technology/submissions/`

**Fields:**
- `campaign` (required): ID of the campaign
- `service` (optional): ID of the service
- `submission_period` (optional): Date field (YYYY-MM-DD)
- `list_of_equipments_in_church` (optional): Text
- `picture_files` (optional): Array of image files

---

### 10. Sheperding Control
**Endpoint:** `/campaigns/sheperding-control/submissions/`

**Fields:**
- `campaign` (required): ID of the campaign
- `service` (optional): ID of the service
- `submission_period` (optional): Date field (YYYY-MM-DD)
- `current_no_of_leaders` (optional): Integer
- `no_of_cos` (optional): Integer
- `no_of_bos` (optional): Integer
- `no_of_bls` (optional): Integer
- `no_of_fls` (optional): Integer
- `no_of_potential_leaders` (required): Integer
- `no_of_leaders_who_have_been_sacked` (required): Integer

---

### 11. Multiplication
**Endpoint:** `/campaigns/multiplication/submissions/`

**Fields:**
- `campaign` (required): ID of the campaign
- `service` (optional): ID of the service
- `submission_period` (optional): Date field (YYYY-MM-DD)
- `date` (optional): Date field (YYYY-MM-DD)
- `no_of_outreaches` (optional): Integer
- `type_of_outreaches` (optional): Text
- `no_of_members_who_came_from_outreaches_to_church` (optional): Integer
- `no_of_invites_done` (optional): Integer
- `avg_number_of_people_invited_per_week` (optional): Integer
- `picture_files` (optional): Array of image files

---

### 12. Understanding
**Endpoint:** `/campaigns/understanding/submissions/`

**Fields:**
- `campaign` (required): ID of the campaign
- `service` (optional): ID of the service
- `submission_period` (optional): Date field (YYYY-MM-DD)
- `date` (optional): Date field (YYYY-MM-DD)
- `lay_school_material_being_taught` (required): String (max 200 chars)
- `no_of_lay_school_teachers` (optional): Integer
- `average_attendance_at_lay_school_meeting` (optional): Integer
- `picture_files` (optional): Array of image files

---

### 13. Sheep Seeking
**Endpoint:** `/campaigns/sheep-seeking/submissions/`

**Fields:**
- `campaign` (required): ID of the campaign
- `service` (optional): ID of the service
- `submission_period` (optional): Date field (YYYY-MM-DD)
- `date` (optional): Date field (YYYY-MM-DD)
- `no_of_people_visited` (optional): Integer
- `types_of_visits_done` (optional): Text
- `no_of_idl_visits_done` (optional): Integer
- `no_of_first_time_retained` (optional): Integer
- `no_of_convert_visits_done` (optional): Integer
- `no_of_converts_retained` (optional): Integer
- `picture_files` (optional): Array of image files

---

### 14. Testimony
**Endpoint:** `/campaigns/testimony/submissions/`

**Fields:**
- `campaign` (required): ID of the campaign
- `service` (optional): ID of the service
- `submission_period` (optional): Date field (YYYY-MM-DD)
- `date` (optional): Date field (YYYY-MM-DD)
- `number_of_testimonies_shared` (optional): Integer
- `type_of_testimony_shared` (optional): Text

---

### 15. Telepastoring
**Endpoint:** `/campaigns/telepastoring/submissions/`

**Fields:**
- `campaign` (required): ID of the campaign
- `service` (optional): ID of the service
- `submission_period` (optional): Date field (YYYY-MM-DD)
- `date` (optional): Date field (YYYY-MM-DD)
- `no_of_telepastors` (optional): Integer
- `total_no_of_calls_made` (optional): Integer
- `categories_of_people_called` (optional): Text
- `picture_files` (optional): Array of image files

---

### 16. Gathering Bus
**Endpoint:** `/campaigns/gathering-bus/submissions/`

**Fields:**
- `campaign` (required): ID of the campaign
- `service` (optional): ID of the service
- `submission_period` (optional): Date field (YYYY-MM-DD)
- `date` (optional): Date field (YYYY-MM-DD)
- `avg_number_of_members_bused` (optional): Integer
- `avg_number_of_members_who_walk_in` (optional): Integer
- `avg_number_of_buses_for_service` (optional): Integer
- `avg_attendance_for_the_service` (optional): Integer
- `avg_number_of_first_timers` (optional): Integer
- `picture_files` (optional): Array of image files

---

### 17. Organised Creative Arts
**Endpoint:** `/campaigns/organised-creative-arts/submissions/`

**Fields:**
- `campaign` (required): ID of the campaign
- `service` (optional): ID of the service
- `submission_period` (optional): Date field (YYYY-MM-DD)
- `date` (optional): Date field (YYYY-MM-DD)
- `was_there_any_organisation_of_creative_arts` (optional): Boolean
- `which_basonta_was_responsible` (optional): String (max 200 chars)

---

### 18. Tangerine
**Endpoint:** `/campaigns/tangerine/submissions/`

**Fields:**
- `campaign` (required): ID of the campaign
- `service` (optional): ID of the service
- `submission_period` (optional): Date field (YYYY-MM-DD)
- `date` (optional): Date field (YYYY-MM-DD)
- `no_of_tangerines` (optional): Integer
- `types_of_tangerines` (optional): Text

---

### 19. Swollen Sunday
**Endpoint:** `/campaigns/swollen-sunday/submissions/`

**Fields:**
- `campaign` (required): ID of the campaign
- `service` (optional): ID of the service
- `submission_period` (optional): Date field (YYYY-MM-DD)
- `attendance_for_swollen_sunday` (optional): Integer
- `no_of_converts_for_swollen_sunday` (optional): Integer
- `picture_files` (optional): Array of image files

---

### 20. Sunday Management
**Endpoint:** `/campaigns/sunday-management/submissions/`

**Fields:**
- `campaign` (required): ID of the campaign
- `service` (optional): ID of the service
- `submission_period` (optional): Date field (YYYY-MM-DD)
- `month` (required): Date field (YYYY-MM-DD) - Month this submission is for
- `no_of_meetings_per_month` (optional): Integer
- `picture_files` (optional): Array of image files

---

## Authentication

All endpoints require authentication. Include the authentication token in the request headers:

```
Authorization: Bearer <your-token>
```

Or use the appropriate authentication method configured in your Django REST Framework settings.

---

## Common Fields in All Submissions

All submission serializers include these read-only fields:
- `id`: Unique identifier for the submission
- `submitted_by`: ID of the user who submitted (auto-populated from request)
- `submitted_by_name`: Full name of the user who submitted
- `service_name`: Name of the service
- `created_at`: Timestamp when the submission was created
- `updated_at`: Timestamp when the submission was last updated

---

## Example: Creating a Soul Winning Submission

**Request:**
```http
POST /campaigns/soul-winning/submissions/
Content-Type: multipart/form-data
Authorization: Bearer <your-token>

{
  "campaign": 1,
  "service": 5,
  "submission_period": "2025-10-01",
  "date": "2025-10-15",
  "no_of_crusades": 3,
  "no_of_souls_won": 25,
  "picture_files": [<file1>, <file2>]
}
```

**Response:**
```json
{
  "id": 1,
  "campaign": 1,
  "submitted_by": 10,
  "submitted_by_name": "John Doe",
  "service": 5,
  "service_name": "Downtown Service",
  "submission_period": "2025-10-01",
  "date": "2025-10-15",
  "no_of_crusades": 3,
  "no_of_massive_organised_outreaches": null,
  "no_of_dance_outreach": null,
  "no_of_souls_won": 25,
  "no_of_missionaries_in_training": null,
  "no_of_missionaries_sent": null,
  "pictures": [
    {
      "id": 1,
      "file": "http://example.com/media/campaign_submissions/file1.jpg",
      "uploaded_at": "2025-10-18T12:00:00Z"
    }
  ],
  "created_at": "2025-10-18T12:00:00Z",
  "updated_at": "2025-10-18T12:00:00Z"
}
```

---

## Notes

1. **File Uploads**: Endpoints that support file uploads use `picture_files` as a write-only field and return the uploaded files in the `pictures` field.

2. **Pagination**: List endpoints are paginated using the `DefaultPagination` class.

3. **Filtering**: You can filter submissions by campaign ID using the `?campaign=<id>` query parameter.

4. **Auto-populated Fields**: The `submitted_by` field is automatically populated from the authenticated user making the request.

5. **Date Formats**: All dates should be in ISO 8601 format (YYYY-MM-DD).

---

## API Exploration

You can explore the API interactively using:
- Swagger UI: `/api/docs/`
- ReDoc: `/api/schema/redoc/`
- OpenAPI Schema: `/api/schema/`

