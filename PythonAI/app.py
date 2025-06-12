from fastapi import FastAPI, HTTPException
from ai_model import generate_schedule, format_schedule_prompt, call_openai_api
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