from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class CodeRequest(BaseModel):
    task_type: str
    language: str
    task: str

@app.get("/")
async def root():
    return {"dir" : "root"}

@app.post("/code-assistant")
async def code_assistant(req: CodeRequest):
    return {
        "response": f"Received task '{req.task}' in {req.language} for {req.task_type}"
    }
