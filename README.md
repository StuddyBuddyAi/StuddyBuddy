<p align="center">
  <img src="docs/studybuddy_logo.png" alt="StudyBuddy Logo" width="200" />
</p>

<h1 align="center">StudyBuddy AI</h1>

<p align="center">
  Your intelligent study companion — powered by Unity and AI.
</p>

<p align="center">
  <a href="https://github.com/StuddyBuddyAi/StuddyBuddy/issues">
    <img alt="Issues" src="https://img.shields.io/github/issues/StuddyBuddyAi/StuddyBuddy?style=flat-square&logo=github">
  </a>
  <a href="https://github.com/StuddyBuddyAi/StuddyBuddy/blob/main/LICENSE">
    <img alt="License" src="https://img.shields.io/badge/license-pending-lightgrey?style=flat-square">
  </a>
</p>

---

## 📚 About the Project

**StudyBuddy AI** is a cross-platform productivity app that combines the power of Unity with a Python-based AI backend. Designed to support students with adaptive study schedules, task reminders, and break recommendations, the goal is to provide a lightweight but smart personal study assistant.

This project is part of a collaborative development effort and is currently under active development.

## 🚀 Features (Planned & In Progress)

- AI-generated study schedules based on deadlines and energy levels
- Adaptive Pomodoro timers with smart break reminders
- Visual task timeline and calendar views
- Continuous habit tracking and personalized feedback

## Technologies
- Unity
- C# 
- Python backend integration using FastAPI

## 🛠️ Installation

- Download the Build folder from the OneDrive or the GitHub
- Run the exe file inside for the current runnable build

## Development Setup

### Clone the Repository

```bash
git clone https://github.com/StuddyBuddyAi/StuddyBuddy.git
cd StuddyBuddy
```

### Python Backend Setup

Please follow the full backend setup guide here:
📄 [docs/setup-python-backend.md](docs\setup-python-backend.md)

Steps include:
- Creating and activating a Python ```venv```
- Installing dependencies with ```pip```
- Running the FastAPI server (```uvicorn app:app --reload```)
- Testing the ```/ping``` endpoint from Unity

### Unity Setup

- Open the project folder via Unity Hub
- Load the test scene and press Play
- Use the PingTester.cs script to verify server communication

Make sure the Python server is running locally before entering Play mode.

## 🤝 Contribution

We welcome contributions once the core system is stabilized. For now, teammates should:

- Use feature branches (e.g. feature/SCRUM-###-pomodoro-ui) <-- SCRUM ID based on task in Jira Board
- Submit pull requests with clear descriptions
- Follow our style tile for UI consistency

A full contribution guide will be added soon.

## 📄 License

This project is currently shared within the scope of a team project and is not yet licensed for public distribution. License to be added in final release phase.

## 👥 Project Contributors 

- [Anastasia Altamirano](https://github.com/anapaltami)
- [Michael Nathan Belisaire](https://github.com/SoldierTaker)
- [Nathaniel McCleery](https://github.com/nate254347)

## 🧪 Current Project Status : Pre-Alpha stage

| Component             | Status                        |
| --------------------- | ----------------------------- |
| Python API Server     | ✅ Ping endpoint working       |
| Unity HTTP Connection | ✅ Working via UnityWebRequest |
| AI Schedule Stub      | 🔧 In development             |
| Pomodoro Timer Logic  | ⏳ Planned                    |
| Habit Tracking        | ⏳ Planned                     |

## 🙌 Credits

- Logo based on an illustration by [Design.com] – Modified for the project
- Owl mascot & icon style inspired by [Study-focused UI trends]
- Fonts: ADLaM Display, Aharoni, Quicksand

### 🎨 Custom Color Palette
|  | Name | Hex | RGB | HSL |
| --- | --- | --- | --- | --- |
| ![](docs/000000.png) | Black | `#000000` | `rgb(0, 0, 0)` | `hsl(0, 0%, 0%)` |
| ![](docs/FFFFFF.png) | White | `#FFFFFF` | `rgb(255, 255, 255)` | `hsl(0, 0%, 100%)` |
| ![](docs/3DA0F1.png) | Azure | `#3DA0F1` | `rgb(61, 160, 241)` | `hsl(207, 87%, 59%)` |
| ![](docs/7DDA58.png) | Green | `#7DDA58` | `rgb(125, 218, 88)` | `hsl(99, 69%, 60%)` |
| ![](docs/98F5F9.png) | Aqua | `#98F5F9` | `rgb(152, 245, 249)` | `hsl(183, 88%, 79%)` |
| ![](docs/B06CE9.png) | Violet | `#B06CE9` | `rgb(176, 108, 233)` | `hsl(271, 73%, 67%)` |
| ![](docs/BBD9FF.png) | Sky Blue | `#BBD9FF` | `rgb(187, 217, 255)` | `hsl(215, 100%, 87%)` |
| ![](docs/EFC3CA.png) | Blush | `#EFC3CA` | `rgb(239, 195, 202)` | `hsl(349, 60%, 85%)` |
| ![](docs/FE9900.png) | Orange | `#FE9900` | `rgb(254, 153, 0)` | `hsl(35, 100%, 50%)` |

