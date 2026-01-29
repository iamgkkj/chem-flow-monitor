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

## Current Status
- Created `requirements.txt` for backend dependencies.
- Local Python venv (`.venv`) is required because system Python is externally managed (PEP 668).

## Backend API (implemented)
- `POST /api/auth/token/` (DRF token auth)
- `POST /api/datasets/upload/` (multipart field `file`)
- `GET /api/datasets/history/` (last 5 uploads)
- `GET /api/datasets/<id>/`
- `GET /api/datasets/<id>/report/` (PDF)

## How to run (dev)
- Start server: `../.venv/bin/python manage.py runserver` (run from `backend/`)

## Decisions / Notes
- Repo root: `/home/gopal/Desktop/Fossee`
- Sample CSV present: `sample_equipment_data.csv`

