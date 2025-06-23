import logging
from fastapi import FastAPI, HTTPException
from ai_model import generate_schedule, format_schedule_prompt, call_openai_api
from models import StudyRequest, ScheduleResponse
from utils import parse_llm_response

logging.basicConfig(level=logging.DEBUG)

app = FastAPI()

@app.get("/ping")
def ping():
    return {"message": "pong"}

@app.post("/generate_schedule/", response_model=ScheduleResponse)
def schedule(request: StudyRequest):
    # Log the incoming request for debugging
    logging.info(f"Received StudyRequest: user_id={request.user_id}, tasks={len(request.tasks)}, slots={len(request.available_slots)}")

    # Basic validation
    if not request.available_slots:
        raise HTTPException(status_code=400, detail="No available time slots provided.")
    if not request.tasks:
        raise HTTPException(status_code=400, detail="No tasks provided for scheduling.")
    if len(request.energy_level) < len(request.available_slots):
        raise HTTPException(status_code=400, detail="Not enough energy for available time slots.")
    return generate_schedule(request)

@app.post("/generate_ai_schedule/", response_model=ScheduleResponse)
def generate_ai_schedule(request: StudyRequest):
    """
    Calls OpenAI API with a formatted schedule prompt and returns raw response text.
    """
    try:
        prompt = format_schedule_prompt(request)
        gpt_response = call_openai_api(prompt)

        if not isinstance(gpt_response, list) or not all(isinstance(item, dict) for item in gpt_response):
            raise ValueError("Invalid response format from OpenAI API. Expected a list of session dictionaries.")

        sessions = parse_llm_response(gpt_response)

        total_study_time = sum([s.task.duration_minutes for s in sessions])
        total_break_time = sum([s.break_after for s in sessions if s.break_after])

        # Compare scheduled vs original tasks
        scheduled_tasks = {s.task.title for s in sessions}
        original_tasks = request.tasks
        unscheduled_tasks = [t for t in original_tasks if t.title not in scheduled_tasks]
        warnings = [
            f"ChatGPT did not include task '{task.title}' (due {task.due_date.strftime('%Y-%m-%d %H:%M')}) in the generated schedule." for task in unscheduled_tasks
        ]

        logging.info(f"Generated {len(sessions)} AI sessions for user {request.user_id}.")
        if sessions:
            logging.debug(f"First session: {sessions[0]!r}")
            logging.debug(f"All sessions: {sessions!r}")
        return ScheduleResponse(
            user_id=request.user_id,
            sessions=sessions,
            total_study_time=total_study_time,
            total_break_time=total_break_time,
            success=len(unscheduled_tasks) == 0,
            message="Schedule generated successfully." if not unscheduled_tasks else "Some tasks could not be scheduled due to time constraints.",
            warnings=warnings
        )
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=f"Invalid response format: {ve}")
    except Exception as e:
        logging.warning(f"AI scheduling failed: {e}. Falling back to rule-based scheduling.")
        fallback_response = generate_schedule(request)
        fallback_response.warnings.append(f"AI scheduling failed: {e}. Fallback to rule-based scheduling used.")
        fallback_response.message = "AI scheduling failed. Rule-based scheduling used instead."
        fallback_response.success = False # Fallback implies partial failure
        return fallback_response