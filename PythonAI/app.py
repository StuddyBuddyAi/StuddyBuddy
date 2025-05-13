from fastapi import FastAPI
from pydantic import BaseModel
from ai_model import generate_schedule

app = FastAPI()

class StudyRequest(BaseModel):
    deadlines: list
    energy_levels: list

@app.post("/generate_schedule/")
def schedule(request: StudyRequest):
    return generate_schedule(request.deadlines, request.energy_levels)