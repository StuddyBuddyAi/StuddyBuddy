from fastapi import FastAPI, HTTPException
from ai_model import generate_schedule
from models import StudyRequest, ScheduleResponse

app = FastAPI()

@app.get("/ping")
def ping():
    return {"message": "pong"}

@app.post("/generate_schedule/", response_model=ScheduleResponse)
def schedule(request: StudyRequest):
    return generate_schedule(request)

@app.post("/generate_ai_schedule/")
def generate_ai_schedule_stub(request: StudyRequest):
    """
    This is a placeholder for the AI-based scheduling route.
    For now, it just confirms receipt of the request.
    """
    return {
        "status": "ok",
        "user_id": request.user_id,
        "num_tasks": len(request.tasks),
        "num_slots": len(request.available_slots),
        "message": "Stub endpoint for AI-based scheduling. LLM logic not implemented yet."
    }