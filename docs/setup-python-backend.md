# 🧠 StudyBuddy AI – Python Backend Setup Guide

This guide will walk you through setting up the Python backend (/PythonAI/) for the StudyBuddy project. It assumes you already have the Unity project running from the main branch and want to integrate the backend for AI scheduling functionality.

---

## 📁 Folder Structure Overview

Make sure your folder looks like this:

StudyBuddy/
├── Assets/
├── PythonAI/
│ ├── ai_model.py
│ ├── app.py
│ ├── README.md <-- You are here! 👌
│ ├── requirements.txt
│ └── venv/ <-- will be created for you
├── ProjectSettings/
├── .gitignore
└── ...

---

## 🧩 Prerequisites

- **Python 3.8+** installed
- pip (comes with Python)
- Git access to the feature/ai-backend-integration branch
- One of the following editors:
  - ✅ Visual Studio Code (recommended)
  - ✅ Visual Studio 2022 (with Python workload)

---

## 🛠️ Step-by-Step Setup

### ✅ 1. Clone the Feature Branch

bash
git clone https://github.com/nate254347/StuddyBuddy.git
cd StuddyBuddy
git checkout feature/ai-backend-integration


---

### 🧪 2. Set Up the Python Environment

Navigate into the backend folder:
bash
cd PythonAI


Create a virtual environment:
bash
python -m venv venv

This creates an isolated Python environment just for this project.

---

### ▶ 3. Activate the Virtual Environment

#### If Using VS Code (Recommended)
- Open VS Code to the PythonAI folder:
   - File → Open Folder → PythonAI
- Open the terminal in VS Code (Ctrl + ~)

Run:
bash
# in PowerShell if on Windows
.\venv\Scripts\Activate.ps1

# OR CMD
venv\Scripts\activate.bat

You should see (venv) in your terminal prompt.

#### If Using Visual Studio 2022
- Open Visual Studio
- Go to File → Open → Folder... and select PythonAI
- Visual Studio should detect the Python environment and prompt to create a requirements.txt environment.
- If not, open the terminal via View → Terminal, and activate manually as above.

⚠️ If you're not seeing the environment activate in Visual Studio, make sure the Python development workload is installed from the Visual Studio Installer.

---

### 📦 4. Install Dependencies

With the virtual environment activated:
bash
pip install -r requirements.txt

This installs:
- FastAPI (web framework)
- Uvicorn (server runner)
- Pydantic (data models)

---

### 🚀 5. Run the FastAPI Server

Still in the PythonAI folder and with venv active:
bash
uvicorn app:app --reload


You should see output like:
bash
Uvicorn running on http://127.0.0.1:8000


---

### 🌐 6. Test the Server

Open a browser and go to:
- http://localhost:8000/ping
   → Should return:
   
bash
   {"message": "pong"}


You can also test the interactive docs at:
http://localhost:8000/docs

---

### 🧩 7. Unity Integration Test

If the Unity project is open:
- Open the test scene that includes the PingTester script or AI HTTP client
- Enter Play Mode
- You should see the response in Unity's Console:
css
Response from server: {"message":"pong"}


---

### ✅ You're Done!

You’ve now successfully:
- Set up the Python backend with virtual environment
- Installed and verified dependencies
- Ran the FastAPI server
- Connected Unity to the backend

Let a teammate know if you hit any errors or need to reset your environment.

---

### 🧹 7. Bonus Troubleshooting Tips

If something breaks:
- Re-run the venv activation script
- Try pip install fastapi uvicorn manually if needed
- Re-clone the repo into a clean folder if venv gets corrupted