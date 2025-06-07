from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class Task(BaseModel):
    """A study task with required time, deadline, and optional category."""
    title: str
    due_date: datetime
    duration_minutes: int
    category: Optional[str] = None

class TimeSlot(BaseModel):
    """Represents an available block of time for scheduling study sessions."""
    start_time: datetime
    end_time: datetime

class StudyRequest(BaseModel):
    """
    Input payload for scheduling.

    Attributes:
        user_id: Identifier for the student or user.
        energy_level: A list representing energy values for each corresponding time slot.
        pomodoro_length: Preferred study block length in minutes (default: 25).
        available_slots: Time windows the user is free to study.
        tasks: List of tasks to schedule.
    """
    user_id: str
    energy_level: List[int]  # Energy levels for each time slot, e.g., [1, 2, 3]
    pomodoro_length: Optional[int] = 25  # Default Pomodoro length in minutes
    available_slots: List[TimeSlot]  # Available time slots for study
    tasks: List[Task]  # List of tasks with deadlines and durations

class Session(BaseModel):
    """
    Represents a scheduled study session.

    Attributes:
        task: The task being studied during the session.
        start_time: When the session starts.
        end_time: When the session ends.
        break_after: Suggested break duration after the session in minutes.
    """
    task: Task
    start_time: datetime
    end_time: datetime
    break_after: Optional[int] = 5  # Default break after the session in minutes

class ScheduleResponse(BaseModel):
    """
    Output model returned by the scheduling API.

    Attributes:
        user_id: The ID of the user the schedule was generated for.
        sessions: List of scheduled study sessions.
        total_study_time: Sum of all study durations in minutes.
        total_break_time: Sum of all break times in minutes.
        success: Whether all tasks were successfully scheduled.
        message: Additional info or error message.
    """
    user_id: str
    sessions: List[Session]  # List of scheduled study sessions
    total_study_time: int  # Total study time in minutes
    total_break_time: int  # Total break time in minutes
    success: bool = True  # Indicates if the schedule was successfully created
    message: Optional[str] = None  # Additional message or error description