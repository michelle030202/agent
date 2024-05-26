from fastapi import FastAPI
from pydantic import BaseModel
from typing import Dict, Any
from task_manager import task_manager

app = FastAPI()


class RunTaskRequest(BaseModel):
    task_type: str
    parameters: Dict[str, Any]


@app.post("/run_task")
async def run_task(request: RunTaskRequest):
    print("Received request:", request)
    task_type = request.task_type
    parameters = request.parameters
    result = task_manager.run_task(task_type, parameters)
    print("Task result:", result)
    return {"result": result}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8001)
