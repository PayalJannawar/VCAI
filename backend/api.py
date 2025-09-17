from fastapi import FastAPI
from pydantic import BaseModel
from backend.base_llm import BaseLLM
from backend.prompt_manager import PromptManager

app = FastAPI()
llm = BaseLLM()
pm = PromptManager()

class CodeRequest(BaseModel):
    task_type: str  # "generate_code", "explain_code", "debug_code"
    language: str = "Python"
    task: str = None
    code: str = None

@app.post("/code-assistant")
def code_assistant(req: CodeRequest):
    prompt = pm.build_prompt(
        task_type=req.task_type,
        language=req.language,
        task=req.task,
        code=req.code
    )
    response = llm.generate(prompt, max_tokens=300)
    return {"response": response}