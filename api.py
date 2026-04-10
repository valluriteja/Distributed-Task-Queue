from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from task_queue import push_task, r
import json

app = FastAPI(title="Task Queue API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class TaskRequest(BaseModel):
    task_type: str
    payload: dict
    priority: int = 1

@app.post("/tasks")
def create_task(request: TaskRequest):
    task_id = push_task(request.task_type, request.payload, request.priority)
    return {"message": "Task added!", "task_id": task_id}

@app.get("/stats")
def get_stats():
    return {
        "high_priority_queue": r.llen("high_priority_queue"),
        "normal_queue": r.llen("normal_queue"),
        "dead_letter_queue": r.llen("dead_letter_queue"),
    }

@app.get("/dead-letter")
def get_dead_letter_tasks():
    tasks = r.lrange("dead_letter_queue", 0, -1)
    return {"failed_tasks": [json.loads(t) for t in tasks]}

@app.get("/")
def root():
    return {"message": "Task Queue API is running! Go to /docs to test it."}