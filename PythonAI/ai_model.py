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