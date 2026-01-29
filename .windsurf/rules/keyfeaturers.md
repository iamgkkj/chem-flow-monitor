---
trigger: always_on
---
# Internship Screening Task: Chemical Equipment Parameter Visualizer

[cite_start]**Objective:** Build a hybrid application that operates as both a **Web Application** and a **Desktop Application** using a shared backend[cite: 2, 7].

---

## 1. Fixed Tech Stack Rules
[cite_start]You must strictly adhere to the following technologies[cite: 10, 11]:

| Layer | Technology | Purpose |
| :--- | :--- | :--- |
| **Frontend (Web)** | React.js + Chart.js | Display tables & charts on the web |
| **Frontend (Desktop)** | PyQt5 + Matplotlib | Display visualization on desktop |
| **Backend** | Django + Django REST Framework | Common API for both frontends |
| **Data Logic** | Pandas | Reading CSV & performing analytics |
| **Database** | SQLite | Store history of uploaded datasets |
| **Version Control** | Git & GitHub | Collaboration & submission |

---

## 2. Core Functional Requirements

### A. Data Input (CSV Upload)
* [cite_start]**Web & Desktop:** Both interfaces must allow users to upload a CSV file[cite: 13].
* [cite_start]**Input Format:** The CSV will contain the following columns: *Equipment Name, Type, Flowrate, Pressure, Temperature*[cite: 7].
* [cite_start]**Sample Data:** Use the provided `sample equipment data.csv` for testing and demo purposes[cite: 11, 18].

### B. Backend Processing (The Brain)
* [cite_start]The Django backend must parse the uploaded CSV using **Pandas**[cite: 8, 11].
* It must expose an **API** that returns:
    * [cite_start]Total count of equipment[cite: 14].
    * [cite_start]Average values (Flowrate, Pressure, Temperature)[cite: 14].
    * [cite_start]Distribution of Equipment Types[cite: 14].

### C. Visualization & Display
* [cite_start]**Web:** Use **Chart.js** to display data tables, charts, and summaries[cite: 9].
* [cite_start]**Desktop:** Use **Matplotlib** embedded in **PyQt5** to display the same visualizations[cite: 9, 11].

### D. History & Reporting
* [cite_start]**History Management:** The application must store and retrieve the **last 5 uploaded datasets** with their summaries[cite: 16].
* [cite_start]**Reporting:** Generate a PDF report of the analysis[cite: 17].
* [cite_start]**Security:** Implement basic authentication[cite: 17].

---

## 3. Extras


* [cite_start]**Documentation:** A `README.md` file with clear setup instructions (must be in the repo)[cite: 24].

also make a python environment file for the project along with a gitignore file to ignore any unnecessary files.