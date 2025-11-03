# Analytics API Endpoint Documentation

## Endpoint

`GET /auth/users/analytics/`

## Authentication

Requires `Bearer Token` authentication.

## Query Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `period` | string | No | Time period: `week`, `month` (default), `quarter`, `year`, `all` |
| `start_date` | string (YYYY-MM-DD) | No | Start date for custom range (must be used with `end_date`) |
| `end_date` | string (YYYY-MM-DD) | No | End date for custom range (must be used with `start_date`) |

## Response Structure

The response includes comprehensive analytics data with **chart-ready data structures** for line charts, bar charts, and other visualizations. Each metric category includes:

- **Summary metrics**: Current period totals and statistics
- **Trend arrays**: Historical data points (last 12 months)
- **Chart data objects**: Pre-formatted data for charting libraries

```json
{
  "period": {
    "type": "month",
    "start": "2025-01-01T00:00:00Z",
    "end": "2025-01-31T23:59:59Z"
  },
  "membership": {
    "current": 1250,
    "previous": 1200,
    "growth": 50,
    "growth_percentage": 4.17,
    "stable": 1000,
    "unstable": 200,
    "lost": 50,
    "trend": [
      {
        "period": "2025-01",
        "label": "Jan 2025",
        "total": 1250,
        "stable": 1000,
        "unstable": 200,
        "lost": 50
      }
    ],
    "chart_data": {
      "labels": ["Jan 2025", "Dec 2024", "Nov 2024"],
      "datasets": [
        {
          "label": "Total Membership",
          "data": [1250, 1200, 1180],
          "color": "#2196F3"
        },
        {
          "label": "Stable Members",
          "data": [1000, 950, 930],
          "color": "#4CAF50"
        },
        {
          "label": "Unstable Members",
          "data": [200, 220, 230],
          "color": "#FF9800"
        }
      ]
    }
  },
  "soul_winning": {
    "total_all_time": 500,
    "this_period": 25,
    "previous_period": 30,
    "crusades": 3,
    "outreaches": 5,
    "dance_outreach": 2,
    "missionaries_sent": 10,
    "trend": [
      {
        "period": "2025-01",
        "label": "Jan 2025",
        "souls_won": 25,
        "crusades": 3,
        "outreaches": 5,
        "dance_outreach": 2,
        "missionaries_sent": 10
      }
    ],
    "cumulative_trend": [
      {
        "period": "2025-01",
        "label": "Jan 2025",
        "cumulative": 500
      }
    ],
    "chart_data": {
      "labels": ["Jan 2025", "Dec 2024"],
      "datasets": [
        {
          "label": "Souls Won",
          "data": [25, 30],
          "color": "#4CAF50"
        },
        {
          "label": "Crusades",
          "data": [3, 4],
          "color": "#2196F3"
        },
        {
          "label": "Outreaches",
          "data": [5, 6],
          "color": "#FF9800"
        }
      ],
      "cumulative": {
        "labels": ["Jan 2025", "Dec 2024"],
        "data": [500, 475],
        "color": "#9C27B0"
      }
    }
  },
  "leadership": {
    "total_leaders": 45,
    "trained_leaders": 35,
    "teaching_sessions": 12,
    "avg_attendance": 25.5,
    "hierarchy": {
      "cos": 5,
      "bos": 10,
      "bls": 15,
      "fls": 15,
      "potential_leaders": 20
    },
    "training_metrics": {
      "makarios": 30,
      "dakes_bible": 25,
      "thompson_chain": 20,
      "pose_certified": 15,
      "iptp_training": 10
    }
  },
  "small_groups": {
    "bacentas": 25,
    "basontas": 50,
    "new_groups": 3,
    "avg_attendance": 15,
    "avg_saturday": 200,
    "avg_sunday": 950,
    "trend": [...],
    "chart_data": {
      "labels": ["Jan 2025", "Dec 2024"],
      "datasets": [
        {
          "label": "Bacentas",
          "data": [25, 23],
          "color": "#2196F3"
        },
        {
          "label": "Basontas",
          "data": [50, 48],
          "color": "#4CAF50"
        }
      ]
    }
  },
  "attendance": {
    "avg_service": 850,
    "avg_saturday": 200,
    "avg_sunday": 950,
    "avg_bused": 650,
    "avg_walk_in": 200,
    "first_timers": 25,
    "swollen_sunday": {
      "attendance": 1200,
      "converts": 50
    },
    "trend": [...],
    "chart_data": {
      "labels": ["Jan 2025", "Dec 2024"],
      "datasets": [
        {
          "label": "Service Attendance",
          "data": [850, 820],
          "color": "#2196F3"
        },
        {
          "label": "Bused Members",
          "data": [650, 630],
          "color": "#4CAF50"
        },
        {
          "label": "Walk-in Members",
          "data": [200, 190],
          "color": "#FF9800"
        },
        {
          "label": "First Timers",
          "data": [25, 22],
          "color": "#9C27B0"
        }
      ]
    }
  },
  "engagement": {
    "youtube_subscribers": 150,
    "podcast_subscribers": 200,
    "messages_listened": 500,
    "testimonies_shared": 15,
    "lay_school_attendance": 45.5,
    "lay_school_teachers": 5,
    "trend": [...],
    "chart_data": {
      "labels": ["Jan 2025", "Dec 2024"],
      "datasets": [
        {
          "label": "YouTube Subscribers",
          "data": [150, 145],
          "color": "#FF0000"
        },
        {
          "label": "Podcast Subscribers",
          "data": [200, 195],
          "color": "#9C27B0"
        },
        {
          "label": "Testimonies Shared",
          "data": [15, 12],
          "color": "#FF9800"
        }
      ]
    }
  },
  "member_care": {
    "members_counseled": 120,
    "counseling_coverage": 9.6,
    "calls_made": 300,
    "telepastors": 10,
    "in_person": 80,
    "via_calls": 40,
    "trend": [...],
    "chart_data": {
      "labels": ["Jan 2025", "Dec 2024"],
      "datasets": [
        {
          "label": "Members Counseled",
          "data": [120, 110],
          "color": "#2196F3"
        },
        {
          "label": "In Person",
          "data": [80, 75],
          "color": "#4CAF50"
        },
        {
          "label": "Via Calls",
          "data": [40, 35],
          "color": "#FF9800"
        },
        {
          "label": "Telepastoring Calls",
          "data": [300, 280],
          "color": "#9C27B0"
        }
      ]
    }
  },
  "prayer": {
    "hours_prayed": 150.5,
    "participants": 45,
    "trend": [...],
    "chart_data": {
      "labels": ["Jan 2025", "Dec 2024"],
      "datasets": [
        {
          "label": "Hours Prayed",
          "data": [150.5, 145.2],
          "color": "#2196F3",
          "yAxisID": "y"
        },
        {
          "label": "Participants",
          "data": [45, 42],
          "color": "#4CAF50",
          "yAxisID": "y1"
        }
      ]
    }
  },
  "outreach": {
    "total_outreaches": 10,
    "members_from_outreaches": 50,
    "total_invites": 200,
    "people_visited": 150,
    "first_time_retained": 30,
    "converts_retained": 25,
    "trend": [...],
    "chart_data": {
      "labels": ["Jan 2025", "Dec 2024"],
      "datasets": [
        {
          "label": "Outreaches",
          "data": [10, 8],
          "color": "#2196F3"
        },
        {
          "label": "People Visited",
          "data": [150, 140],
          "color": "#4CAF50"
        },
        {
          "label": "Members from Outreaches",
          "data": [50, 45],
          "color": "#FF9800"
        },
        {
          "label": "First Time Retained",
          "data": [30, 28],
          "color": "#9C27B0"
        },
        {
          "label": "Converts Retained",
          "data": [25, 22],
          "color": "#F44336"
        }
      ]
    }
  }
}
```

## Example Requests

### Get Monthly Analytics
```bash
curl -X GET 'http://your-domain.com/auth/users/analytics/?period=month' \
  -H 'Authorization: Bearer YOUR_TOKEN'
```

### Get Quarterly Analytics
```bash
curl -X GET 'http://your-domain.com/auth/users/analytics/?period=quarter' \
  -H 'Authorization: Bearer YOUR_TOKEN'
```

### Get Custom Date Range
```bash
curl -X GET 'http://your-domain.com/auth/users/analytics/?start_date=2025-01-01&end_date=2025-01-31' \
  -H 'Authorization: Bearer YOUR_TOKEN'
```

### Get All-Time Analytics
```bash
curl -X GET 'http://your-domain.com/auth/users/analytics/?period=all' \
  -H 'Authorization: Bearer YOUR_TOKEN'
```

## Data Sources

The analytics aggregate data from the following campaign submissions:

- **Membership**: State of the Flock Campaign
- **Soul Winning**: Soul Winning Campaign
- **Leadership**: Servants Armed and Trained + Sheperding Control Campaigns
- **Small Groups**: Basonta Proliferation Campaign
- **Attendance**: Gathering Bus + Swollen Sunday Campaigns
- **Engagement**: Hearing and Seeing + Testimony + Understanding Campaigns
- **Member Care**: Intimate Counseling + Telepastoring Campaigns
- **Prayer**: Antibrutish Campaign
- **Outreach**: Multiplication + Sheep Seeking Campaigns

## Chart Data Format

The `chart_data` objects are formatted for direct use with common charting libraries (Chart.js, Victory Native, Recharts, etc.). Each includes:

- **labels**: Array of period labels (e.g., "Jan 2025", "Feb 2025")
- **datasets**: Array of data series with:
  - `label`: Series name
  - `data`: Array of numeric values matching labels
  - `color`: Hex color code for styling

### Chart Types Supported

1. **Line Charts**: Multi-series line charts (membership, soul winning, attendance, etc.)
2. **Bar Charts**: Stacked or grouped bar charts (outreach, member care)
3. **Area Charts**: Filled area charts (cumulative trends)
4. **Dual-Axis Charts**: Charts with two Y-axes (prayer hours vs participants)

### Example Usage with Chart.js

```javascript
const membershipChartData = {
  labels: response.membership.chart_data.labels,
  datasets: response.membership.chart_data.datasets.map(dataset => ({
    label: dataset.label,
    data: dataset.data,
    borderColor: dataset.color,
    backgroundColor: dataset.color + '20', // Add transparency
    tension: 0.4
  }))
};

// Use with Chart.js Line Chart
new Chart(ctx, {
  type: 'line',
  data: membershipChartData,
  options: { ... }
});
```

### Example Usage with Victory Native

```javascript
import { VictoryChart, VictoryLine, VictoryGroup } from 'victory-native';

const soulWinningData = response.soul_winning.chart_data;

<VictoryChart>
  <VictoryGroup>
    {soulWinningData.datasets.map((dataset, index) => (
      <VictoryLine
        key={index}
        data={dataset.data.map((value, i) => ({
          x: soulWinningData.labels[i],
          y: value
        }))}
        style={{ data: { stroke: dataset.color } }}
      />
    ))}
  </VictoryGroup>
</VictoryChart>
```

## Notes

- All metrics are calculated based on submissions by the authenticated user
- **Trend data** shows the **last 12 months** of historical data
- **Chart data** includes pre-formatted arrays ready for visualization
- Percentages and growth calculations handle division by zero gracefully
- Missing data fields default to 0 or appropriate null values
- Date filtering respects the `submission_period` or `date` field depending on the campaign type
- All color codes are provided in hex format (#RRGGBB) for easy styling

## Error Responses

### Invalid Date Format
```json
{
  "error": "Invalid date format. Use YYYY-MM-DD."
}
```
Status: `400 Bad Request`

### Unauthorized
```json
{
  "detail": "Authentication credentials were not provided."
}
```
Status: `401 Unauthorized`

