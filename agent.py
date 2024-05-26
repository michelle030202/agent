from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, Any
from src.task_manager import task_manager

app = FastAPI()


class RunTaskRequest(BaseModel):
    task_type: str
    parameters: Dict[str, Any]


@app.post("/run_task")
async def run_task(request: RunTaskRequest):
    print("Received request:", request)
    task_type = request.task_type
    parameters = request.parameters
    try:
        result = task_manager.run_task(task_type, parameters)
        print("Task result:", result)
        return {"result": result}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        print("Error:", e)  # Log the error
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8001)
