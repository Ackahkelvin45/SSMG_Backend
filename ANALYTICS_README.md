# Church Growth Analytics & Visualizations

This document outlines analytics metrics and visualizations that can be implemented in the mobile app dashboard based on campaign submission data. All metrics are derived from actual submission fields across the 20 campaign types.

---

## 📊 Analytics Categories

### 1. **Membership Growth Analytics**
### 2. **Outreach & Evangelism Analytics**
### 3. **Leadership Development Analytics**
### 4. **Small Group Growth Analytics**
### 5. **Member Engagement Analytics**
### 6. **Service Attendance Analytics**
### 7. **Member Care Analytics**
### 8. **Spiritual Development Analytics**
### 9. **Overall Growth Score**

---

## 1. Membership Growth Analytics

### Data Source: State of the Flock Campaign

**Key Metrics:**
- `total_membership` - Total church membership
- `stable` - Number of stable members
- `unstable` - Number of unstable members
- `lost` - Number of members lost

### Visualizations:

#### 1.1 Membership Trend Line Chart
**Type:** Line Chart
**X-Axis:** Submission periods (months)
**Y-Axis:** Total membership count
**Data Points:**
- Total membership over time
- Stable members over time
- Unstable members over time

**API Calculation:**
```python
# Get all State of the Flock submissions grouped by submission_period
# Return: {period: "2025-01", total_membership: 150, stable: 120, unstable: 25, lost: 5}
```

#### 1.2 Membership Composition Pie Chart
**Type:** Pie/Donut Chart
**Sections:**
- Stable members (green)
- Unstable members (yellow)
- Lost members (red)

**API Calculation:**
```python
# Get latest State of the Flock submission
# Calculate percentages: stable%, unstable%, lost%
```

#### 1.3 Growth Rate Card
**Type:** Stat Card
**Metrics:**
- Current total membership
- Growth from last month (absolute and percentage)
- Net growth (new - lost)

**API Calculation:**
```python
# Compare current month with previous month
growth = current_total - previous_total
growth_percentage = (growth / previous_total) * 100
```

---

## 2. Outreach & Evangelism Analytics

### Data Sources:
- **Soul Winning Campaign**
- **Multiplication Campaign**
- **Sheep Seeking Campaign**
- **Swollen Sunday Campaign**

### Key Metrics:

#### Soul Winning:
- `no_of_souls_won`
- `no_of_crusades`
- `no_of_massive_organised_outreaches`
- `no_of_dance_outreach`
- `no_of_missionaries_sent`

#### Multiplication:
- `no_of_outreaches`
- `no_of_members_who_came_from_outreaches_to_church`
- `no_of_invites_done`
- `avg_number_of_people_invited_per_week`

#### Sheep Seeking:
- `no_of_people_visited`
- `no_of_first_time_retained`
- `no_of_converts_retained`

#### Swollen Sunday:
- `attendance_for_swollen_sunday`
- `no_of_converts_for_swollen_sunday`

### Visualizations:

#### 2.1 Souls Won Over Time
**Type:** Line Chart / Area Chart
**X-Axis:** Months
**Y-Axis:** Number of souls won
**Series:**
- Total souls won per month
- Cumulative souls won (running total)

#### 2.2 Outreach Activities Bar Chart
**Type:** Stacked Bar Chart
**X-Axis:** Months
**Y-Axis:** Count
**Stacks:**
- Crusades
- Massive outreaches
- Dance outreaches
- Visits

#### 2.3 Conversion Funnel
**Type:** Funnel Chart
**Stages:**
1. People Visited (Sheep Seeking)
2. First Time Visitors Retained
3. Converts Retained
4. Souls Won (Soul Winning)
5. Members from Outreaches (Multiplication)

#### 2.4 Outreach Impact Card
**Type:** Stat Cards (Grid)
**Metrics:**
- Total souls won (all time)
- Souls won this month
- Outreaches conducted this month
- New members from outreaches

---

## 3. Leadership Development Analytics

### Data Sources:
- **Servants Armed and Trained Campaign**
- **Sheperding Control Campaign**

### Key Metrics:

#### Servants Armed and Trained:
- `no_of_teachings_done_by_pastor`
- `average_attendance_during_meetings_by_pastor`
- `no_of_leaders_who_have_makarios`
- `no_of_leaders_who_own_dakes_bible`
- `no_of_leaders_who_own_thompson_chain`
- `no_of_pose_certified_leaders`
- `no_of_leaders_in_iptp_training`

#### Sheperding Control:
- `current_no_of_leaders`
- `no_of_cos` (Chief Officers)
- `no_of_bos` (Branch Officers)
- `no_of_bls` (Branch Leaders)
- `no_of_fls` (Flock Leaders)
- `no_of_potential_leaders`

### Visualizations:

#### 3.1 Leadership Hierarchy Chart
**Type:** Pyramid Chart / Organizational Chart
**Levels (bottom to top):**
- Potential Leaders
- FLs (Flock Leaders)
- BLs (Branch Leaders)
- BOs (Branch Officers)
- COs (Chief Officers)

#### 3.2 Leader Development Progress
**Type:** Progress Bars / Gauge Charts
**Metrics:**
- Leaders with Makarios (%)
- Leaders with Dake's Bible (%)
- Leaders with Thompson Chain (%)
- POSE Certified Leaders (%)
- Leaders in IPTP Training (%)

#### 3.3 Training Activity Chart
**Type:** Bar Chart
**X-Axis:** Months
**Y-Axis:** Count
**Metrics:**
- Number of teachings done
- Average attendance at training
- Leaders trained this month

---

## 4. Small Group Growth Analytics

### Data Source: Basonta Proliferation Campaign

### Key Metrics:
- `no_of_bacentas_at_beginning_of_month`
- `current_number_of_bacentas`
- `no_of_new_bacentas`
- `no_of_basontas`
- `average_no_of_people_at_bacenta_meeting`
- `average_number_of_people_at_basonta_meetings`
- `avg_no_of_members_saturday_service`
- `avg_no_of_members_sunday_service`

### Visualizations:

#### 4.1 Small Group Growth Trend
**Type:** Dual Line Chart
**X-Axis:** Months
**Y-Axis:** Count
**Lines:**
- Bacentas over time
- Basontas over time

#### 4.2 Group Growth Rate
**Type:** Stat Card
**Metrics:**
- Current bacentas
- New bacentas this month
- Growth rate (%)
- Average attendance per group

#### 4.3 Service Attendance Comparison
**Type:** Comparison Chart (Bar/Line)
**Series:**
- Saturday service average attendance
- Sunday service average attendance
- Bacenta meeting average
- Basonta meeting average

---

## 5. Member Engagement Analytics

### Data Sources:
- **Hearing and Seeing Campaign**
- **Testimony Campaign**
- **Understanding Campaign**

### Key Metrics:

#### Hearing and Seeing:
- `avg_number_of_leaders_that_join_flow`
- `no_of_people_subscribed_bishop_dag_youtube`
- `no_of_people_subscribed_es_joys_podcast`
- `no_of_messages_listened_to`

#### Testimony:
- `number_of_testimonies_shared`

#### Understanding:
- `no_of_lay_school_teachers`
- `average_attendance_at_lay_school_meeting`

### Visualizations:

#### 5.1 Digital Engagement Chart
**Type:** Stacked Area Chart
**X-Axis:** Months
**Y-Axis:** Count
**Layers:**
- YouTube subscribers
- Podcast subscribers
- Messages listened to

#### 5.2 Engagement Activity
**Type:** Bar Chart
**Metrics:**
- Testimonies shared this month
- Lay school attendance
- Leaders in flow

---

## 6. Service Attendance Analytics

### Data Sources:
- **Gathering Bus Campaign**
- **Swollen Sunday Campaign**
- **Sunday Management Campaign**

### Key Metrics:

#### Gathering Bus:
- `avg_attendance_for_the_service`
- `avg_number_of_members_bused`
- `avg_number_of_members_who_walk_in`
- `avg_number_of_first_timers`
- `avg_number_of_buses_for_service`

#### Sunday Management:
- `no_of_meetings_per_month`

### Visualizations:

#### 6.1 Attendance Trend
**Type:** Line Chart
**X-Axis:** Months/Weeks
**Y-Axis:** Attendance count
**Series:**
- Average service attendance
- Members bused
- Walk-in members
- First timers

#### 6.2 Transportation vs Walk-in
**Type:** Comparison Pie Chart
**Sections:**
- Members bused (%)
- Walk-in members (%)

#### 6.3 First Timer Growth
**Type:** Line Chart
**Shows:** New visitors trend over time

---

## 7. Member Care Analytics

### Data Sources:
- **Intimate Counseling Campaign**
- **Telepastoring Campaign**

### Key Metrics:

#### Intimate Counseling:
- `total_number_of_members`
- `total_number_of_members_counseled`
- `no_of_members_counseled_via_calls`
- `no_of_members_counseled_in_person`

#### Telepastoring:
- `no_of_telepastors`
- `total_no_of_calls_made`

### Visualizations:

#### 7.1 Counseling Coverage Chart
**Type:** Gauge Chart / Progress Circle
**Metric:** Percentage of members counseled
**Calculation:** `(total_counseled / total_members) * 100`

#### 7.2 Counseling Methods Comparison
**Type:** Stacked Bar Chart
**Series:**
- In-person counseling
- Call counseling

#### 7.3 Pastoral Care Activity
**Type:** Stat Cards
**Metrics:**
- Total calls made
- Members counseled this month
- Counseling coverage percentage

---

## 8. Spiritual Development Analytics

### Data Sources:
- **Antibrutish Campaign** (Prayer)
- **Honour Your Prophet Campaign**

### Key Metrics:

#### Antibrutish:
- `hours_prayed`
- `number_of_people_who_prayed`

#### Honour Your Prophet:
- `no_of_people_who_honoured_with_offering`

### Visualizations:

#### 8.1 Prayer Activity Chart
**Type:** Area Chart
**X-Axis:** Months
**Y-Axis:** Hours
**Metric:** Total hours prayed per month

#### 8.2 Prayer Participation
**Type:** Line Chart
**Shows:** Number of people participating in prayer over time

---

## 9. Overall Growth Score Dashboard

### Composite Metrics:

#### 9.1 Growth Score Card
**Type:** Large Stat Card with Trend Indicator
**Calculation:**
```
Growth Score = Weighted average of:
- Membership Growth (30%)
- Soul Winning (25%)
- Leadership Development (20%)
- Small Group Growth (15%)
- Member Engagement (10%)
```

**Visual:** Large number with up/down arrow and percentage change

#### 9.2 Growth Radar Chart
**Type:** Radar/Spider Chart
**Axes:**
1. Membership Growth
2. Soul Winning
3. Leadership Development
4. Small Groups
5. Member Engagement
6. Attendance
7. Member Care

**Values:** Normalized scores (0-100) for each category

#### 9.3 Month-over-Month Comparison
**Type:** Bar Chart (Grouped)
**Groups:** This Month vs Last Month
**Metrics:** Key indicators side by side

---

## 📱 Mobile App Dashboard Layout Suggestions

### Analytics Section Structure:

```
┌─────────────────────────────────┐
│   Growth Overview               │
│   [Growth Score Card]           │
└─────────────────────────────────┘

┌─────────────────────────────────┐
│   Key Metrics (Quick View)      │
│   [4-6 Stat Cards in Grid]     │
│   - Total Membership            │
│   - Souls Won (This Month)     │
│   - Active Leaders              │
│   - Small Groups                │
└─────────────────────────────────┘

┌─────────────────────────────────┐
│   Membership Growth             │
│   [Trend Line Chart]            │
│   [Growth Rate Card]            │
└─────────────────────────────────┘

┌─────────────────────────────────┐
│   Outreach Impact               │
│   [Souls Won Chart]             │
│   [Outreach Activities]         │
└─────────────────────────────────┘

┌─────────────────────────────────┐
│   Leadership Development         │
│   [Hierarchy Chart]             │
│   [Training Progress]           │
└─────────────────────────────────┘

┌─────────────────────────────────┐
│   Small Groups                  │
│   [Growth Trend]               │
│   [Attendance Comparison]       │
└─────────────────────────────────┘
```

---

## 🔢 API Endpoint Structure

### Suggested Endpoint:

```
GET /auth/users/analytics/
```

### Query Parameters:
- `period`: `month`, `quarter`, `year`, `all` (default: `month`)
- `start_date`: Start date for custom range (YYYY-MM-DD)
- `end_date`: End date for custom range (YYYY-MM-DD)
- `metrics`: Comma-separated list of specific metrics to include

### Response Structure:

```json
{
  "period": {
    "type": "month",
    "start": "2025-01-01",
    "end": "2025-01-31"
  },
  "growth_score": 75.5,
  "membership": {
    "current": 1250,
    "previous": 1200,
    "growth": 50,
    "growth_percentage": 4.17,
    "stable": 1000,
    "unstable": 200,
    "lost": 50,
    "trend": [
      {"period": "2025-01", "total": 1250, "stable": 1000},
      {"period": "2024-12", "total": 1200, "stable": 950}
    ]
  },
  "soul_winning": {
    "total_all_time": 500,
    "this_period": 25,
    "crusades": 3,
    "outreaches": 5,
    "trend": [
      {"period": "2025-01", "souls_won": 25},
      {"period": "2024-12", "souls_won": 30}
    ]
  },
  "leadership": {
    "total_leaders": 45,
    "trained_leaders": 35,
    "teaching_sessions": 12,
    "hierarchy": {
      "cos": 5,
      "bos": 10,
      "bls": 15,
      "fls": 15
    }
  },
  "small_groups": {
    "bacentas": 25,
    "basontas": 50,
    "new_groups": 3,
    "avg_attendance": 15
  },
  "attendance": {
    "avg_service": 850,
    "avg_saturday": 200,
    "avg_sunday": 950,
    "first_timers": 25
  },
  "engagement": {
    "youtube_subscribers": 150,
    "podcast_subscribers": 200,
    "testimonies_shared": 15
  },
  "member_care": {
    "members_counseled": 120,
    "counseling_coverage": 9.6,
    "calls_made": 300
  },
  "prayer": {
    "hours_prayed": 150.5,
    "participants": 45
  }
}
```

---

## 📈 Specific Metrics Calculations

### Membership Growth Rate
```python
# Get latest and previous month submissions
current = latest_submission.total_membership
previous = previous_submission.total_membership
growth_rate = ((current - previous) / previous) * 100
```

### Soul Winning Conversion Rate
```python
# From Multiplication and Soul Winning campaigns
conversion_rate = (souls_won / people_visited) * 100
```

### Leadership Development Index
```python
# Weighted score based on various training metrics
index = (
    (leaders_with_makarios / total_leaders) * 30 +
    (pose_certified / total_leaders) * 25 +
    (iptp_training / total_leaders) * 25 +
    (own_dakes_bible / total_leaders) * 20
)
```

### Small Group Health Score
```python
# Based on growth and attendance
health_score = (
    (new_groups / current_groups) * 50 +
    (avg_attendance / target_attendance) * 50
)
```

### Member Engagement Score
```python
engagement = (
    (youtube_subs / total_members) * 30 +
    (podcast_subs / total_members) * 30 +
    (testimonies_shared / total_members) * 40
)
```

---

## 🎨 Visualization Recommendations

### Chart Types by Use Case:

1. **Trends Over Time:** Line Charts, Area Charts
2. **Comparisons:** Bar Charts, Column Charts
3. **Composition:** Pie Charts, Donut Charts
4. **Hierarchy:** Pyramid Charts, Tree Charts
5. **Progress:** Gauge Charts, Progress Bars
6. **Multiple Metrics:** Radar Charts, Dashboard Cards
7. **Funnels:** Funnel Charts for conversion tracking

### Color Scheme Suggestions:
- **Growth/Positive:** Green (#4CAF50)
- **Neutral:** Blue (#2196F3)
- **Warning:** Yellow/Orange (#FF9800)
- **Decline/Negative:** Red (#F44336)
- **Accent:** Purple (#9C27B0)

---

## 📊 Priority Metrics for Initial Implementation

### High Priority (Phase 1):
1. ✅ Membership Growth Trend
2. ✅ Total Souls Won (All-time & Monthly)
3. ✅ Current Total Membership
4. ✅ Growth Score Card
5. ✅ Active Campaigns Count

### Medium Priority (Phase 2):
6. Leadership Development Progress
7. Small Group Growth
8. Service Attendance Trends
9. Outreach Activities Summary

### Lower Priority (Phase 3):
10. Detailed Engagement Metrics
11. Member Care Analytics
12. Prayer Activity Tracking
13. Comprehensive Growth Radar Chart

---

## 🔄 Time Period Options

### Available Periods:
- **This Week**
- **This Month** (default)
- **Last Month**
- **This Quarter**
- **Last Quarter**
- **This Year**
- **Last Year**
- **All Time**
- **Custom Range** (date picker)

### Period Comparison:
- Compare current period with previous period
- Show percentage change
- Display trend indicators (↑↓)

---

## 📱 Mobile-Friendly Chart Recommendations

### Libraries:
- **React Native:** Victory Native, Recharts (if using WebView)
- **Flutter:** FL Chart, Charts
- **Native:** MPAndroidChart (Android), Charts (iOS)

### Best Practices:
- Use swipeable cards for different metric categories
- Implement horizontal scrolling for time-based charts
- Use tab navigation for different time periods
- Add pull-to-refresh for data updates
- Show loading skeletons while fetching
- Cache data for offline viewing

---

## 💡 Insight Messages

### Based on Analytics:

#### Positive Growth:
```
🎉 Excellent Growth!
Your membership has grown by {percentage}% this month. 
Keep up the great work!
```

#### Areas for Improvement:
```
📊 Growth Opportunity
Your small group attendance is {percentage}% below average. 
Consider encouraging more participation.
```

#### Milestone Achievements:
```
🏆 Milestone Reached!
You've won {number} souls this month! 
This is your best month yet.
```

---

## 📋 Implementation Checklist

### Backend (API):
- [ ] Create analytics endpoint (`/auth/users/analytics/`)
- [ ] Aggregate data from all 20 campaign types
- [ ] Calculate growth metrics
- [ ] Implement time period filtering
- [ ] Add comparison with previous periods
- [ ] Optimize queries for performance

### Frontend (Mobile App):
- [ ] Create analytics dashboard screen
- [ ] Implement chart components
- [ ] Add time period selector
- [ ] Create metric cards
- [ ] Add loading states
- [ ] Implement pull-to-refresh
- [ ] Add empty states
- [ ] Create insight messages

---

This README provides a comprehensive foundation for implementing church growth analytics in your mobile app. All metrics are derived from actual submission data across your 20 campaign types.
