# test app.py
from fastapi.testclient import TestClient
from app import app
from datetime import datetime, timedelta

client = TestClient(app)

def test_generate_schedule_success():
    now = datetime.now()
    request_data = {
        "user_id": "test_user_1",
        "energy_level": [3, 2],
        "pomodoro_length": 25,
        "available_slots": [
            {
                "start_time": (now + timedelta(hours=1)).isoformat(),
                "end_time": (now + timedelta(hours=3)).isoformat()
            },
            {
                "start_time": (now + timedelta(hours=4)).isoformat(),
                "end_time": (now + timedelta(hours=6)).isoformat()
            }
        ],
        "tasks": [
            {
                "title": "Write essay",
                "due_date": (now + timedelta(days=1)).isoformat(),
                "duration_minutes": 60,
                "category": "Writing"
            },
            {
                "title": "Study math",
                "due_date": (now + timedelta(days=2)).isoformat(),
                "duration_minutes": 45,
                "category": "Math"
            }
        ]
    }

    response = client.post("/generate_schedule", json=request_data)
    assert response.status_code == 200
    data = response.json()
    assert data["user_id"] == "test_user_1"
    assert data["sessions"][0]["task"]["title"] == "Write essay"
    assert data["sessions"][1]["task"]["title"] == "Study math"
    assert len(data["sessions"]) == 2
    assert data["total_study_time"] >= 105
    assert data["success"] is True

def test_generate_schedule_missing_tasks():
    now = datetime.now()
    request_data = {
        "user_id": "test_user_2",
        "energy_level": [2],
        "pomodoro_length": 25,
        "available_slots": [
            {
                "start_time": (now + timedelta(hours=1)).isoformat(),
                "end_time": (now + timedelta(hours=2)).isoformat()
            }
        ],
        "tasks": []
    }

    response = client.post("/generate_schedule", json=request_data)
    assert response.status_code == 400
    assert response.json()["detail"] == "No tasks provided for scheduling."

def test_generate_schedule_not_enough_energy():
    now = datetime.now()
    request_data = {
        "user_id": "test_user_3",
        "energy_level": [3],
        "pomodoro_length": 25,
        "available_slots": [
            {
                "start_time": (now + timedelta(hours=1)).isoformat(),
                "end_time": (now + timedelta(hours=2)).isoformat()
            },
            {
                "start_time": (now + timedelta(hours=3)).isoformat(),
                "end_time": (now + timedelta(hours=4)).isoformat()
            }
        ],
        "tasks": [
            {
                "title": "Read chapter",
                "due_date": (now + timedelta(days=1)).isoformat(),
                "duration_minutes": 30,
                "category": "Reading"
            }
        ]
    }

    response = client.post("/generate_schedule", json=request_data)
    assert response.status_code == 400
    assert response.json()["detail"] == "Not enough energy for available time slots."