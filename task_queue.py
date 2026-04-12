import redis
import json
import uuid
import os
from datetime import datetime

# Read host from environment variable (Docker sets this to 'redis', local is 'localhost')
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
r = redis.Redis(host=REDIS_HOST, port=6379, decode_responses=True)

def push_task(task_type: str, payload: dict, priority: int = 1, retries: int = 0):
    """Add a task to the queue — priority 2 = high, priority 1 = normal"""
    task = {
        "id": str(uuid.uuid4()),
        "type": task_type,
        "payload": payload,
        "priority": priority,
        "status": "pending",
        "created_at": datetime.now().isoformat(),
        "retries": retries
    }

    # High priority → different queue
    if priority == 2:
        r.lpush("high_priority_queue", json.dumps(task))
        print(f"🔴 HIGH priority task added: {task['id']} | Type: {task_type}")
    else:
        r.lpush("normal_queue", json.dumps(task))
        print(f"🟢 NORMAL task added: {task['id']} | Type: {task_type}")

    return task["id"]

def pop_task():
    """Always check high priority queue first!"""
    # Try high priority first
    task_data = r.rpop("high_priority_queue")
    if task_data:
        task = json.loads(task_data)
        print(f"🔴 Got HIGH priority task: {task['id']} | Type: {task['type']}")
        return task

    # Then check normal queue
    task_data = r.rpop("normal_queue")
    if task_data:
        task = json.loads(task_data)
        print(f"🟢 Got NORMAL task: {task['id']} | Type: {task['type']}")
        return task

    return None

def push_to_dead_letter(task):
    """Send a failed task to the dead letter queue"""
    task["status"] = "failed"
    task["failed_at"] = datetime.now().isoformat()
    r.lpush("dead_letter_queue", json.dumps(task))
    print(f"💀 Task in dead letter queue: {task['id']}")