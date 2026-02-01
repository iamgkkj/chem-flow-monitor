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
- [x] Desktop frontend (PyQt5 + Matplotlib) implemented
