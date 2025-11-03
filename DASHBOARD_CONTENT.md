# Mobile App Dashboard Content

This document contains ready-to-use content for your mobile app dashboard, tailored to match your actual UI structure.

---

## 🔍 Header Section

### Search Bar Placeholder
```
"Help others..."
```
**Note:** This appears in the search input field. Users can search for campaigns, submissions, or other content.

### Search Bar Helper Text
```
Search campaigns, submissions, or members
```

---

## 🏠 Your Service Card

### Card Title
```
Your Service
```

### Service Name Display
**Format:** Display the user's service name as received from API
**Fallback:** `"No Service Assigned"` if service is null

### Location Display
**Prefix Icon:** 📍 Location pin icon
**Format:** `{service_location}`
**Fallback:** `"Location not specified"` if location is null
**Example:**
```
📍 Accra Central
```

### Total Members Badge
**Label:** `"Total Members"`
**Value:** Display total_members from service data
**Format:** `{number} members`
**Example:**
```
Total Members
1,250 members
```

### Empty State (No Service)
```
No Service Assigned

You haven't been assigned to a service yet. Please contact your administrator.
```

---

## 📊 Statistics Cards

### Active Campaigns Card
**Title:** `Active Campaigns`
**Value:** Display count from API (statistics.active_campaigns)
**Icon:** 🎯 Target icon
**Subtitle/Description:** `"Currently participating"`
**Color:** Yellow accent (#FFC107 or your brand yellow)

**Empty State:**
```
Active Campaigns
0
Start participating in campaigns
```

**With Data:**
```
Active Campaigns
5
Currently participating
```

### Monthly Submissions Card
**Title:** `Monthly Submissions`
**Value:** Display count from API (statistics.submissions_this_month)
**Icon:** 📝 File-text icon
**Subtitle/Description:** `"This month's reports"`
**Color:** Yellow accent (#FFC107 or your brand yellow)

**Empty State:**
```
Monthly Submissions
0
No submissions this month
```

**With Data:**
```
Monthly Submissions
12
This month's reports
```

---

## 📋 Recent Submissions Section

### Section Header
**Title:** `Recent Submissions`
**Subtitle:** `"Your latest activity"`

### Card Content Structure
Each submission card should display:

**Campaign Type Label:**
- Display the `campaign_type` from API (e.g., "Soul Winning", "State of the Flock")
- Style as a small badge/chip above the submission name
- Use appropriate color coding per campaign type

**Submission Name:**
- Display `campaign_name` from API
- Primary text, bold or semi-bold
- Truncate if too long with ellipsis



**Submission Count:**
- Display count of submissions for this campaign
- Format: `{count} submissions`
- Position below or beside progress bar

### Example Card Data Structure
```
Campaign Type: "Soul Winning"
Campaign Name: "Youth Outreach Program"
Submissions: 188 submissions
```

### Sample Placeholder Data (if no data from API)
**Card 1:**
```
Youth Attendance Survey
188 submissions
```

**Card 2:**
```
Community Outreach Data
113 submissions
```

**Card 3:**
```
Prayer Request Form
225 submissions
```

### Empty State
```
No Recent Submissions

You haven't submitted any reports recently. Start tracking your ministry activities today.

[Browse Campaigns Button]
```

### Loading State
```
Loading recent submissions...
```

---

## 🎯 Active Campaigns Section

### Section Header
**Title:** `Active Campaigns`
**Subtitle:** `"Campaigns in progress"`

### Card Content Structure
Each campaign card should display:

**Campaign Type:**
- Display the `campaign_type` from API
- Style as a badge/chip
- Use campaign-specific color coding

**Campaign Name:**
- Display `campaign.name` from API
- Primary text, bold or semi-bold
- Truncate if too long

**Progress Bar:**
- Calculate: `(submission_count / target_responses) * 100`
- Show percentage: `{percentage}% progress`
- Visual progress bar with fill color
- Target: Use `target` value from campaign data or calculate based on campaign type

**Target Response Count:**
- Display: `Target: {number} responses`
- Or show: `{current}/{target} responses`
- Position below progress bar

### Example Card Data Structure
```
Campaign Type: "Testimony"
Campaign Name: "Member Registration"
Progress: 60% progress
Target: 300 responses
```

### Sample Placeholder Data (if no data from API)
**Card 1:**
```
Member Registration
60% progress
Target: 300 responses
```

**Card 2:**
```
Event Feedback
35% progress
Target: 200 responses
```

**Card 3:**
```
Ministry Preferences
80% progress
Target: 150 responses
```

### Empty State
```
No Active Campaigns

You're not currently participating in any campaigns. Explore available campaigns to get started.

[View All Campaigns Button]
```

### Loading State
```
Loading active campaigns...
```

---

## 🔔 Notification Icon Badge

### Notification Badge Content
- Show badge count if user has unread notifications
- Badge should display number of unread items
- Clear badge when notifications are read

---

## 📱 Empty States & Error Messages

### No Data Available
```
No Data Available

We're having trouble loading your dashboard data. Please check your connection and try again.

[Retry Button]
```

### Network Error
```
Connection Error

Unable to connect to the server. Please check your internet connection.

[Retry Button]
```

### Loading States (Skeleton Loaders)
- Show skeleton loaders for all cards during data fetch
- Simulate 2-second loading time
- Display placeholders that match the actual card structure

---

## 🎨 Content for Campaign Types (Badge Labels)

Use these labels for campaign type badges in Recent Submissions and Active Campaigns:

1. `State of the Flock`
2. `Soul Winning`
3. `Servants Armed & Trained`
4. `Antibrutish`
5. `Hearing & Seeing`
6. `Honour Your Prophet`
7. `Basonta Proliferation`
8. `Intimate Counseling`
9. `Technology`
10. `Sheperding Control`
11. `Multiplication`
12. `Understanding`
13. `Sheep Seeking`
14. `Testimony`
15. `Telepastoring`
16. `Gathering Bus`
17. `Creative Arts`
18. `Tangerine`
19. `Swollen Sunday`
20. `Sunday Management`

---

## 📊 Progress Calculation Logic

### For Recent Submissions
If target is not available in API, use these default targets based on campaign type:
- **Soul Winning:** 250 responses
- **State of the Flock:** 200 responses
- **Testimony:** 150 responses
- **Multiplication:** 300 responses
- **Others:** 200 responses (default)

**Calculation:**
```javascript
const progress = (submissionCount / targetCount) * 100;
const displayProgress = Math.min(progress, 100); // Cap at 100%
```

### For Active Campaigns
Use the target value from campaign data if available, otherwise use default targets above.

---

## 🎨 Visual Guidelines

### Colors
- **Primary Accent:** Yellow (#FFC107 or your brand yellow)
- **Progress Bar Fill:** Green (#4CAF50) for good progress, Yellow for medium, Orange for low
- **Background:** White/light gray for cards
- **Text:** Dark gray/black for primary text, medium gray for secondary

### Typography
- **Card Titles:** Bold, 16-18px
- **Values/Counts:** Bold, 20-24px
- **Labels:** Regular, 12-14px
- **Progress Text:** Regular, 12-14px

### Spacing
- Card padding: 16px
- Card margin: 8-12px
- Section spacing: 24px between sections

---

## 🔄 Refresh & Pull-to-Refresh

### Pull-to-Refresh Message
```
Pull to refresh
Release to update dashboard
```

### Refreshing State
```
Refreshing...
```

### Refresh Success (Optional)
```
Dashboard updated
```

---

## 📝 API Data Mapping

### Your Service Card
- `service_name` → Service Name
- `service.location` → Location
- `service.total_members` → Total Members

### Statistics Cards
- `statistics.active_campaigns` → Active Campaigns count
- `statistics.submissions_this_month` → Monthly Submissions count

### Recent Submissions
- `recent_submissions[]` array
  - `campaign_type` → Campaign Type badge
  - `campaign_name` → Submission Name
  - Calculate progress from preview_data or use defaults
  - Use submission count from preview_data if available

### Active Campaigns
- `recent_campaigns[]` array
  - `campaign_type` → Campaign Type badge
  - `name` → Campaign Name
  - Calculate progress (may need to fetch submission count separately)
  - Use target from campaign data

---

## 💡 Additional Tips

### Handling Missing Data
- Always provide fallback values for missing data
- Show empty states when arrays are empty
- Display "N/A" or "Not specified" for missing individual fields

### Progress Bar Colors
- **0-30%:** Orange/Red (needs attention)
- **31-70%:** Yellow (in progress)
- **71-100%:** Green (good progress)
- **100%+:** Blue (completed/exceeded)

### Campaign Type Colors
You can assign colors to campaign types for better visual distinction:
- Soul Winning: Purple
- State of the Flock: Blue
- Testimony: Gold
- Antibrutish: Red
- Others: Use a color palette that provides good contrast

---

This content matches your actual UI structure. Use the placeholders and format them with actual data from your API responses.