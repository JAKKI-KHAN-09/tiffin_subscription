# AI Logs - Tiffin Subscription Project

## Date
2026-09-17

## Session overview
This file contains the complete working log of the project work done so far in this session, including repo setup, backend/frontend fixes, twist-feature implementation, GitHub updates, and final run instructions.

## 1) Initial objective
The user wanted the project structure created inside the repository folder and later extended with required backend/feature logic.

Tasks requested during the session included:
- create the project structure
- paste backend folder contents into the project
- run the model/app
- improve the UI for better user interaction
- run the project manually step by step
- check project errors and fix them
- identify why Add Customer did not work
- implement the twist requirements
- push the project updates to GitHub
- keep a permanent AI log in the repository

## 2) Project structure created
The repo was organized as:
- /workspaces/tiffin_subscription
- /workspaces/tiffin_subscription/tiffin-management-system
- frontend/
- backend/
- database/
- tests/
- docs/

The working project uses:
- React + Vite frontend
- FastAPI backend
- SQLAlchemy ORM
- SQLite database for local development

## 3) Problems found and fixed during the session
### Issue 1: Import path mismatch
Symptoms:
- ModuleNotFoundError: No module named 'app'
- ModuleNotFoundError: No module named 'database'

Root cause:
- The app was being started from the wrong directory and PYTHONPATH was not set correctly.

Fix:
```bash
cd /workspaces/tiffin_subscription/tiffin-management-system/backend
source ../.venv/bin/activate
PYTHONPATH=.. uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### Issue 2: Wrong database configuration
The project was pointing to PostgreSQL settings even though no PostgreSQL server was running.

Fix:
- switched to SQLite local config
- ensured tables are created on startup

### Issue 3: Frontend could not reach backend
Problem:
- browser fetch failed
- CORS errors occurred

Fix:
- configured FastAPI CORS middleware for localhost:5173

### Issue 4: Port 8000 was already occupied
The backend was failing to start because an old uvicorn instance was still running.

Fix:
```bash
lsof -nP -i :8000
kill -9 <PID>
```

### Issue 5: Add Customer looked non-responsive
The form did not show success/error states.

Fix:
- added loading state
- added success/error message handling
- kept form reset on successful insert

### Issue 6: DB schema initialization was missing
The database metadata existed, but the app sometimes started without table creation.

Fix:
- create all tables during startup
- also ensure model imports load before metadata creation

## 4) Final working app commands
### Backend
```bash
cd /workspaces/tiffin_subscription/tiffin-management-system/backend
source ../.venv/bin/activate
PYTHONPATH=.. uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### Frontend
```bash
cd /workspaces/tiffin_subscription/tiffin-management-system/frontend
npm install
npm run dev -- --host 0.0.0.0
```

### Browser URLs
- Frontend: http://localhost:5173
- Backend: http://localhost:8000
- Health check: http://localhost:8000/health

## 5) Twist / advanced requirements implemented
### T1 — Daily delivery notification flow
Implemented a clock-based notification outbox flow.

Files added/updated:
- backend/app/api/clock.py
- backend/app/api/outbox.py
- database/models.py

Behavior:
- POST /api/clock generates delivery notifications for active, non-paused, due-today subscriptions
- GET /api/outbox returns queued outbound notifications

### T6 — Mid-cycle subscription transfer
Implemented subscription transfer functionality so a subscription can be reassigned to a new customer mid-cycle while keeping the plan and cycle details.

Files involved:
- backend/app/api/subscriptions.py
- backend/app/services/subscription_service.py
- backend/app/schemas/subscription.py

Endpoint:
```http
POST /api/subscriptions/{subscription_id}/transfer
```

### T4 — Messy customer import workflow
Implemented a messy-data import flow with deduplication and reporting.

Files involved:
- backend/app/api/customers.py

Behavior:
- accepts rows with duplicate phone numbers
- handles mixed date formats
- ignores blanks or invalid data
- returns counts for:
  - imported
  - deduped
  - rejected

## 6) Core project files
### Backend
- backend/app/main.py
- backend/app/api/customers.py
- backend/app/api/subscriptions.py
- backend/app/api/pauses.py
- backend/app/api/billing.py
- backend/app/api/dashboard.py
- backend/app/api/clock.py
- backend/app/api/outbox.py
- backend/app/services/customer_service.py
- backend/app/services/subscription_service.py
- backend/app/services/pause_service.py
- backend/app/services/billing_service.py
- backend/app/schemas/customer.py
- backend/app/schemas/subscription.py
- backend/app/schemas/pause.py
- backend/app/config.py

### Database
- database/models.py
- database/database.py
- database/seed.py

### Frontend
- frontend/src/App.jsx
- frontend/src/pages/AddCustomer.jsx
- frontend/src/services/api.js

## 7) Validation performed
We ran the twist tests and verified they pass.

Command used:
```bash
cd /workspaces/tiffin_subscription/tiffin-management-system
source .venv/bin/activate
PYTHONPATH=backend pytest tests/backend/test_twists.py -q
```

Result:
- 3 passed
- 0 failed

## 8) GitHub push summary
The updates were pushed to GitHub successfully after rebasing on the latest remote branch.

Commands used:
```bash
cd /workspaces/tiffin_subscription
git add .
git commit -m "Add twist features and backend fixes"
git push origin main
```

If remote rejected the push because it was behind, the solution was:
```bash
git pull --rebase origin main
git push origin main
```

## 9) Final notes
The base app works, the twist requirements were implemented, the project was saved to GitHub, and a permanent log was written to the repo root as AI_LOGS.md.

This file captures the work done so far and acts as a record for continuity, debugging, and future work.

