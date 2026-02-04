# Chem Flow Monitor
**[🔴 Live Demo](https://chem-flow-monitor.onrender.com/)** | **[📄 API Docs](https://chem-flow-backend.onrender.com/api/datasets/history/)** | **[📄 Project Documentation](https://docs.google.com/document/d/1sbKwdR0MgMHTLUGTTjjW1WPOu5JB55w-su5mencRrjU/edit?usp=sharing)**

**Username:** `demo`
**Password:** `demo12345`

<p align="center">
  <img src="https://github.com/iamgkkj/chem-flow-monitor/blob/861705097e9b611e1081ff3dd95c07fd5691c1ef/web/src/QR%20Code.png" alt="Scan me" width="300"/>
  <br>
  <em>Scan to test on mobile</em>
  <br>
  <sub>(Enable Desktop mode in browser-recommended)</sub>
</p>

> [!NOTE]
> **Render.com** free tier deployment may take some time (up to 1-2 minutes) to reactivate after a period of inactivity. Please be patient while the live demo loads.

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

#### Automated Setup (Optional)
Run the entire stack with a single script:

##### Linux / macOS
```bash
cd desktop
chmod +x linuxrun.sh
./linuxrun.sh
```

> [!TIP]
> **GUI execution (Linux):** You can also run the script without the terminal. Right-click `linuxrun.sh` > **Properties** > **Permissions** > Check **"Allow executing file as program"**. After that, you can simply right-click the file and select **"Run as a program"** anytime.
> 
> **GUI execution (macOS):** Rename `linuxrun.sh` to `linuxrun.command`. You can then double-click it to run. (You may need to `chmod +x linuxrun.command` once from terminal).

##### Windows
```powershell
cd desktop
./winrun.ps1
```

> [!TIP]
> **GUI execution (Windows):** After setting the execution policy (see Troubleshooting), you can run the script without opening a terminal manually. Right-click `winrun.ps1` and select **"Run with PowerShell"**.

### 1. Backend Setup (Django) 

The backend must be running for either frontend to work.

#### A. Linux setup
##### Automated Setup (Recommended)
```bash
cd backend
chmod +x backend.sh
./backend.sh
```

##### Manual Setup
```bash
# Create and activate virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
python -m pip install --upgrade pip
pip install Django==4.2.10 djangorestframework==3.14.0 pandas==2.2.0 reportlab==4.0.9 django-cors-headers==4.3.1 gunicorn --only-binary :all:

# Run migrations and setup database
python3 backend/manage.py migrate
python3 backend/manage.py createsuperuser --username demo --email demo@example.com
# (Set password to 'demo12345' to match the guide below, or choose your own)

# Start the server
python3 backend/manage.py runserver

```

#### B. Windows setup
##### Automated Setup (Recommended)
```powershell
cd backend
./backend.ps1
```

##### Manual Setup
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

*Server runs at `http://127.0.0.1:8000`*

---
### 2. Web Application Setup (React) 

#### Automated Setup (Recommended)
You can run the frontend efficiently using the provided scripts.

##### Linux / macOS
```bash
cd web
chmod +x frontend.sh
./frontend.sh
```

##### Windows
```powershell
cd web
./frontend.ps1
```

*The web app will open at `http://localhost:3000`*

> [!TIP]
> **Access on Local Network:** You can access the web dashboard from other devices (e.g. mobile) on the same Wi-Fi network. Check the terminal output after starting the frontend for the **"On Your Network"** URL (e.g., `http://192.168.x.x:3000`).

### 3. Desktop Application Setup (PyQt5)
Please Use the application in Full screen mode after login for better experience.

#### A. Automated Setup (Recommended)

Run the desktop application easily with the provided scripts.

##### Linux / macOS
```bash
# Navigate to desktop directory
cd desktop

# Make executable and run
chmod +x linuxrun.sh
./linuxrun.sh
```

##### Windows
```powershell
cd desktop
./winrun.ps1
```

> [!NOTE]
> The automated scripts (especially on Windows) handle dependency installation and backend startup for you.

#### B. Manual Setup (Optional)
If you prefer to control the environment yourself.

##### i. Linux setup
After running the backend setup (⚠️ crucial), follow these steps:

```bash
# Navigate to the desktop directory
cd desktop

# Create and activate virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install desktop requirements
pip install -r requirements.txt

# Launch the app
.venv/bin/python3 main.py
```

##### ii. Windows setup
```powershell
# Navigate to the desktop directory
cd desktop

# Create virtual environment
python -m venv .venv
.venv\Scripts\Activate.ps1

# Install desktop requirements (Install individually to avoid version conflicts)
pip install PyQt5 matplotlib requests

# Launch the app
.venv\Scripts\python main.py
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
* **Invisible password during initial setup:** Keep in mind that the password is invisible during initial setup (Due to TUI limitations), but it is still being set. *Tip: hold backspace to clear the password and then type it again.*
* **Testing Application in Windows:** You can use the automated `winrun.ps1` script in PowerShell for a quick setup. If it fails, follow the manual setup.
* **Incorrect Python Environment:** If you get "ModuleNotFoundError", ensure you are using the virtual environment. It is safer to use the explicit path: `.venv/bin/python3` (Linux/Mac OS) or `.venv\Scripts\python` (Windows) instead of just `python`.
* **Bad Request (400) in Windows:** If you can't login with the demo credentials, it might be because the automation script created a new superuser with your system's specific environment. Try logging in with the username/password you manually set (if any) or check the script output for user creation status.

#### ⚠️ Important: 
**Windows Execution Policy Error:**
If you see "running scripts is disabled on this system", run this command in PowerShell as Administrator:
```powershell
Set-ExecutionPolicy -ExecutionPolicy Unrestricted -Scope LocalMachine -Force
```

**Dependency Installation Error:**
If dependencies fail to install (e.g. `numpy` build error), ensure you have the latest `pip`:
```powershell
python -m pip install --upgrade pip
```
Then try running `winrun.ps1` again.

---
## Thanks for reviewing my project, hope you liked it ＼(＾O＾)／

★ Please star the repository if you find it useful★
