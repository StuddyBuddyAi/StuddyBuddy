from typing import List
from datetime import datetime, timedelta
from models import Session, Task

def parse_llm_response(text: str, reference_date: str, default_category: str = "General") -> List[Session]:
    """
    Parses raw LLM response into a list of Session objects.
    
    Args:
        text (str): The raw response from the LLM.
        reference_date (str): The date to use as a reference for task dates, in 'YYYY-MM-DD' format.
        default_category (str): The category to assign to tasks if not specified.
    
    Returns:
        List[Session]: A list of Session objects created from the parsed tasks.
    """
    sessions = []

    lines = text.splitlines()
    for line in lines:
        if "AM" in line or "PM" in line:
            try:
                # Example line: - 10:00 AM - 10:25 AM: Write history essay [History]
                time_part, task_part = line.split(":", 1)
                times = time_part.strip("-• ").split(" - ")
                task_title = task_part.split("[")[0].strip()
                category = task_part.split("[")[-1].replace("]", "").strip() if "[" in task_part else default_category

                start_dt = datetime.strptime(f"{reference_date} {times[0].strip()}", "%Y-%m-%d %I:%M %p")
                end_dt = datetime.strptime(f"{reference_date} {times[1].strip()}", "%Y-%m-%d %I:%M %p")

                task = Task(
                    title=task_title,
                    due_date=end_dt, # Assuming end date is the due date for now
                    duration_minutes=int((end_dt - start_dt).total_seconds() / 60),
                    category=category
                )

                sessions.append(Session(
                    task=task,
                    start_time=start_dt,
                    end_time=end_dt,
                    break_after=5
                ))
            except Exception as e:
                print(f"Error parsing line: {line} -> {e}")
                continue
    return sessions