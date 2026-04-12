import time
import multiprocessing
from task_queue import pop_task, push_task, push_to_dead_letter

MAX_RETRIES = 3

def process_task(task):
    """Actually execute the task"""
    print(f"⚙️  [{multiprocessing.current_process().name}] Processing: {task['type']} | ID: {task['id']}")

    if task["type"] == "send_email":
        print(f"📧 Sending email to: {task['payload']['to']}")
        time.sleep(1)

    elif task["type"] == "resize_image":
        print(f"🖼️  Resizing image: {task['payload']['filename']}")
        time.sleep(2)

    elif task["type"] == "failing_task":
        raise Exception("💥 This task always fails!")

    else:
        print(f"❓ Unknown task type: {task['type']}")

    print(f"✅ [{multiprocessing.current_process().name}] Done: {task['id']}")

def handle_failure(task, error):
    """Retry or send to dead letter queue"""
    task["retries"] += 1
    print(f"❌ Task failed: {task['id']} | Retries: {task['retries']} | Error: {error}")

    if task["retries"] < MAX_RETRIES:
        print(f"🔄 Retrying task: {task['id']}...")
        push_task(task["type"], task["payload"], task["priority"], retries=task["retries"])
    else:
        print(f"🪦 Max retries reached! Sending to dead letter queue: {task['id']}")
        push_to_dead_letter(task)

def run_worker(worker_id):
    """Single worker loop"""
    print(f"🚀 Worker-{worker_id} started!")
    while True:
        task = pop_task()
        if task:
            try:
                process_task(task)
            except Exception as e:
                handle_failure(task, str(e))
        else:
            time.sleep(2)

def run_worker_pool(num_workers=3):
    """Launch multiple workers in parallel"""
    print(f"🏊 Starting worker pool with {num_workers} workers...")
    processes = []

    for i in range(num_workers):
        p = multiprocessing.Process(target=run_worker, args=(i+1,), name=f"Worker-{i+1}")
        p.start()
        processes.append(p)
        print(f"✅ Worker-{i+1} launched!")

    # Keep main process alive
    for p in processes:
        p.join()

if __name__ == "__main__":
    run_worker_pool(num_workers=3)