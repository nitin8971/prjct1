# backend/main.py

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List

app = FastAPI()

# CORS middleware to allow cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET", "POST", "DELETE"], # Add OPTIONS method
    allow_headers=["*"],
)

class Task(BaseModel):
    id: int
    title: str
    description: str

tasks = []

@app.get("/tasks", response_model=List[Task])
async def get_tasks():
    print("GET /tasks endpoint hit")
    return tasks

@app.post("/tasks", response_model=Task)
async def create_task(task: Task):
    print("POST /tasks endpoint hit")
    print("Received task:", task)
    tasks.append(task)
    return task

@app.delete("/tasks/{task_id}", response_model=Task)
async def delete_task(task_id: int):
    print(f"DELETE /tasks/{task_id} endpoint hit")
    for task in tasks:
        if task.id == task_id:
            print("Deleted task:", task)
            tasks.remove(task)
            return task
    raise HTTPException(status_code=404, detail="Task not found")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)
