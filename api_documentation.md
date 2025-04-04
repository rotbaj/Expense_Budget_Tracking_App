# Budget & Expense Tracker API Documentation

## Overview
The Budget & Expense Tracker API allows users to manage their financial transactions, including budgets, expenses, and incomes. The API supports user authentication and provides endpoints for CRUD operations on budgets, expenses, and incomes.

## Authentication
All endpoints require authentication using JWT tokens.
- Obtain a token: `POST /api/auth/token/`
- Refresh token: `POST /api/auth/token/refresh/`

---
## Endpoints

### **1. User Authentication**
#### Register a new user
**POST** `/api/auth/register/`
##### Request Body:
```json
{
  "username": "user123",
  "email": "user@example.com",
  "password": "password123"
}
```
##### Response:
```json
{
  "id": 1,
  "username": "user123",
  "email": "user@example.com"
}
```

#### Login
**POST** `/api/auth/token/`
##### Request Body:
```json
{
  "username": "user123",
  "password": "password123"
}
```
##### Response:
```json
{
  "access": "jwt_access_token",
  "refresh": "jwt_refresh_token"
}
```

---
### **2. Budget Management**
#### Get all budgets
**GET** `/api/budgets/`
##### Response:
```json
[
  {
    "id": 1,
    "category": "Groceries",
    "limit": 500.00,
    "spent": 250.00,
    "remaining": 250.00
  }
]
```

#### Create a new budget
**POST** `/api/budgets/`
##### Request Body:
```json
{
  "category": "Groceries",
  "limit": 500.00
}
```
##### Response:
```json
{
  "id": 2,
  "category": "Groceries",
  "limit": 500.00,
  "spent": 0.00,
  "remaining": 500.00
}
```

#### Update a budget
**PUT** `/api/budgets/{id}/`
##### Request Body:
```json
{
  "limit": 600.00
}
```
##### Response:
```json
{
  "id": 2,
  "category": "Groceries",
  "limit": 600.00,
  "spent": 250.00,
  "remaining": 350.00
}
```

#### Delete a budget
**DELETE** `/api/budgets/{id}/`
##### Response:
```json
{
  "message": "Budget deleted successfully"
}
```

---
### **3. Expense Management**
#### Get all expenses
**GET** `/api/expenses/`
##### Response:
```json
[
  {
    "id": 1,
    "amount": 50.00,
    "category": "Groceries",
    "date": "2025-04-02"
  }
]
```

#### Create a new expense
**POST** `/api/expenses/`
##### Request Body:
```json
{
  "amount": 50.00,
  "category": "Groceries",
  "date": "2025-04-02"
}
```
##### Response:
```json
{
  "id": 2,
  "amount": 50.00,
  "category": "Groceries",
  "date": "2025-04-02"
}
```

#### Update an expense
**PUT** `/api/expenses/{id}/`
##### Request Body:
```json
{
  "amount": 60.00
}
```
##### Response:
```json
{
  "id": 2,
  "amount": 60.00,
  "category": "Groceries",
  "date": "2025-04-02"
}
```

#### Delete an expense
**DELETE** `/api/expenses/{id}/`
##### Response:
```json
{
  "message": "Expense deleted successfully"
}
```

---
### **4. Income Management**
#### Get all incomes
**GET** `/api/incomes/`
##### Response:
```json
[
  {
    "id": 1,
    "amount": 1000.00,
    "source": "Salary",
    "date": "2025-04-01"
  }
]
```

#### Create a new income
**POST** `/api/incomes/`
##### Request Body:
```json
{
  "amount": 1000.00,
  "source": "Salary",
  "date": "2025-04-01"
}
```
##### Response:
```json
{
  "id": 2,
  "amount": 1000.00,
  "source": "Salary",
  "date": "2025-04-01"
}
```

#### Update an income
**PUT** `/api/incomes/{id}/`
##### Request Body:
```json
{
  "amount": 1100.00
}
```
##### Response:
```json
{
  "id": 2,
  "amount": 1100.00,
  "source": "Salary",
  "date": "2025-04-01"
}
```

#### Delete an income
**DELETE** `/api/incomes/{id}/`
##### Response:
```json
{
  "message": "Income deleted successfully"
}
```

---
## Error Handling
### Common Error Responses
#### 400 Bad Request
```json
{
  "error": "Invalid request data"
}
```

#### 401 Unauthorized
```json
{
  "error": "Authentication required"
}
```

#### 404 Not Found
```json
{
  "error": "Resource not found"
}
```

#### 500 Internal Server Error
```json
{
  "error": "An unexpected error occurred"
}
```

---
## Conclusion
This API provides a structured way for users to manage their budgets, expenses, and incomes securely. Ensure you handle authentication properly before accessing protected endpoints.

