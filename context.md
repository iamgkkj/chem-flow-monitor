# Project Context: Chemical Equipment Parameter Visualizer

## Goals
- Build a shared **Django + Django REST Framework** backend used by:
  - React.js + Chart.js web frontend
  - PyQt5 + Matplotlib desktop frontend
- Support CSV upload (Equipment Name, Type, Flowrate, Pressure, Temperature)
- Compute analytics via Pandas:
  - Total equipment count
  - Average Flowrate/Pressure/Temperature
  - Distribution of equipment types
- Persist last 5 uploaded datasets + summaries in SQLite
- Provide PDF report generation
- Implement basic authentication

## Progress
- [x] Backend scaffolding (Django + DRF) created
- [x] CSV upload + validation implemented
- [x] Analytics endpoints implemented
- [x] History (last 5) implemented
- [x] Authentication implemented
- [x] PDF report implemented
- [x] Web frontend (React + Chart.js) implemented
- [ ] Desktop frontend (PyQt5 + Matplotlib) implemented

## Current Status
- Created `requirements.txt` for backend dependencies.
- Local Python venv (`.venv`) is required because system Python is externally managed (PEP 668).

## Backend API (implemented)
- `POST /api/auth/token/` (DRF token auth)
- `POST /api/datasets/upload/` (multipart field `file`)
- `GET /api/datasets/history/` (last 5 uploads)
- `GET /api/datasets/<id>/`
- `GET /api/datasets/<id>/report/` (PDF)

## Reporting
- PDF report now includes: summary + type distribution list + embedded charts.
- Charts layout: pie chart page first, then bar chart page, both centered with titles (prevents overlap).
- Charts sizing: pie and bar drawings reduced to ~50% to avoid overpowering the page.

## How to run (dev)
- Start server: `../.venv/bin/python manage.py runserver` (run from `backend/`)

## Web Frontend
- Location: `web/`
- Tech: React + Chart.js (`react-chartjs-2`) + Axios
- Dev proxy: `web/package.json` proxies to `http://127.0.0.1:8000`
- UI: blue header, light/dark theme toggle, footer credits + social links, pie chart percentage labels
- Charts: pie chart uses a multi-color palette for better visual separation; bar chart remains blue-themed.
- Bar chart: value labels on bars set to white for readability.
- Branding: updated header/login branding with new logo assets; removed default React app title/manifest branding.

## How to run (dev) - Web
- Backend (terminal 1): run from `backend/` -> `../.venv/bin/python manage.py runserver`
- Web (terminal 2): run from `web/` -> `npm start`

## Desktop Frontend
- Location: `desktop/`
- Tech: PyQt5 + Matplotlib + requests
- Entry point: `desktop/main.py`
- UI: primary/secondary button styling; title area is plain text (no highlighted header bar).

## How to run (dev) - Desktop
- Backend: run from `backend/` -> `../.venv/bin/python manage.py runserver`
- Desktop deps:
  - `python3 -m venv desktop/.venv`
  - `desktop/.venv/bin/pip install -r desktop/requirements.txt`
- Run app:
  - `desktop/.venv/bin/python desktop/main.py`

## Smoke Test (completed)
- Created demo user: `demo` / `demo12345`
- Token auth: `POST /api/auth/token/` => 200
- Upload sample CSV: `POST /api/datasets/upload/` => 201 (dataset id `1`)
- History: `GET /api/datasets/history/` => 200 (len 1)
- Detail: `GET /api/datasets/1/` => 200 (`total_count` 15)
- Report: `GET /api/datasets/1/report/` => 200 (`application/pdf`, ~2013 bytes)

## Decisions / Notes
- Repo root: `/home/gopal/Desktop/Fossee`
- Sample CSV present: `sample_equipment_data.csv`
- README updated with full setup, architecture, API endpoints, repository tree, and usage flow.

