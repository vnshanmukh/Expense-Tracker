# Expense Tracker API Documentation

A FastAPI-based expense tracking system with JWT authentication and advanced features.

## Route Guide

### Authentication Routes

| Method | Endpoint                | Description                          | Requirements                      |
|--------|-------------------------|--------------------------------------|-----------------------------------|
| POST   | `/api/v1/auth/register`  | Register new user                    | `UserCreate` schema               |
| POST   | `/api/v1/auth/login`     | Login with email/password            | `UserLogin` schema                |
| POST   | `/api/v1/auth/login/token` | OAuth2-compatible token login        | OAuth2 form data                  |
| GET    | `/api/v1/auth/me`        | Get current user details             | Valid JWT in Authorization header |


## POST  `/api/v1/auth/register`

**Request:**
```
curl -X POST "http://localhost:8000/api/v1/auth/register" \
-H "Content-Type: application/json" \
-d '{
  "email": "john@example.com",
  "username": "john_doe",
  "password": "securepassword123"
}'
```
**Response**
```
{
  "email": "user1@example.com",
  "username": "string2",
  "id": 2,
  "is_active": true,
  "created_at": "2025-05-09T17:21:50"
}
```

## POST   `/api/v1/auth/login`

**Request:**
```
curl -X 'POST' \
  'http://127.0.0.1:8000/api/v1/auth/login' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "email": "user@example.com",
  "password": "string"
}'
```
**Response**
```
	
Response body
Download
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9....",
  "token_type": "bearer"
}
```

## POST   `/api/v1/auth/login`

**Request:**
```
curl -X 'POST' \
  'http://127.0.0.1:8000/api/v1/auth/login' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "email": "user@example.com",
  "password": "string"
}'
```
**Response**
```
	
Response body
Download
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9....",
  "token_type": "bearer"
}
```

## POST `/api/v1/auth/login/token`

**Request:**
```
curl -X 'POST' \
  'http://127.0.0.1:8000/api/v1/auth/login/token' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  -d 'grant_type=&username=user%40example.com&password=stringst&scope=&client_id=&client_secret='
```
**Response**
```

{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9....",
  "token_type": "bearer"
}
```

## GET `/api/v1/auth/me` 

**Request:**
```
curl -X 'GET' \
  'http://127.0.0.1:8000/api/v1/auth/me' \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxIiwiZXhwIjoxNzQ2ODA3NDk4fQ.JTX0oYe3NuKWXgLD7K1zGIFOKnNESCd8o2g5UbXw0zw'
```
**Response**

```
{
  "email": "user@example.com",
  "username": "string",
  "id": 1,
  "is_active": true,
  "created_at": "2025-05-09T15:48:06"
}
```


### Expense Routes

| Method | Endpoint                    | Description                          | Parameters/Requirements           |
|--------|-----------------------------|--------------------------------------|-----------------------------------|
| POST   | `/api/v1/expenses/`          | Create new expense                   | `ExpenseCreate` schema (Rate limited: 2/min) |
| GET    | `/api/v1/expenses/`          | Get filtered expenses                | Optional filters: category, payment_mode, date range |
| GET    | `/api/v1/expenses/{expense_id}` | Get specific expense                 | Valid expense ID                  |
| PUT    | `/api/v1/expenses/{expense_id}` | Update existing expense              | `ExpenseUpdate` schema              |
| DELETE | `/api/v1/expenses/{expense_id}` | Delete expense                       | Valid expense ID                  |


## POST  `/api/v1/expenses/`

**Request:**
```
curl -X 'POST' \
  'http://127.0.0.1:8000/api/v1/expenses/' \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxIiwiZXhwIjoxNzQ2ODEzODI3fQ.12eyKb-B06sFyCmh2RuZqAtTe8FaYxE8mHZ_nKX93pc' \
  -H 'Content-Type: application/json' \
  -d '{
  "amount": 1,
  "category": "gas",
  "description": "string",
  "date": "2025-05-09",
  "payment_mode": "apple_pay"
}'
```


**Response**

```
{
  "amount": 1,
  "category": "gas",
  "description": "string",
  "date": "2025-05-09",
  "payment_mode": "apple_pay",
  "id": 2,
  "user_id": 1,
  "created_at": "2025-05-09T17:35:38",
  "updated_at": "2025-05-09T17:35:38"
}
```


## GET  `/api/v1/expenses/`

In the Get Expenses route (GET /api/v1/expenses/), you can apply various filters to narrow down the results. Here are the available filters and how you can use them:

**Request:**
```
curl -X 'GET' \
  'http://127.0.0.1:8000/api/v1/expenses/?skip=0&limit=100' \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxIiwiZXhwIjoxNzQ2ODEzODI3fQ.12eyKb-B06sFyCmh2RuZqAtTe8FaYxE8mHZ_nKX93pc'
```

# Category
**Request:**
```
curl -X GET "http://localhost:8000/api/v1/expenses/?category=Food" \
-H "Authorization: Bearer your-jwt-token"
```

# payment_mode
**Request:**
```
curl -X GET "http://localhost:8000/api/v1/expenses/?payment_mode=credit_card" \
-H "Authorization: Bearer your-jwt-token"

```

# date_range
**Request:**
```
curl -X GET "http://localhost:8000/api/v1/expenses/?date_from=2025-05-01&date_to=2025-05-31" \
-H "Authorization: Bearer your-jwt-token"
```

**Response**

```
[
  {
    "amount": 1,
    "category": "string",
    "description": "string",
    "date": "2025-05-09",
    "payment_mode": "apple_pay",
    "id": 1,
    "user_id": 1,
    "created_at": "2025-05-09T15:50:06",
    "updated_at": "2025-05-09T15:50:06"
  },
  {
    "amount": 1,
    "category": "gas",
    "description": "string",
    "date": "2025-05-09",
    "payment_mode": "apple_pay",
    "id": 2,
    "user_id": 1,
    "created_at": "2025-05-09T17:35:38",
    "updated_at": "2025-05-09T17:35:38"
  }
```

##  GET `/api/v1/expenses/{expense_id}`

**Request:**
```
curl -X 'GET' \
  'http://127.0.0.1:8000/api/v1/expenses/1' \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxIiwiZXhwIjoxNzQ2ODEzODI3fQ.12eyKb-B06sFyCmh2RuZqAtTe8FaYxE8mHZ_nKX93pc'
```

**Response**

```
{
  "amount": 1,
  "category": "string",
  "description": "string",
  "date": "2025-05-09",
  "payment_mode": "apple_pay",
  "id": 1,
  "user_id": 1,
  "created_at": "2025-05-09T15:50:06",
  "updated_at": "2025-05-09T15:50:06"
}
```

##  PUT `/api/v1/expenses/{expense_id}`

**Request:**
```
curl -X 'PUT' \
  'http://127.0.0.1:8000/api/v1/expenses/2' \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxIiwiZXhwIjoxNzQ2ODEzODI3fQ.12eyKb-B06sFyCmh2RuZqAtTe8FaYxE8mHZ_nKX93pc' \
  -H 'Content-Type: application/json' \
  -d '{
  "amount": 1,
  "category": "food",
  "description": "string",
  "payment_mode": "cash"
}'
```

**Response**

```
{
  "amount": 1,
  "category": "food",
  "description": "string",
  "date": "2025-05-09",
  "payment_mode": "cash",
  "id": 2,
  "user_id": 1,
  "created_at": "2025-05-09T17:35:38",
  "updated_at": "2025-05-09T17:46:28"
}
```

##  DELETE `/api/v1/expenses/{expense_id}`

**Request:**
```
curl -X 'DELETE' \
  'http://127.0.0.1:8000/api/v1/expenses/2' \
  -H 'accept: */*' \
  -H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxIiwiZXhwIjoxNzQ2ODEzODI3fQ.12eyKb-B06sFyCmh2RuZqAtTe8FaYxE8mHZ_nKX93pc'
```

### Report Routes

| Method | Endpoint                      | Description                          | Parameters                       |
|--------|-------------------------------|--------------------------------------|----------------------------------|
| GET    | `/api/v1/reports/monthly/{year}/{month}` | Monthly summary by category | Year (int), Month (int)          |
| GET    | `/api/v1/reports/export/csv`   | Export all expenses as CSV           | N/A                              |


##  GET  `/api/v1/reports/monthly/{year}/{month}`

**Request:**
```
curl -X 'GET' \
  'http://127.0.0.1:8000/api/v1/reports/monthly/2025/05' \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxIiwiZXhwIjoxNzQ2ODEzODI3fQ.12eyKb-B06sFyCmh2RuZqAtTe8FaYxE8mHZ_nKX93pc'
Request URL
```

**Response**

```
{
  "month": "May",
  "year": 2025,
  "total_amount": 1,
  "categories": [
    {
      "category": "string",
      "total_amount": 1,
      "count": 1
    }
  ]
}
```

##  GET  `/api/v1/reports/export/csv`

**Request:**

```
curl -X 'GET' \
  'http://127.0.0.1:8000/api/v1/reports/export/csv' \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxIiwiZXhwIjoxNzQ2ODEzODI3fQ.12eyKb-B06sFyCmh2RuZqAtTe8FaYxE8mHZ_nKX93pc'
```
