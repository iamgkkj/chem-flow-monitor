# Chem Flow Monitor - Technical Documentation

## 1. Introduction

Chem Flow Monitor is a hybrid full-stack analytics platform built to demonstrate a unified architecture where a single powerful backend drives two completely different frontend interfaces: a modern web dashboard and a native desktop application.

The core problem this application solves is the analysis of industrial equipment data. It takes raw CSV logs from chemical machinery (pumps, compressors, etc.) and instantly turns them into actionable insights—statistical averages, type distributions, and downloadable PDF reports.

---

## 2. System Requirements

To run this project locally, your system needs to meet the following minimum requirements:

### General
*   **OS:** Windows 10/11, Ubuntu 20.04+ (or other Linux distros), macOS 12+
*   **RAM:** 4GB minimum (8GB recommended for comfortable development)
*   **Disk Space:** ~500MB for project files and virtual environments

### Software Dependencies
*   **Python:** Version 3.9 or higher (Tested with 3.10)
*   **Node.js:** Version 16 or higher (Received LTS recommended)
*   **npm:** Installed automatically with Node.js
*   **Git:** For version control

---

## 3. Project Architecture

The project follows a **Client-Server** architecture pattern.

1.  **Metric Server (Backend):** A Django application acts as the source of truth. It handles:
    *   Data ingestion (CSV parsing)
    *   Business logic (Statistical computation via Pandas)
    *   Data persistence (SQLite database)
    *   Authentication (Token-based)
2.  **Web Client:** A React.js Single Page Application (SPA) that consumes the API to render a responsive dashboard.
3.  **Desktop Client:** A PyQt5 (Python) application that provides a native OS experience, also consuming the exact same API.

This design ensures that business logic is never duplicated. If we update the calculation method for "Average Pressure", both the Web and Desktop apps reflect the change immediately without needing updates.

---

## 4. File Structure

Here is a high-level overview of the important files in the repository:

```text
chem-flow-monitor/
├── backend/                        # Django Project Root
│   ├── equipment/                  # Main App Logic
│   │   ├── models.py               # Database Schema (Dataset)
│   │   ├── views.py                # API Endpoints (Upload, List, Report)
│   │   ├── services.py             # Business Logic (Pandas processing)
│   │   └── reports.py              # PDF Generation Logic
│   ├── manage.py                   # Django CLI entry point
│   ├── backend.sh                  # Automation script (Linux)
│   └── backend.ps1                 # Automation script (Windows)
├── desktop/                        # PyQt5 Project Root
│   ├── main.py                     # Main Application Entry (GUI)
│   ├── api_client.py               # HTTP Client wrapper
│   ├── linuxrun.sh                 # Full-stack automation (Linux)
│   └── winrun.ps1                  # Full-stack automation (Windows)
├── web/                            # React Project Root
│   ├── src/
│   │   ├── App.js                  # Main React Component & Auth State
│   │   ├── api.js                  # Axios setup & Token handling
│   │   └── components/             # UI Components (Dashboard, Login)
│   ├── frontend.sh                 # Automation script (Linux)
│   └── frontend.ps1                # Automation script (Windows)
├── requirements.txt                # Backend Python Dependencies
└── README.md                       # Quick Start Guide
```

---

## 5. Development Process & Code Explanation

### A. The Backend (Python/Django)
The heart of the system. We started by defining the data model in `backend/equipment/models.py`. The `Dataset` model is designed to be immutable regarding the file content—once a CSV is uploaded, we immediately calculate its stats and save them as fields (`avg_flowrate`, `type_distribution`, etc.) to avoid re-calculating them on every read.

*   **CSV Parsing (`services.py`):** 
    *   `parse_equipment_csv(file)`: Validates headers and converts columns to numeric types.
    *   `compute_summary(df)`: Calculates averages (`avg_flowrate`, etc.) and determines type distribution using Pandas vectorization.
*   **API Views (`views.py`):** We use Django Rest Framework (DRF). The `DatasetUploadView` is the most complex endpoint. It receives the file, passes it to the generic service layer for parsing, saves the result, and then ensures we only keep the last 5 datasets to save space.

### B. The Desktop App (PyQt5)
Located in `desktop/main.py`. This is a traditional GUI programming approach.
*   **The Loop:** It starts an application event loop (`QApplication`).
*   **Login:** The first window is `LoginDialog`. It blocks the main window until a valid token is retrieved from the API.
*   **Dashboard:** The `MainWindow` uses a layout manager (`QVBoxLayout`, `QHBoxLayout`) to organize widgets.
*   **Plotting:** We embed **Matplotlib** directly into the interface using `FigureCanvasQTAgg`. This allows us to render scientific-grade charts natively.

### C. The Web App (React)
Located in `web/`.
*   **State:** We use React hooks (`useState`, `useEffect`) in `App.js` to manage the authentication state globally.
*   **Storage:** The Auth Token is stored in `sessionStorage` (in `api.js`). We chose `sessionStorage` over `localStorage` so that the user's session ends when they close the tab/window. This auto-logout feature is crucial for security and prevents stale token issues on the free database tier.
*   **Data:** Similar to the desktop app, it fetches JSON data from the API and renders it. For charts, it uses `Chart.js`, which is more "web-native" and interactive than Matplotlib.

---

## 6. Automation Scripts Reference

We have created a suite of scripts to make running this complex multi-part system easy.

### Full Stack Automation
These scripts set up *everything* (Backend + Desktop) in one go.

#### 🐧 `desktop/linuxrun.sh` (Linux/macOS)
1.  **Environment:** Checks for a `.venv`, creates it if missing, and activates it.
2.  **Dependencies:** Installs both backend and desktop requirements.
3.  **Database:** Runs migrations and creates the `demo` superuser automatically.
4.  **Execution:** Starts the Django server in the background (`&`), captures its Process ID (PID), then launches the Desktop app. When you close the Desktop app, it uses `kill $PID` to shut down the server cleanly.

#### 🪟 `desktop/winrun.ps1` (Windows)
1.  **Environment:** Similar check and creation of `.venv`.
2.  **Dependencies:** *Unique behavior:* Instead of reading `requirements.txt`, it installs packages like `pandas` and `numpy` individually. This is a crucial workaround for Windows environments to ensure `pip` finds the correct pre-built binary wheels and avoids complex C++ compilation errors.
3.  **Execution:** Starts the backend as a background process object and stops it when the script ends.

### Component Automation

#### `backend/backend.sh` & `backend/backend.ps1`
Dedicated scripts for running *only* the Django API. Useful if you want to develop the backend in isolation or run the Web Client against a local server. The Windows version also uses the individual package installation method for stability.

#### `web/frontend.sh` & `web/frontend.ps1`
Simple wrappers around `npm install` and `npm start`. They save you from typing the commands manually and are helpful for consistency (e.g., if we ever needed to add environment variable setup, we'd add it here).

---

## 7. Conclusion

This project serves as a reference implementation for modern Python-based tooling. By combining the calculation power of Pandas, the robustness of Django, and the flexibility of React/Qt, it delivers a powerful user experience across platforms.
