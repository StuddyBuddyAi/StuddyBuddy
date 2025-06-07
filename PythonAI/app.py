from fastapi import FastAPI
from pydantic import BaseModel
from ai_model import generate_schedule
from models import StudyRequest, ScheduleResponse

app = FastAPI()

@app.get("/ping")
def ping():
    return {"message": "pong"}

@app.post("/generate_schedule/", response_model=ScheduleResponse)
def schedule(request: StudyRequest):
    return generate_schedule(request)