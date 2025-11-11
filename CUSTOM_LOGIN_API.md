# Custom Login API with User Role

## Overview

The login endpoint now returns **complete user information** including role, service assignment, and profile details along with the JWT tokens.

This eliminates the need for a separate API call to get user details after login.

---

## Endpoint

**POST** `/api/auth/login/`

---

## Request

### Headers
```
Content-Type: application/json
```

### Request Body
```json
{
  "username": "johndoe",
  "password": "your-password"
}
```

---

## Response

### Success Response (200 OK)

```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "user": {
    "id": 1,
    "username": "johndoe",
    "email": "john@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "full_name": "John Doe",
    "role": "PASTOR",
    "phone_number": "+1234567890",
    "password_changed": true,
    "profile_picture": "http://example.com/media/profile_pictures/john.jpg",
    "service": {
      "id": 5,
      "name": "Accra Central Service",
      "location": "Accra",
      "total_members": 250
    },
    "is_campaign_manager": false
  }
}
```

### Response for Campaign Manager

```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "user": {
    "id": 15,
    "username": "janecm",
    "email": "jane@example.com",
    "first_name": "Jane",
    "last_name": "Campaign Manager",
    "full_name": "Jane Campaign Manager",
    "role": "CAMPAIGN_MANAGER",
    "phone_number": "+1234567891",
    "password_changed": false,
    "profile_picture": null,
    "service": null,
    "is_campaign_manager": true,
    "assigned_campaigns_count": 5
  }
}
```

### Error Response (401 Unauthorized)

```json
{
  "detail": "No active account found with the given credentials"
}
```

---

## Response Fields

### Root Level
| Field | Type | Description |
|-------|------|-------------|
| `access` | string | JWT access token (expires in 60 minutes) |
| `refresh` | string | JWT refresh token (expires in 24 hours) |
| `user` | object | Complete user information |

### User Object
| Field | Type | Description |
|-------|------|-------------|
| `id` | integer | User ID |
| `username` | string | Username |
| `email` | string | Email address |
| `first_name` | string | First name |
| `last_name` | string | Last name |
| `full_name` | string | Full name (first + last) |
| `role` | string | User role: `ADMIN`, `PASTOR`, `HELPER`, or `CAMPAIGN_MANAGER` |
| `phone_number` | string | Phone number |
| `password_changed` | boolean | Whether user has changed their default password |
| `profile_picture` | string/null | URL to profile picture or `null` |
| `service` | object/null | Service details or `null` (Campaign Managers have `null`) |
| `is_campaign_manager` | boolean | Whether user is a Campaign Manager |
| `assigned_campaigns_count` | integer | (Only for Campaign Managers) Number of assigned campaigns |

### Service Object (if user has a service)
| Field | Type | Description |
|-------|------|-------------|
| `id` | integer | Service ID |
| `name` | string | Service name |
| `location` | string | Service location |
| `total_members` | integer | Total members in service |

---

## Use Cases by Role

### 1. Admin User
```json
{
  "user": {
    "role": "ADMIN",
    "service": {
      "id": 1,
      "name": "Headquarters",
      ...
    },
    "is_campaign_manager": false
  }
}
```

### 2. Pastor User
```json
{
  "user": {
    "role": "PASTOR",
    "service": {
      "id": 8,
      "name": "Kumasi Branch",
      ...
    },
    "is_campaign_manager": false
  }
}
```

### 3. Helper User
```json
{
  "user": {
    "role": "HELPER",
    "service": {
      "id": 8,
      "name": "Kumasi Branch",
      ...
    },
    "is_campaign_manager": false
  }
}
```

### 4. Campaign Manager User
```json
{
  "user": {
    "role": "CAMPAIGN_MANAGER",
    "service": null,
    "is_campaign_manager": true,
    "assigned_campaigns_count": 5
  }
}
```

---

## Frontend Implementation Examples

### React/React Native - Login with Role Check

```typescript
import { useState } from 'react';
import axios from 'axios';

interface LoginResponse {
  access: string;
  refresh: string;
  user: {
    id: number;
    username: string;
    email: string;
    first_name: string;
    last_name: string;
    full_name: string;
    role: 'ADMIN' | 'PASTOR' | 'HELPER' | 'CAMPAIGN_MANAGER';
    phone_number: string;
    password_changed: boolean;
    profile_picture: string | null;
    service: {
      id: number;
      name: string;
      location: string;
      total_members: number;
    } | null;
    is_campaign_manager: boolean;
    assigned_campaigns_count?: number;
  };
}

const useLogin = () => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const login = async (username: string, password: string) => {
    setLoading(true);
    setError(null);

    try {
      const response = await axios.post<LoginResponse>('/api/auth/login/', {
        username,
        password
      });

      const { access, refresh, user } = response.data;

      // Store tokens
      localStorage.setItem('accessToken', access);
      localStorage.setItem('refreshToken', refresh);

      // Store user data
      localStorage.setItem('user', JSON.stringify(user));

      // Role-based navigation
      if (user.role === 'CAMPAIGN_MANAGER') {
        // Redirect to Campaign Manager dashboard
        window.location.href = '/campaign-manager/dashboard';
      } else if (user.role === 'ADMIN') {
        // Redirect to Admin dashboard
        window.location.href = '/admin/dashboard';
      } else {
        // Redirect to standard dashboard (Pastor/Helper)
        window.location.href = '/dashboard';
      }

      // Check if password change is needed
      if (!user.password_changed) {
        window.location.href = '/change-password';
      }

      return user;
    } catch (err: any) {
      const errorMessage = err.response?.data?.detail || 'Login failed';
      setError(errorMessage);
      throw new Error(errorMessage);
    } finally {
      setLoading(false);
    }
  };

  return { login, loading, error };
};

export default useLogin;
```

### React - Login Form Component

```tsx
import React, { useState } from 'react';
import { Form, Input, Button, Alert } from 'antd';
import useLogin from './useLogin';

const LoginForm = () => {
  const { login, loading, error } = useLogin();

  const onFinish = async (values: { username: string; password: string }) => {
    try {
      const user = await login(values.username, values.password);
      console.log('Logged in as:', user.role);
    } catch (error) {
      console.error('Login error:', error);
    }
  };

  return (
    <Form onFinish={onFinish} layout="vertical">
      {error && <Alert message={error} type="error" showIcon />}
      
      <Form.Item
        label="Username"
        name="username"
        rules={[{ required: true, message: 'Please input your username!' }]}
      >
        <Input placeholder="Enter username" />
      </Form.Item>

      <Form.Item
        label="Password"
        name="password"
        rules={[{ required: true, message: 'Please input your password!' }]}
      >
        <Input.Password placeholder="Enter password" />
      </Form.Item>

      <Form.Item>
        <Button type="primary" htmlType="submit" loading={loading} block>
          Log In
        </Button>
      </Form.Item>
    </Form>
  );
};

export default LoginForm;
```

### React Native - Login Screen

```typescript
import React, { useState } from 'react';
import { View, Text, TextInput, TouchableOpacity, StyleSheet, Alert } from 'react-native';
import AsyncStorage from '@react-native-async-storage/async-storage';
import axios from 'axios';

const LoginScreen = ({ navigation }) => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);

  const handleLogin = async () => {
    if (!username || !password) {
      Alert.alert('Error', 'Please fill in all fields');
      return;
    }

    setLoading(true);

    try {
      const response = await axios.post('/api/auth/login/', {
        username,
        password
      });

      const { access, refresh, user } = response.data;

      // Store tokens and user data
      await AsyncStorage.setItem('accessToken', access);
      await AsyncStorage.setItem('refreshToken', refresh);
      await AsyncStorage.setItem('user', JSON.stringify(user));

      // Navigate based on role
      if (user.is_campaign_manager) {
        navigation.replace('CampaignManagerDashboard');
      } else if (user.role === 'ADMIN') {
        navigation.replace('AdminDashboard');
      } else {
        navigation.replace('Dashboard');
      }

      // Prompt password change if needed
      if (!user.password_changed) {
        Alert.alert(
          'Change Password',
          'You are using the default password. Please change it for security.',
          [
            {
              text: 'Later',
              style: 'cancel'
            },
            {
              text: 'Change Now',
              onPress: () => navigation.navigate('ChangePassword')
            }
          ]
        );
      }
    } catch (error: any) {
      const errorMessage = error.response?.data?.detail || 'Login failed. Please try again.';
      Alert.alert('Login Failed', errorMessage);
    } finally {
      setLoading(false);
    }
  };

  return (
    <View style={styles.container}>
      <Text style={styles.title}>SSMG Login</Text>

      <TextInput
        style={styles.input}
        placeholder="Username"
        value={username}
        onChangeText={setUsername}
        autoCapitalize="none"
      />

      <TextInput
        style={styles.input}
        placeholder="Password"
        value={password}
        onChangeText={setPassword}
        secureTextEntry
      />

      <TouchableOpacity
        style={[styles.button, loading && styles.buttonDisabled]}
        onPress={handleLogin}
        disabled={loading}
      >
        <Text style={styles.buttonText}>
          {loading ? 'Logging in...' : 'Log In'}
        </Text>
      </TouchableOpacity>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'center',
    padding: 20,
    backgroundColor: '#fff',
  },
  title: {
    fontSize: 32,
    fontWeight: 'bold',
    marginBottom: 40,
    textAlign: 'center',
  },
  input: {
    borderWidth: 1,
    borderColor: '#ddd',
    padding: 15,
    marginBottom: 15,
    borderRadius: 8,
    fontSize: 16,
  },
  button: {
    backgroundColor: '#2196F3',
    padding: 15,
    borderRadius: 8,
    alignItems: 'center',
    marginTop: 10,
  },
  buttonDisabled: {
    backgroundColor: '#ccc',
  },
  buttonText: {
    color: '#fff',
    fontSize: 16,
    fontWeight: 'bold',
  },
});

export default LoginScreen;
```

---

## Role-Based Routing Example

```typescript
// utils/roleBasedRoute.ts
export const getRoleBasedRoute = (role: string, isCampaignManager: boolean): string => {
  if (isCampaignManager) {
    return '/campaign-manager/dashboard';
  }

  switch (role) {
    case 'ADMIN':
      return '/admin/dashboard';
    case 'PASTOR':
      return '/pastor/dashboard';
    case 'HELPER':
      return '/helper/dashboard';
    default:
      return '/dashboard';
  }
};

// Usage
const user = response.data.user;
const route = getRoleBasedRoute(user.role, user.is_campaign_manager);
navigate(route);
```

---

## Context/Store Example (React)

```typescript
// contexts/AuthContext.tsx
import React, { createContext, useContext, useState, useEffect } from 'react';

interface User {
  id: number;
  username: string;
  role: string;
  is_campaign_manager: boolean;
  service: any;
  // ... other fields
}

interface AuthContextType {
  user: User | null;
  isAuthenticated: boolean;
  login: (username: string, password: string) => Promise<void>;
  logout: () => void;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);

  useEffect(() => {
    // Check for stored user data
    const storedUser = localStorage.getItem('user');
    if (storedUser) {
      setUser(JSON.parse(storedUser));
    }
  }, []);

  const login = async (username: string, password: string) => {
    const response = await axios.post('/api/auth/login/', { username, password });
    const { access, refresh, user } = response.data;

    localStorage.setItem('accessToken', access);
    localStorage.setItem('refreshToken', refresh);
    localStorage.setItem('user', JSON.stringify(user));

    setUser(user);
  };

  const logout = () => {
    localStorage.removeItem('accessToken');
    localStorage.removeItem('refreshToken');
    localStorage.removeItem('user');
    setUser(null);
  };

  return (
    <AuthContext.Provider
      value={{
        user,
        isAuthenticated: !!user,
        login,
        logout
      }}
    >
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within AuthProvider');
  }
  return context;
};
```

---

## Benefits

1. **Single API Call:** Get tokens and user info in one request
2. **Role-Based Navigation:** Immediately redirect based on user role
3. **Service Information:** Know user's service without extra call
4. **Campaign Manager Support:** Detect Campaign Managers and show assigned campaigns count
5. **Password Change Detection:** Prompt users to change default passwords
6. **Reduced Latency:** Faster login experience

---

## Migration Guide

### Before (Two API Calls)
```typescript
// 1. Login to get tokens
const loginRes = await axios.post('/api/auth/login/', { username, password });
const { access } = loginRes.data;

// 2. Get user profile
const userRes = await axios.get('/api/auth/users/get_profile/', {
  headers: { Authorization: `Bearer ${access}` }
});
const user = userRes.data;
```

### After (One API Call)
```typescript
// Login and get user info in one call
const { data } = await axios.post('/api/auth/login/', { username, password });
const { access, refresh, user } = data;

// user object already contains role, service, profile picture, etc.
```

---

## Security Notes

1. **Access Token:** Valid for 60 minutes
2. **Refresh Token:** Valid for 24 hours
3. **Password Security:** System prompts for password change if `password_changed` is `false`
4. **Token Storage:**
   - **Web:** Use `localStorage` or `sessionStorage`
   - **Mobile:** Use secure storage like `AsyncStorage` (React Native) or `SecureStore` (Expo)

---

## Testing Examples

### cURL
```bash
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username": "johndoe", "password": "password123"}'
```

### Postman
```
POST http://localhost:8000/api/auth/login/
Content-Type: application/json

{
  "username": "johndoe",
  "password": "password123"
}
```

---

## See Also

- [Campaign Manager API](./CAMPAIGN_MANAGER_API.md)
- [Campaign Manager Service Selection](./CAMPAIGN_MANAGER_SERVICE_SELECTION.md)
- [Admin Dashboards Specification](./ADMIN_DASHBOARDS_SPECIFICATION.md)

---

**Implementation Date:** November 10, 2025  
**Last Updated:** November 10, 2025


