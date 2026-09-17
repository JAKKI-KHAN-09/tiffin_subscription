# AI Logs - Tiffin Subscription Project

## Date
2026-09-17

## Project summary
This project is a full-stack tiffin subscription management system built with:
- Frontend: React + Vite
- Backend: FastAPI
- Database: SQLAlchemy + SQLite for local development
- Repo root: /workspaces/tiffin_subscription
- Project folder: /workspaces/tiffin_subscription/tiffin-management-system

## Major project goals completed
- Created a monorepo structure for frontend and backend.
- Fixed backend import and database configuration issues.
- Enabled SQLite for local development instead of PostgreSQL.
- Added CORS support for frontend access on localhost:5173.
- Fixed customer creation flow so Add Customer works with proper feedback.
- Added backend health and root routes.
- Extended the app with twist requirements:
  - T1: daily delivery notifications via clock/outbox
  - T6: mid-cycle subscription transfer
  - T4: messy customer import with dedupe/reject summary
- Added backend tests covering the twist functionality.
- Pushed the repository updates to GitHub.

## Important technical findings
### Backend run command
```bash
cd /workspaces/tiffin_subscription/tiffin-management-system/backend
source ../.venv/bin/activate
PYTHONPATH=.. uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### Frontend run command
```bash
cd /workspaces/tiffin_subscription/tiffin-management-system/frontend
npm install
npm run dev -- --host 0.0.0.0
```

### App URLs
- Frontend: http://localhost:5173
- Backend: http://localhost:8000
- Health check: http://localhost:8000/health

### Main backend files
- backend/app/main.py
- backend/app/api/customers.py
- backend/app/api/subscriptions.py
- backend/app/api/clock.py
- backend/app/api/outbox.py
- backend/app/services/subscription_service.py
- database/models.py
- database/database.py

### Main frontend files
- frontend/src/App.jsx
- frontend/src/pages/AddCustomer.jsx
- frontend/src/services/api.js

## Key debugging issues fixed
- Python module import path issue (`app` / `database` not found)
- SQLite DB config mismatch
- CORS issue between frontend and backend
- Port 8000 conflicts during backend restarts
- Lack of user visible feedback when adding customer
- Missing schema initialization for SQLAlchemy models

## Twist requirements implemented
### T1 — Notification service / outbox
Daily delivery reminder logic was added through:
- POST /api/clock
- GET /api/outbox

This checks active, non-paused subscriptions and writes notification records to the outbox.

### T6 — Subscription transfer
The system supports transferring an existing subscription to a new customer mid-cycle while preserving the plan and cycle context.

Endpoint:
- POST /api/subscriptions/{subscription_id}/transfer

### T4 — Messy customer import
The app accepts a messy customer list and returns:
- imported
- deduped
- rejected

The import flow normalizes phone numbers, handles duplicates, and rejects empty required fields.

## Validation status
The targeted regression tests pass for the new twist requirements:
```bash
cd /workspaces/tiffin_subscription/tiffin-management-system
source .venv/bin/activate
PYTHONPATH=backend pytest tests/backend/test_twists.py -q
```
Result:
- 3 passed
- 0 failed

## Git status and push summary
The repo was updated and pushed to GitHub successfully.

## Notes
This file serves as a summary of the work done so far for continuity and future debugging.

