
# Chem Flow Monitor
**[🔴 Live Demo](https://chem-flow-web.onrender.com)** | **[📄 API Docs](https://chem-flow-backend.onrender.com/api/datasets/history/)**

**Username:** `demo`
**Password:** `demo12345`

<p align="center">
  <img src="https://github.com/iamgkkj/chem-flow-monitor/blob/861705097e9b611e1081ff3dd95c07fd5691c1ef/web/src/QR%20Code.png" alt="Scan me" width="300"/>
  <br>
  <em>Scan to test on mobile</em>
</p>

---
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

##  Quick Start

Follow these steps to set up the environment and run the application.

### 1. Backend Setup (Django) 

The backend must be running for either frontend to work. (DON'T Run this if you're running the automated script)

#### A. Linux setup
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

#### B. Windows setup
```bash
python -m venv .venv
.venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt

# Run migrations and setup database
python backend/manage.py migrate
python backend/manage.py createsuperuser --username demo --email demo@example.com
# (Set password to 'demo12345' to match the guide below, or choose your own)

# Start the server
python backend/manage.py runserver
```
---
### 2. Web Application Setup (React) 

Open a new terminal tab:

```bash
cd web # inside path/to/chem-flow-monitor/

# Install Node modules
npm install

# Start the development server
npm start

```

*The web app will open at `http://localhost:3000*`

### 3. Desktop Application Setup (PyQt5)
Please Use the application in Full screen mode after login for better experience.

#### A. Manual Setup (Recommended for Windows)
##### i. Linux setup
After running the backend setup (⚠️ crucial), follow these steps to run the desktop application:

Open a new terminal tab:

```bash
# Navigate to the desktop directory
cd desktop # inside path/to/chem-flow-monitor/

# Create a dedicated environment for desktop dependencies
python3 -m venv .venv
source .venv/bin/activate

# Install desktop requirements
pip install -r requirements.txt

# Launch the app
.venv/bin/python main.py

```
##### ii. Windows setup
```bash
# Navigate to the desktop directory
cd desktop # inside path/to/chem-flow-monitor/

# Create a dedicated environment for desktop dependencies
python -m venv .venv
.venv\Scripts\Activate.ps1

# Install desktop requirements
pip install -r requirements.txt

# Launch the app
.venv\Scripts\python main.py
```

#### B. Automated Setup (Optional: No backend setup required)

Open a new linux (or WSL) terminal and run the following commands:

```bash
# 1. Make sure you are in the project root
cd desktop # inside path/to/chem-flow-monitor/

# 2. Make the script executable (if you haven't already)
chmod +x linuxrun.sh

# 3. Run it
./linuxrun.sh
```
If you're running the file as a program from GUI then make sure the backend server is running.

---

## ✔ Evaluation & Usage Guide

To test the application features, use the provided sample data and credentials.

**Test Credentials:**

* **Username:** `demo`
* **Password:** `demo12345` (or the password you set during setup)

**Sample Data:**

* Use `sample_equipment_data.csv` located in the root of this repository.
<p align="center">
  <img src="https://github.com/iamgkkj/chem-flow-monitor/blob/cb71e401aa668ffe846712f0faa028a4e04b0f42/backend/screenshots/Screenshot%20from%202026-02-02%2003-39-14.png" width="300" alt="Desktop Application Login">
</p>
<p align="center">
  <img src="https://github.com/iamgkkj/chem-flow-monitor/blob/f83fd9dce12b8292dbdc02d9c0356561d33bbbfe/backend/screenshots/web%20login.png" width="800" alt="Web Login Screenshot">
</p>


### 🔌 Workflow

1. **Login:** Authenticate using the credentials above on either the Web or Desktop client.
2. **Upload:** Navigate to the dashboard and upload the sample CSV.
3. **Analyze:** View the generated "Summary Cards" and Charts (Pie/Bar).
4. **Report:** Click the "Generate PDF" button to download a comprehensive analysis report.
5. **History:** Upload the file again (or a modified version) to see the History tab update with the most recent entries.

<p align="center">
  <img src="https://github.com/iamgkkj/chem-flow-monitor/raw/861705097e9b611e1081ff3dd95c07fd5691c1ef/backend/screenshots/Screenshot%20from%202026-02-02%2000-07-20.png" width="800" alt="Web Application Screenshot1">
</p>
<p align="center">
  <img src="https://github.com/iamgkkj/chem-flow-monitor/blob/861705097e9b611e1081ff3dd95c07fd5691c1ef/backend/screenshots/Screenshot%20from%202026-02-02%2000-07-26.png" width="800" alt="Web Application Screenshot2">
</p>
<p align="center">
  <img src="https://github.com/iamgkkj/chem-flow-monitor/blob/cb71e401aa668ffe846712f0faa028a4e04b0f42/backend/screenshots/Screenshot%20from%202026-02-02%2003-39-31.png" width="800" alt="Desktop Application Screenshot">
</p>

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
* **Automated Script issues:** If the automated script fails to run, Please check if the backend server is running on port `8000` before running the script. Also allow the permissions to the script by running `chmod +x linuxrun.sh`. 
*If the script still fails to run, you should do manual setup as mentioned in the manual setup section.*
* **Desktop App Full Screen:** Please Use the application in Full screen mode after login for better experience.
* **Invisible password during initial setup** Keep in mind that the password is invisible during initial setup (Due to TUI limitations), but it is still being set. *Tip: hold backspace to clear the password and then type it again.*
* **Testing Application in Windows:** There is currently no automated setup for windows, you should do manual setup as mentioned in the manual setup section.

#### ⚠️ Important: 
If ```pip install -r requirements.txt``` fails to install dependencies in windows desktop, you should install them manually one by one.

---
## Thanks for reviewing my project, hope you liked it ＼(＾O＾)／

★ Please star the repository if you find it useful★
