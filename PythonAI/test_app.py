# test app.py by running pytest test_app.py
from fastapi.testclient import TestClient
from app import app
from datetime import datetime, timedelta
from unittest.mock import patch

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

def test_generate_schedule_with_unschedulable_task():
    now = datetime.now()
    request_data = {
        "user_id": "test_unshedulable_user",
        "energy_level": [3],
        "pomodoro_length": 25,
        "available_slots": [
            {
                "start_time": (now + timedelta(hours=1)).isoformat(),
                "end_time": (now + timedelta(hours=2)).isoformat()
            }
        ],
        "tasks": [
            {
                "title": "Big Task",
                "due_date": (now + timedelta(days=1)).isoformat(),
                "duration_minutes": 120,  # Longer than the available slot
                "category": "Overflow"
            }
        ]
    }

    response = client.post("/generate_schedule", json=request_data)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is False
    assert "warnings" in data
    assert len(data["warnings"]) == 1
    assert "Big Task" in data["warnings"][0]

def test_generate_ai_schedule_structure():
    response = client.post("/generate_ai_schedule/", json={
        "user_id": "test_user_4",
        "energy_level": [3, 2],
        "pomodoro_length": 25,
        "available_slots": [
            {
                "start_time": "2025-06-11T10:00:00",
                "end_time": "2025-06-11T12:00:00"
            },
            {
                "start_time": "2025-06-11T14:00:00",
                "end_time": "2025-06-11T16:00:00"
            }
        ],
        "tasks": [
            {
                "title": "Write history essay",
                "due_date": "2025-06-12T23:59:59",
                "duration_minutes": 60,
                "category": "History"
            },
            {
                "title": "Review math notes",
                "due_date": "2025-06-12T23:59:59",
                "duration_minutes": 45,
                "category": "Math"
            }
        ]
    })

    assert response.status_code == 200
    data = response.json()
    assert data["user_id"] == "test_user_4"
    assert len(data["sessions"]) > 0
    assert all("task" in session for session in data["sessions"])
    assert all("start_time" in session for session in data["sessions"])
    assert all("end_time" in session for session in data["sessions"])

def test_generate_ai_schedule_with_mock():
    mock_response = [
        {
            "task": "Mocked Essay",
            "start": "2025-06-11T10:00:00",
            "end": "2025-06-11T10:30:00",
            "category": "Mocking"
        }
    ]

    request_data = {
        "user_id": "mock_user",
        "energy_level": [3],
        "pomodoro_length": 25,
        "available_slots": [
            {
                "start_time": "2025-06-11T10:00:00",
                "end_time": "2025-06-11T12:00:00"
            }
        ],
        "tasks": [
            {
                "title": "Mocked Essay",
                "due_date": "2025-06-11T23:59:59",
                "duration_minutes": 30,
                "category": "Test"
            }
        ]
    }

    with patch("app.call_openai_api", return_value=mock_response):
        response = client.post("/generate_ai_schedule/", json=request_data)
    assert response.status_code == 200
    data = response.json()
    assert data["user_id"] == "mock_user"
    assert len(data["sessions"]) == 1
    assert data["sessions"][0]["task"]["title"] == "Mocked Essay"
    assert data["sessions"][0]["task"]["category"] == "Mocking"
    assert data["sessions"][0]["start_time"] == "2025-06-11T10:00:00"
    assert data["sessions"][0]["end_time"] == "2025-06-11T10:30:00"
    assert data["success"] is True

def test_generate_ai_schedule_with_malformed_llm_response():
    bad_response = "This is now a string, not a valid JSON response."

    request_data = {
        "user_id": "bad_response_user",
        "energy_level": [3],
        "pomodoro_length": 25,
        "available_slots": [
            {
                "start_time": "2025-06-11T10:00:00",
                "end_time": "2025-06-11T12:00:00"
            }
        ],
        "tasks": [
            {
                "title": "Malformed Task",
                "due_date": "2025-06-11T23:59:59",
                "duration_minutes": 30,
                "category": "Broken"
            }
        ]
    }

    with patch("app.call_openai_api", return_value=bad_response):
        response = client.post("/generate_ai_schedule/", json=request_data)
    assert response.status_code == 500 or response.status_code == 400
    assert "Invalid response format from OpenAI API. Expected a list of session dictionaries." in response.json()["detail"]

def test_generate_ai_schedule_with_unschedulable_task():
    mock_response = [
        {
            "task": "First Task",
            "start": "2025-06-11T10:00:00",
            "end": "2025-06-11T10:25:00",
            "category": "First"
        }
    ]

    request_data = {
        "user_id": "test_unschedulable_user_2",
        "energy_level": [3],
        "pomodoro_length": 25,
        "available_slots": [
            {
                "start_time": "2025-06-11T10:00:00",
                "end_time": "2025-06-11T12:00:00"
            }
        ],
        "tasks": [
            {
                "title": "First Task",
                "due_date": "2025-06-11T23:59:59",
                "duration_minutes": 25,
                "category": "First"
            },
            {
                "title": "Skipped Task",
                "due_date": "2025-06-11T23:59:59",
                "duration_minutes": 30,
                "category": "Skipped"
            }
        ]
    }

    with patch("app.call_openai_api", return_value=mock_response):
        response = client.post("/generate_ai_schedule/", json=request_data)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is False
    assert "warnings" in data
    assert len(data["warnings"]) == 1
    assert "Skipped Task" in data["warnings"][0]