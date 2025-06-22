import json
import re
from openai import OpenAI
from dotenv import load_dotenv
from datetime import timedelta
from typing import List
from models import StudyRequest, Session, ScheduleResponse

load_dotenv()  # Load environment variables from .env file

def generate_schedule(request: StudyRequest) -> ScheduleResponse:
    sessions: List[Session] = []
    remaining_tasks = sorted(request.tasks, key=lambda t: t.due_date) # Sort tasks by due date
    break_after = 5 # Default break after the session in minutes
    total_study_time = 0
    total_break_time = 0

    slot_index = 0
    while remaining_tasks and slot_index < len(request.available_slots):
        slot = request.available_slots[slot_index]
        slot_start = slot.start_time
        slot_end = slot.end_time

        while remaining_tasks and slot_start < slot_end:
            task = remaining_tasks[0]
            task_duration = timedelta(minutes=task.duration_minutes)

            # Check if the task fits in the current time slot
            if slot_start + task_duration <= slot_end:
                session = Session(
                    task=task,
                    start_time=slot_start,
                    end_time=slot_start + task_duration,
                    break_after=break_after
                )
                sessions.append(session)
                total_study_time += task.duration_minutes
                total_break_time += break_after
                slot_start += task_duration + timedelta(minutes=break_after)

                # Move to the next time slot after the session and break
                remaining_tasks.pop(0)
            else:
                # If the task doesn't fit, move to the next time slot
                break

        slot_index += 1
    
    return ScheduleResponse(
        user_id=request.user_id,
        sessions=sessions,
        total_study_time=total_study_time,
        total_break_time=total_break_time,
        success=len(remaining_tasks) == 0,
        message="All tasks scheduled successfully." if not remaining_tasks else "Some tasks could not be scheduled due to time constraints."
    )

def format_schedule_prompt(request: StudyRequest) -> str:
    """
    Converts a StudyRequest into a natural-language prompt string for the LLM.
    """
    lines = []
    lines.append(f"The user prefers a study session length of {request.pomodoro_length} minutes.")
    lines.append(f"Available time slots with energy levels for the user are:")
    for i, slot in enumerate(request.available_slots):
        energy = request.energy_level[i] if i < len(request.energy_level) else "unknown"
        start = slot.start_time.strftime("%A, %B %d at %I:%M %p") # Format time like Wednesday, June 11 at 05:29 PM
        end = slot.end_time.strftime("%I:%M %p")
        lines.append(f"- {start} to {end} (Energy Level: {energy})")
    
    lines.append("Tasks to be scheduled:")
    for task in request.tasks:
        due = task.due_date.strftime("%A, %B %d")
        category = f" [{task.category}]" if task.category else ""
        lines.append(f"- {task.title}{category}, {task.duration_minutes} due {due}")
    
    lines.append("\nPlease generate an optimized study schedule using the given constraints.")
    lines.append("Repond with ONLY a plain JSON array in the following format (do not use markdown):")
    lines.append("""
[
    {
        "task": "Write history essay",
        "start": "2025-06-11T10:00:00",
        "end": "2025-06-11T10:25:00",
        "category": "History",
    }
]
                 """)
    return "\n".join(lines)

def call_openai_api(prompt: str) -> List[dict]:
    """
    Sends the formatted prompt to OpenAI and returns the raw response text.
    """
    client = OpenAI()  # Initialize OpenAI client

    response = client.chat.completions.create(
        model = "gpt-4",
        messages = [
            {"role": "system", "content": "You are a helpful assistant that generates study schedules."},
            {"role": "user", "content": prompt}
        ],
        temperature = 0.7, # Adjust temperature for creativity vs. precision
        max_tokens = 1000, # Limit response length
        n = 1 # Number of responses to generate
    )
    text = response.choices[0].message.content.strip()

    # Extract JSON array from the response using regex (to avoid markdown formatting or text before/after)
    try:
        json_str = re.search(r"\[.*\]", text, re.DOTALL).group(0)
        return json.loads(json_str)
    except Exception as e:
        print(f"[ERROR] Failed to parse LLM response as JSON: {e}")
        return []