
# Chem Flow Monitor

**Chemical Equipment Parameter Visualizer**

Chem Flow Monitor is a hybrid full-stack analytics platform designed to ingest, analyze, and visualize chemical equipment data. It operates as both a modern web dashboard and a standalone desktop application, powered by a unified Django backend.

This project was built to demonstrate a hybrid architecture where a single REST API drives multiple frontend interfaces (Web & Desktop) while maintaining consistent business logic and data integrity.

## ◕ Project Overview

The application solves the problem of analyzing batch CSV exports from industrial equipment. Users can upload raw datasets to generate instant analytics, including:
* **Statistical Analysis:** Automated calculation of mean flow rates, pressures, and temperatures.
* **Visualization:** Interactive charts for equipment type distribution and operational counts.
* **Reporting:** Generation of downloadable PDF reports for archival.
* **History:** Persistence of the last 5 uploaded datasets for quick comparison.

## Tech Stack

| Component | Technology | Description |
| :--- | :--- | :--- |
| **Backend** | Python, Django, DRF | REST API, Data Processing (Pandas), SQLite storage |
| **Web Frontend** | React.js, Chart.js | Responsive web dashboard |
| **Desktop Frontend** | Python, PyQt5, Matplotlib | Native desktop GUI |
| **Data Processing** | Pandas | CSV parsing and statistical computation |

##  Repository Structure

```text
.
├── backend/                # Django project root (API & Logic)
├── desktop/                # PyQt5 application source
│   ├── main.py             # Desktop app entry point
│   └── requirements.txt    # Desktop-specific dependencies
├── web/                    # React application source
├── sample_equipment_data.csv  # Test dataset
└── requirements.txt        # Backend dependencies

```

---

## ♣ Quick Start (Linux)

Follow these steps to set up the environment and run the application.

### 1. Backend Setup (Django) 

The backend must be running for either frontend to work.

```bash
# Create and activate virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run migrations and setup database
python backend/manage.py migrate
python backend/manage.py createsuperuser --username demo --email demo@example.com
# (Set password to 'demo12345' to match the guide below, or choose your own)

# Start the server
python backend/manage.py runserver

```

*Server runs at `http://127.0.0.1:8000*`

### 2. Web Application Setup (React) ✿

Open a new terminal tab:

```bash
cd web

# Install Node modules
npm install

# Start the development server
npm start

```

*The web app will open at `http://localhost:3000*`

### 3. Desktop Application Setup (PyQt5) π

Open a new terminal tab:

```bash
# Create a dedicated environment for desktop dependencies
python3 -m venv desktop/.venv
source desktop/.venv/bin/activate

# Install desktop requirements
pip install -r desktop/requirements.txt

# Launch the app
python desktop/main.py

```

---

## ✔ Evaluation & Usage Guide

To test the application features, use the provided sample data and credentials.

**Test Credentials:**

* **Username:** `demo`
* **Password:** `demo12345` (or the password you set during setup)

**Sample Data:**

* Use `sample_equipment_data.csv` located in the root of this repository.

### ✿ Workflow

1. **Login:** Authenticate using the credentials above on either the Web or Desktop client.
2. **Upload:** Navigate to the dashboard and upload the sample CSV.
3. **Analyze:** View the generated "Summary Cards" and Charts (Pie/Bar).
4. **Report:** Click the "Generate PDF" button to download a comprehensive analysis report.
5. **History:** Upload the file again (or a modified version) to see the History tab update with the most recent entries.

## ☁ API Reference

The backend exposes the following endpoints for the frontend clients:

* `POST /api/auth/token/` - Obtain authentication token.
* `POST /api/datasets/upload/` - Upload CSV (Multipart form data).
* `GET /api/datasets/<id>/` - Retrieve analytics for a specific dataset.
* `GET /api/datasets/<id>/report/` - Download PDF report.
* `GET /api/datasets/history/` - List last 5 uploads.

## ▲ Troubleshooting

* **Connection Refused:** Ensure the Django backend is running on port `8000` before launching the frontends.
* **Upload Failed:** Ensure the CSV file strictly follows the format: `Equipment Name, Type, Flowrate, Pressure, Temperature`.
* **Desktop App Scaling:** If the PyQt5 window appears too small on high-DPI displays, you may need to set the environment variable: `export QT_AUTO_SCREEN_SCALE_FACTOR=1`.

---
## Thanks for reviewing my project, hope you liked it ＼(＾O＾)／

★ Please star the repository if you find it useful★