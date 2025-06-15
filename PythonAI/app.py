import logging
from fastapi import FastAPI, HTTPException
from ai_model import generate_schedule, format_schedule_prompt, call_openai_api
from models import StudyRequest, ScheduleResponse

logging.basicConfig(level=logging.INFO)

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

@app.post("/generate_ai_schedule/")
def generate_ai_schedule_stub(request: StudyRequest):
    """
    Calls OpenAI API with a formatted schedule prompt and returns raw response text.
    """
    try:
        prompt = format_schedule_prompt(request)
        gpt_response = call_openai_api(prompt)
        return {
            "user_id": request.user_id,
            "gpt_response": gpt_response,
            "prompt_used": prompt, # for debugging
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))