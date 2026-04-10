# ⚡ Distributed Task Queue

A production-grade distributed task queue built from scratch — similar to Celery or Amazon SQS — using Python, Redis, FastAPI and React.

## 🚀 Features
- **Priority Scheduling** — High priority tasks jump the queue
- **Auto Retries** — Failed tasks automatically retry 3 times
- **Dead Letter Queue** — Permanently failed tasks are tracked separately
- **REST API** — Submit and monitor tasks via FastAPI
- **Live Dashboard** — React dashboard that auto-refreshes every 3 seconds

## 🛠️ Tech Stack
- **Backend** — Python, FastAPI
- **Queue Storage** — Redis
- **Frontend** — React, Vite
- **Infrastructure** — Docker

## 📦 How to Run

### 1. Start Redis
```bash
docker run -d --name redis-task-queue -p 6379:6379 redis
```

### 2. Start the API
```bash
pip install -r requirements.txt
uvicorn api:app --reload
```

### 3. Start the Worker
```bash
python worker.py
```

### 4. Start the Dashboard
```bash
cd dashboard
npm install
npm run dev
```

Open `http://localhost:5173` to see the live dashboard.

## 🏗️ Architecture
