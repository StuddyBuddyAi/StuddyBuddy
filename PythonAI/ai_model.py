from datetime import datetime, timedelta
from typing import List
from models import Task, TimeSlot, StudyRequest, Session, ScheduleResponse

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
    lines.append(f"The user prefers a study session length of {request.session_length_minutes} minutes.")
    lines.append(f"Available time slots with energy levels for the user are:")
    for i, slot in enumerate(request.available_slots):
        energy = request.energy_level[i] if i < len(request.energy_level) else "unknown"
        start = slot.start_time.strftime("%A, %B %d at %I:%M %p")
        end = slot.end_time.strftime("%I:%M %p")
        lines.append(f"- {start} to {end} (Energy Level: {energy})")
    
    lines.append("Tasks to be scheduled:")
    for task in request.tasks:
        due = task.due_date.strftime("%A, %B %d")
        category = f" [{task.category}]" if task.category else ""
        lines.append(f"- {task.title}{category}, {task.duration_minutes} due {due}")
    
    lines.append("\nPlease generate an optimized study schedule using the given constraints.")
    return "\n".join(lines)