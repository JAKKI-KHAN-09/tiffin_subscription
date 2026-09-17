# Tiffin Management System

A web-based **Tiffin Subscription and Billing Management System** designed for home-style lunch delivery services.

The system helps tiffin owners manage customers, monthly subscriptions, pause/resume requests, and monthly bills. Customers are charged only for the days on which they were actually served.

---

## Problem Statement

A home-style tiffin service provides lunch to customers on a monthly subscription basis, usually on weekdays.

Customers may need to pause their service for a few days due to travel, festivals, or other reasons. The owner needs a reliable way to ensure that customers are **not charged for paused days**.

The system calculates the monthly bill based on the actual number of service days delivered.

---

## Objectives

* Manage tiffin customers using their phone numbers.
* Create and manage monthly subscriptions.
* Allow customers to pause their tiffin service.
* Allow customers to resume their service.
* Calculate the number of scheduled service days.
* Exclude paused weekdays from billing.
* Generate prorated monthly bills.
* Display active and paused customers.
* Provide a REST API for frontend integration.
* Store customer and subscription data in PostgreSQL.

---

## Key Features

### Customer Management

* Add new customers.
* Store customer name, phone number, and address.
* Search customers using their phone number.
* Prevent duplicate customer phone numbers.

### Subscription Management

* Subscribe customers to a monthly tiffin plan.
* Store subscription start and end dates.
* Track subscription status.

### Pause & Resume

* Pause a customer's subscription for a specific date range.
* Store the reason for the pause.
* Resume the subscription when the customer returns.
* Maintain pause history for billing.

### Pro-Rated Billing

The system calculates bills based on the actual days the customer was served.

For example:

```text
Monthly Plan       = ₹3000
Scheduled Weekdays = 22
Paused Weekdays    = 3
Served Days        = 19

Daily Rate = ₹3000 / 22

Final Bill ≈ ₹2590.91
```

Weekends are not counted as tiffin service days.

---

## Technology Stack

### Frontend

* React
* Vite
* JavaScript
* React Router
* HTML
* CSS

### Backend

* Python
* FastAPI
* SQLAlchemy
* Pydantic
* REST API

### Database

* PostgreSQL

### Development & Testing

* Git
* GitHub
* VS Code
* Pytest
* FastAPI Swagger/OpenAPI

---

## System Architecture

```text
                ┌──────────────────────┐
                │      React UI        │
                │      Frontend        │
                └──────────┬───────────┘
                           │
                           │ REST API
                           ▼
                ┌──────────────────────┐
                │       FastAPI        │
                │       Backend        │
                └──────────┬───────────┘
                           │
              ┌────────────┼────────────┐
              ▼            ▼            ▼
        ┌──────────┐ ┌──────────┐ ┌──────────┐
        │ Customer │ │Subscript.│ │ Billing  │
        │ Services │ │ Services │ │ Services │
        └────┬─────┘ └────┬─────┘ └────┬─────┘
             │            │            │
             └────────────┼────────────┘
                          ▼
                  ┌───────────────┐
                  │  SQLAlchemy   │
                  │      ORM      │
                  └───────┬───────┘
                          ▼
                  ┌───────────────┐
                  │  PostgreSQL   │
                  │    Database   │
                  └───────────────┘
```

---

## Project Structure

```text
tiffin-management-system/
│
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   ├── customers.py
│   │   │   ├── subscriptions.py
│   │   │   ├── pauses.py
│   │   │   ├── billing.py
│   │   │   └── dashboard.py
│   │   │
│   │   ├── schemas/
│   │   │   ├── customer.py
│   │   │   ├── subscription.py
│   │   │   ├── pause.py
│   │   │   └── bill.py
│   │   │
│   │   ├── services/
│   │   │   ├── customer_service.py
│   │   │   ├── subscription_service.py
│   │   │   ├── pause_service.py
│   │   │   └── billing_service.py
│   │   │
│   │   ├── utils/
│   │   │   ├── date_utils.py
│   │   │   └── billing_utils.py
│   │   │
│   │   ├── config.py
│   │   └── main.py
│   │
│   ├── database/
│   │   ├── database.py
│   │   ├── models.py
│   │   └── seed.py
│   │
│   ├── tests/
│   ├── requirements.txt
│   ├── .env.example
│   └── .gitignore
│
└── frontend/
    ├── src/
    │   ├── components/
    │   ├── pages/
    │   ├── services/
    │   ├── utils/
    │   ├── App.jsx
    │   ├── main.jsx
    │   └── index.css
    │
    ├── package.json
    └── vite.config.js
```

---

## Database Design

The system uses the following main entities:

### Customer

Stores customer information.

```text
Customer
---------
id
name
phone
address
created_at
```

### Plan

Stores available tiffin plans.

```text
Plan
---------
id
name
monthly_price
service_type
```

### Subscription

Connects a customer with a tiffin plan.

```text
Subscription
---------
id
customer_id
plan_id
start_date
end_date
status
```

### Pause Period

Stores the dates for which a subscription was paused.

```text
PausePeriod
---------
id
subscription_id
start_date
end_date
reason
```

### Bill

Stores calculated monthly billing information.

```text
Bill
---------
id
customer_id
subscription_id
billing_month
scheduled_days
paused_days
served_days
daily_rate
total_amount
```

---

## Billing Logic

The billing system follows these steps:

```text
1. Identify the customer's subscription
                ↓
2. Identify the selected billing month
                ↓
3. Calculate Monday-Friday service days
                ↓
4. Find all pause periods
                ↓
5. Remove paused weekdays
                ↓
6. Calculate actual served days
                ↓
7. Calculate daily rate
                ↓
8. Generate the final bill
```

### Formula

```text
Served Days = Scheduled Days - Paused Days

Daily Rate = Monthly Plan Price / Scheduled Days

Final Bill = Daily Rate × Served Days
```

Overlapping pause dates are treated as a single paused day so that the same day is not deducted more than once.

---

## Backend API

The FastAPI backend provides the following major endpoints:

### Customers

```text
POST /api/customers
```

Create a customer.

```text
GET /api/customers/phone/{phone}
```

Find a customer by phone number.

### Subscriptions

```text
POST /api/subscriptions
```

Create a tiffin subscription.

### Pause / Resume

```text
POST /api/pauses/{subscription_id}/pause
```

Pause a subscription.

```text
POST /api/pauses/{subscription_id}/resume
```

Resume a subscription.

### Billing

```text
GET /api/billing/{customer_id}?month=YYYY-MM
```

Generate the customer's monthly bill.

### Dashboard

```text
GET /api/dashboard
```

Get active and paused customer statistics.

---

## Local Development Setup

### 1. Clone the repository

```bash
git clone <repository-url>
cd tiffin-management-system
```

### 2. Create Python virtual environment

```bash
python3 -m venv .venv
```

Activate it on Linux/Codespaces:

```bash
source .venv/bin/activate
```

### 3. Install backend dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file inside the `backend` directory:

```env
DATABASE_URL=postgresql://tiffin_user:tiffin_password@localhost:5432/tiffin_db
APP_NAME=Tiffin Management System
DEBUG=True
```

Do not commit the `.env` file to GitHub.

### 5. Start the backend

From the `backend` directory:

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Backend:

```text
http://localhost:8000
```

Swagger API documentation:

```text
http://localhost:8000/docs
```

---

## Frontend Setup

Open another terminal.

```bash
cd frontend
npm install
```

Start the development server:

```bash
npm run dev -- --host 0.0.0.0
```

Frontend:

```text
http://localhost:5173
```

---

## Basic Testing Flow

After starting the backend, test the system in this order:

```text
1. Create Customer
       ↓
2. Create/Select Tiffin Plan
       ↓
3. Create Subscription
       ↓
4. Pause Subscription
       ↓
5. Resume Subscription
       ↓
6. Generate Monthly Bill
       ↓
7. Search Customer by Phone
       ↓
8. Check Dashboard
```

---

## Example

Suppose a customer subscribes to a:

```text
Monthly Lunch Plan = ₹3000
```

For a month with:

```text
Scheduled weekdays = 22
Paused weekdays    = 3
```

Then:

```text
Served days = 22 - 3
            = 19
```

The bill is calculated from the 19 actual service days rather than charging the full monthly amount.

---

## API Documentation

FastAPI automatically provides interactive API documentation through Swagger UI.

After starting the backend, open:

```text
http://localhost:8000/docs
```

This allows developers to test the APIs without requiring the frontend.

---

## Security & Configuration

* Database credentials are stored in environment variables.
* `.env` is excluded from Git.
* Database access is handled through SQLAlchemy.
* API validation is handled using Pydantic.
* CORS is configured for frontend-backend communication.

---

## Future Enhancements

* Owner authentication and authorization
* Customer login
* Online payment integration
* PDF invoice generation
* WhatsApp/SMS billing notifications
* Monthly billing reports
* Holiday management
* Multiple tiffin plans
* Delivery tracking
* Customer analytics
* Export billing data to Excel/CSV
* Production deployment using Docker and cloud services

---

## Project Status

**Current Stage:** Development

Core functionality:

* Customer management
* Subscription management
* Pause/resume management
* Weekday-based service calculation
* Pro-rated billing
* Phone-based customer lookup
* Active/paused dashboard

Frontend and backend integration are being developed incrementally.

---

## License

This project is developed for educational and project-development purposes.
