# Campaign Manager Service Selection

## Overview

Campaign Managers are **not assigned to a specific service**. Unlike Pastors and Helpers who are tied to one service, Campaign Managers can submit data for **multiple services** across the campaigns they are assigned to.

This flexibility requires Campaign Managers to **explicitly specify which service** they are submitting data for.

---

## How It Works

### For Campaign Managers
When creating a submission, Campaign Managers **MUST provide** the `service` field:

```json
{
  "campaign": 1,
  "service": 5,
  "submission_period": "2025-01-01",
  "date": "2025-01-15",
  "total_membership": 150,
  "lost": 5,
  "stable": 120,
  "unstable": 25
}
```

**Key Points:**
- `service` is **REQUIRED** for Campaign Managers
- Provide the **service ID** (integer)
- You can submit for ANY service (not restricted by assignments)
- If you forget to include `service`, you'll get an error:
  ```json
  {
    "service": ["Campaign Managers must specify a service."]
  }
  ```

### For Pastors and Helpers
Pastors and Helpers **should NOT provide** the `service` field:

```json
{
  "campaign": 1,
  "submission_period": "2025-01-01",
  "date": "2025-01-15",
  "total_membership": 150,
  "lost": 5,
  "stable": 120,
  "unstable": 25
}
```

**Key Points:**
- `service` is **automatically set** from your user profile
- Even if you provide it, the system uses your assigned service
- You can only submit for your assigned service

---

## API Examples

### Campaign Manager Submission

**Endpoint:** `POST /api/campaigns/state-of-flock/submissions/`

**Headers:**
```
Authorization: Token <campaign-manager-token>
Content-Type: application/json
```

**Request Body:**
```json
{
  "campaign": 3,
  "service": 12,
  "submission_period": "2025-11-01",
  "date": "2025-11-10",
  "total_membership": 200,
  "lost": 10,
  "stable": 160,
  "unstable": 30
}
```

**Success Response (201):**
```json
{
  "id": 456,
  "campaign": 3,
  "submitted_by": 78,
  "submitted_by_name": "Jane Campaign Manager",
  "service": 12,
  "service_name": "Accra Central Service",
  "submission_period": "2025-11-01",
  "date": "2025-11-10",
  "total_membership": 200,
  "lost": 10,
  "stable": 160,
  "unstable": 30,
  "created_at": "2025-11-10T14:30:00Z",
  "updated_at": "2025-11-10T14:30:00Z"
}
```

**Error Response - Missing Service (400):**
```json
{
  "service": ["Campaign Managers must specify a service."]
}
```

**Error Response - Invalid Service (400):**
```json
{
  "service": ["Invalid service id."]
}
```

---

### Pastor/Helper Submission

**Endpoint:** `POST /api/campaigns/state-of-flock/submissions/`

**Headers:**
```
Authorization: Token <pastor-token>
Content-Type: application/json
```

**Request Body:**
```json
{
  "campaign": 3,
  "submission_period": "2025-11-01",
  "date": "2025-11-10",
  "total_membership": 180,
  "lost": 8,
  "stable": 150,
  "unstable": 22
}
```

**Success Response (201):**
```json
{
  "id": 457,
  "campaign": 3,
  "submitted_by": 45,
  "submitted_by_name": "Pastor John",
  "service": 8,
  "service_name": "Kumasi Branch",
  "submission_period": "2025-11-01",
  "date": "2025-11-10",
  "total_membership": 180,
  "lost": 8,
  "stable": 150,
  "unstable": 22,
  "created_at": "2025-11-10T14:35:00Z",
  "updated_at": "2025-11-10T14:35:00Z"
}
```

> **Note:** The `service` field is automatically set to the pastor's assigned service (ID: 8).

---

## Getting Available Services

Campaign Managers need to know which services exist to select from.

**Endpoint:** `GET /api/auth/services/`

**Response:**
```json
{
  "count": 15,
  "results": [
    {
      "id": 1,
      "name": "Accra Central Service",
      "location": "Accra",
      "total_members": 250,
      "created_at": "2024-01-15T10:00:00Z",
      "updated_at": "2025-11-10T12:00:00Z"
    },
    {
      "id": 2,
      "name": "Kumasi Branch",
      "location": "Kumasi",
      "total_members": 180,
      "created_at": "2024-03-20T10:00:00Z",
      "updated_at": "2025-11-09T08:30:00Z"
    },
    ...
  ]
}
```

---

## Frontend Implementation Examples

### React/React Native - Campaign Manager Form

```typescript
import React, { useState, useEffect } from 'react';
import { Select, Form, Input, DatePicker, Button, message } from 'antd';
import axios from 'axios';

interface Service {
  id: number;
  name: string;
  location: string;
}

const CampaignManagerSubmissionForm = () => {
  const [services, setServices] = useState<Service[]>([]);
  const [loading, setLoading] = useState(false);
  const [form] = Form.useForm();

  useEffect(() => {
    // Fetch available services
    const fetchServices = async () => {
      try {
        const response = await axios.get('/api/auth/services/', {
          headers: { Authorization: `Token ${localStorage.getItem('token')}` }
        });
        setServices(response.data.results);
      } catch (error) {
        message.error('Failed to load services');
      }
    };
    fetchServices();
  }, []);

  const onSubmit = async (values: any) => {
    setLoading(true);
    try {
      await axios.post('/api/campaigns/state-of-flock/submissions/', {
        campaign: values.campaign,
        service: values.service, // Required for Campaign Managers
        submission_period: values.submission_period.format('YYYY-MM-DD'),
        date: values.date.format('YYYY-MM-DD'),
        total_membership: values.total_membership,
        lost: values.lost,
        stable: values.stable,
        unstable: values.unstable
      }, {
        headers: { Authorization: `Token ${localStorage.getItem('token')}` }
      });
      message.success('Submission created successfully!');
      form.resetFields();
    } catch (error: any) {
      if (error.response?.data?.service) {
        message.error(error.response.data.service[0]);
      } else {
        message.error('Failed to create submission');
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <Form form={form} onFinish={onSubmit} layout="vertical">
      <Form.Item
        label="Service"
        name="service"
        rules={[{ required: true, message: 'Please select a service' }]}
      >
        <Select placeholder="Select a service">
          {services.map(service => (
            <Select.Option key={service.id} value={service.id}>
              {service.name} - {service.location}
            </Select.Option>
          ))}
        </Select>
      </Form.Item>

      <Form.Item
        label="Campaign"
        name="campaign"
        rules={[{ required: true, message: 'Please enter campaign ID' }]}
      >
        <Input type="number" placeholder="Campaign ID" />
      </Form.Item>

      <Form.Item
        label="Submission Period"
        name="submission_period"
        rules={[{ required: true }]}
      >
        <DatePicker style={{ width: '100%' }} />
      </Form.Item>

      <Form.Item
        label="Date"
        name="date"
        rules={[{ required: true }]}
      >
        <DatePicker style={{ width: '100%' }} />
      </Form.Item>

      <Form.Item
        label="Total Membership"
        name="total_membership"
        rules={[{ required: true }]}
      >
        <Input type="number" />
      </Form.Item>

      <Form.Item label="Lost Members" name="lost" rules={[{ required: true }]}>
        <Input type="number" />
      </Form.Item>

      <Form.Item label="Stable Members" name="stable" rules={[{ required: true }]}>
        <Input type="number" />
      </Form.Item>

      <Form.Item label="Unstable Members" name="unstable" rules={[{ required: true }]}>
        <Input type="number" />
      </Form.Item>

      <Form.Item>
        <Button type="primary" htmlType="submit" loading={loading}>
          Submit
        </Button>
      </Form.Item>
    </Form>
  );
};

export default CampaignManagerSubmissionForm;
```

### React Native - Service Picker

```typescript
import React, { useState, useEffect } from 'react';
import { View, Text, StyleSheet } from 'react-native';
import { Picker } from '@react-native-picker/picker';
import axios from 'axios';

const ServiceSelector = ({ value, onChange }) => {
  const [services, setServices] = useState([]);

  useEffect(() => {
    const fetchServices = async () => {
      try {
        const response = await axios.get('/api/auth/services/');
        setServices(response.data.results);
      } catch (error) {
        console.error('Failed to load services:', error);
      }
    };
    fetchServices();
  }, []);

  return (
    <View style={styles.container}>
      <Text style={styles.label}>Select Service *</Text>
      <Picker
        selectedValue={value}
        onValueChange={onChange}
        style={styles.picker}
      >
        <Picker.Item label="-- Select a service --" value="" />
        {services.map(service => (
          <Picker.Item 
            key={service.id} 
            label={`${service.name} (${service.location})`} 
            value={service.id} 
          />
        ))}
      </Picker>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    marginBottom: 16,
  },
  label: {
    fontSize: 16,
    fontWeight: 'bold',
    marginBottom: 8,
  },
  picker: {
    height: 50,
    borderWidth: 1,
    borderColor: '#ccc',
  },
});

export default ServiceSelector;
```

---

## Validation Rules Summary

| User Role | `service` Field | Behavior |
|-----------|----------------|----------|
| **Campaign Manager** | **REQUIRED** | Must provide service ID in request body |
| **Pastor** | **Omit** | Automatically set from user's assigned service |
| **Helper** | **Omit** | Automatically set from user's assigned service |
| **Admin** | **Omit** | Automatically set (if assigned) |

---

## Error Scenarios

### 1. Campaign Manager Forgets Service Field

**Request:**
```json
{
  "campaign": 1,
  "submission_period": "2025-11-01",
  "date": "2025-11-10",
  "total_membership": 200
}
```

**Response (400):**
```json
{
  "service": ["Campaign Managers must specify a service."]
}
```

### 2. Campaign Manager Provides Invalid Service ID

**Request:**
```json
{
  "campaign": 1,
  "service": 999,
  "submission_period": "2025-11-01",
  "date": "2025-11-10",
  "total_membership": 200
}
```

**Response (400):**
```json
{
  "service": ["Invalid service id."]
}
```

### 3. Campaign Manager Not Assigned to Campaign

**Request:**
```json
{
  "campaign": 50,
  "service": 5,
  "submission_period": "2025-11-01",
  "date": "2025-11-10",
  "total_membership": 200
}
```

**Response (400):**
```json
{
  "campaign": ["You are not assigned to this campaign."]
}
```

---

## Backend Implementation

### Helper Function

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

### Usage in ViewSet

```python
def perform_create(self, serializer):
    user = self.request.user
    campaign_id = self.request.data.get('campaign')
    
    # ... campaign validation ...
    
    # Get service (Campaign Managers select, others use assigned)
    service = get_service_for_submission(user, self.request.data)
    serializer.save(submitted_by=self.request.user, service=service, campaign=campaign)
```

---

## Best Practices

### For Campaign Managers:
1. **Always include the `service` field** in every submission
2. **Fetch the service list** before showing the submission form
3. **Cache the service list** to reduce API calls
4. **Validate service selection** before submitting
5. **Show service name** (not just ID) in the UI for better UX

### For Frontend Developers:
1. **Conditionally show service selector** based on user role
2. **Use dropdown/picker** for service selection (don't allow free text)
3. **Show service location** alongside name for clarity
4. **Implement proper error handling** for service-related errors
5. **Pre-select service** if there's a default or previously used service

### For Backend Developers:
1. **Validate service existence** before creating submission
2. **Log service selection** for audit trails
3. **Consider service permissions** if implementing granular access control
4. **Handle edge cases** (deleted services, inactive services, etc.)

---

## FAQ

**Q: Can a Campaign Manager submit for a service without being assigned to it?**
A: Yes! Campaign Managers can submit for ANY service. They're not restricted to specific services, only to specific campaigns.

**Q: What happens if a Pastor provides a `service` field?**
A: The system will ignore it and use the pastor's assigned service instead.

**Q: Can a Campaign Manager be assigned to a service?**
A: Technically yes, but it's not recommended. Campaign Managers are designed to work across multiple services.

**Q: How do I know which service IDs are valid?**
A: Call `GET /api/auth/services/` to get the full list of services with their IDs.

**Q: Can I submit for multiple services in one request?**
A: No. Each submission is for ONE service only. You need to make separate API calls for each service.

---

## See Also

- [Campaign Manager README](./CAMPAIGN_MANAGER_README.md)
- [Campaign Manager API](./CAMPAIGN_MANAGER_API.md)
- [Campaigns README](./campaigns/README.md)
- [Admin Dashboards Specification](./ADMIN_DASHBOARDS_SPECIFICATION.md)

---

**Implementation Date:** November 10, 2025
**Last Updated:** November 10, 2025


