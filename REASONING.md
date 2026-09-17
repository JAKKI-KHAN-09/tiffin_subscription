# Solution Reasoning

## 1. Problem Understanding

The system is designed for a tiffin service where customers subscribe to a monthly lunch plan. Customers may pause their service for a few days, so billing must be based only on the days they were actually served.

Core requirements:

* Customer management using phone number
* Monthly subscription management
* Pause/resume functionality
* Weekday-based service calculation
* Pro-rated monthly billing
* Active/paused customer status

---

## 2. Solution Approach

The problem was divided into independent modules:

```text
Customer
   ↓
Subscription
   ↓
Pause / Resume
   ↓
Service-Day Calculation
   ↓
Billing
   ↓
Lookup & Dashboard
```

This modular approach makes the system easier to develop, test, and maintain.

---

## 3. Technology Decisions

| Component  | Technology       | Reason                           |
| ---------- | ---------------- | -------------------------------- |
| Frontend   | React + Vite     | Fast and component-based UI      |
| Backend    | Python + FastAPI | Simple REST API development      |
| ORM        | SQLAlchemy       | Structured database access       |
| Database   | PostgreSQL       | Reliable relational data storage |
| Validation | Pydantic         | API request/response validation  |
| Testing    | Pytest           | Automated backend testing        |

---

## 4. Database Design

The data is separated into five main entities:

```text
Customer
   │
   └── Subscription ─── Plan
          │
          └── PausePeriod

Customer ─── Bill
```

This structure preserves pause history and keeps billing information separate from customer and subscription data.

---

## 5. Billing Logic

The most important requirement is accurate pro-rated billing.

Only **Monday-Friday** are considered service days.

```text
Scheduled Days = Service weekdays during subscription period

Paused Days = Unique paused weekdays

Served Days = Scheduled Days - Paused Days

Daily Rate = Monthly Price / Scheduled Days

Final Bill = Daily Rate × Served Days
```

A `set` is used when collecting paused dates so overlapping pause periods cannot deduct the same day twice.

### Example

```text
Monthly Plan = ₹3000
Scheduled Days = 22
Paused Days = 3
Served Days = 19

Final Bill ≈ ₹2590.91
```

---

## 6. Testing Approach

The backend was tested incrementally through FastAPI Swagger UI before frontend integration.

Test sequence:

```text
Create Customer
      ↓
Create Subscription
      ↓
Pause Subscription
      ↓
Resume Subscription
      ↓
Generate Monthly Bill
      ↓
Verify Billing Calculation
      ↓
Test Phone Lookup
      ↓
Test Dashboard
```

The billing test specifically verifies:

* Weekends are excluded
* Pause days are excluded
* Overlapping pauses are not double-counted
* Served days are calculated correctly
* Final amount is prorated correctly

---

## 7. Issues Found and Fixes

### Virtual Environment

The project was being run in GitHub Codespaces using Bash. A Windows PowerShell activation command caused an error.

**Incorrect:**

```bash
.\.venv\Scripts\Activate.ps1
```

**Fixed with:**

```bash
source .venv/bin/activate
```

### Missing Database Directory

Creating `database/__init__.py` initially failed because the directory did not exist.

**Fix:**

```bash
mkdir -p database
touch database/__init__.py
```

### Weekend Billing

A simple date calculation could include Saturday and Sunday.

**Fix:**

```python
day.weekday() < 5
```

This restricts service days to Monday-Friday.

### Overlapping Pauses

Adding pause periods directly could count the same date multiple times.

**Fix:** paused service dates are stored in a Python `set`.

### Duplicate Customers

Since customers are searched by phone number, duplicate phone numbers can cause ambiguity.

**Fix:** the phone field is unique and duplicate checks are performed before creating customers.

---

## 8. Development Strategy

Development is being completed in stages:

```text
Database & Environment
        ↓
Backend APIs
        ↓
Subscription Logic
        ↓
Pause/Resume
        ↓
Billing Engine
        ↓
Backend Testing
        ↓
React Frontend
        ↓
Integration Testing
```

The core billing workflow is validated before completing the frontend.

---

## 9. Key Design Decision

The main design decision is to keep **subscription history, pause history, and billing calculations separate**.

This allows the system to answer:

> How many service days were scheduled, how many were paused, and how much should the customer actually pay?

This provides a clear and maintainable foundation for future features such as invoices, notifications, payments, and reporting.

