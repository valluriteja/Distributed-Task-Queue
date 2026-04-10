import time
from task_queue import pop_task, push_task

MAX_RETRIES = 3

def process_task(task):
    """Actually execute the task"""
    print(f"⚙️  Processing: {task['type']} | ID: {task['id']}")
    
    if task["type"] == "send_email":
        print(f"📧 Sending email to: {task['payload']['to']}")
        time.sleep(1)
        
    elif task["type"] == "resize_image":
        print(f"🖼️  Resizing image: {task['payload']['filename']}")
        time.sleep(2)

    elif task["type"] == "failing_task":
        raise Exception("💥 This task always fails!")  # simulate a failure

    else:
        print(f"❓ Unknown task type: {task['type']}")
    
    print(f"✅ Done: {task['id']}")

def handle_failure(task, error):
    """Retry or send to dead letter queue"""
    task["retries"] += 1
    print(f"❌ Task failed: {task['id']} | Retries: {task['retries']} | Error: {error}")

    if task["retries"] < MAX_RETRIES:
        print(f"🔄 Retrying task: {task['id']}...")
        push_task(task["type"], task["payload"], task["priority"], retries=task["retries"])
    else:
        print(f"🪦 Max retries reached! Sending to dead letter queue: {task['id']}")
        from task_queue import push_to_dead_letter
        push_to_dead_letter(task)

def run_worker():
    """Keep running forever, picking up tasks"""
    print("🚀 Worker started, waiting for tasks...")
    while True:
        task = pop_task()
        if task:
            try:
                process_task(task)
            except Exception as e:
                handle_failure(task, str(e))
        else:
            print("😴 No tasks, sleeping for 2 seconds...")
            time.sleep(2)

if __name__ == "__main__":
    run_worker()