Markdown
# 🚀 Mini GTM Enricher

A robust full-stack application designed to automate company data enrichment. Users can upload a CSV of domains, and the system fetches detailed company insights (Industry, Revenue, Size) using the **Explorium API** in the background.

---

## 🏗️ System Architecture

The project is built with a decoupled architecture to ensure high performance and scalability:

1.  **Frontend (React + Vite):** A modern UI for file uploads and live data tracking.
2.  **Backend (FastAPI):** High-performance API that handles file parsing and task delegation.
3.  **Task Queue (Celery + Redis):** Manages asynchronous jobs so the UI never freezes during API calls.
4.  **Database (PostgreSQL/SQLite):** Stores enrichment batches and company results persistently.



---

## 🛠️ Tech Stack

* **Frontend:** React, Tailwind CSS, Lucide-React (Icons), Axios.
* **Backend:** FastAPI (Python), SQLAlchemy (ORM).
* **Worker:** Celery.
* **Message Broker:** Redis.
* **Enrichment Provider:** Explorium API.

---

## ⚙️ Installation & Setup

### 1. Prerequisites
* Python 3.10+
* Node.js & npm
* Redis Server (Running on `localhost:6379`)

### 2. Backend Setup
```bash
cd backend
python -m venv venv
# Activate virtual environment
# Windows:
.\venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

pip install -r requirements.txt
3. Environment Variables
Create a .env file in the backend/ directory:

Code snippet
EXPLORIUM_API_KEY=your_api_key_here
CELERY_BROKER_URL=redis://localhost:6379/0
DATABASE_URL=sqlite:///./gtm_enricher.db
4. Frontend Setup
Bash
cd frontend
npm install
🚀 Running the Application
To run the full system, you need to open three terminals:

Terminal 1: FastAPI Server
Bash
cd backend
uvicorn app.main:app --reload
Terminal 2: Celery Worker
Bash
cd backend
celery -A app.worker.celery_app worker --loglevel=info -P solo
Terminal 3: React Frontend
Bash
cd frontend
npm run dev
📊 Features Implemented
✅ Domain Cleaning: Automatically extracts clean domains from URLs and Google search strings.

✅ Async Processing: Handles large CSVs without timing out.

✅ Polling Mechanism: Frontend automatically updates every 3 seconds to show new results.

✅ Error Handling: Gracefully handles API failures (422, 401) and reflects the status in the UI.

⚠️ Note for Reviewers
API Key: The enrichment logic requires a valid Explorium API key. If the key is missing or invalid, the system will mark rows as 'ERROR' but will not crash.

Worker Logs: Detailed API responses and payload structures can be monitored in the Celery worker terminal for debugging.

CSV Format: The system expects a .csv file with a column containing company domains or URLs.

📂 Project Structure
Plaintext
├── backend/
│   ├── app/
│   │   ├── main.py          # FastAPI Routes
│   │   ├── worker.py        # Celery Task & API Logic
│   │   ├── models.py        # Database Schema
│   │   └── database.py      # Connection Setup
│   └── .env                 # Secrets (Excluded in Git)
├── frontend/
│   ├── src/
│   │   ├── App.jsx          # Main UI Logic
│   │   └── services/api.js  # API Integration
└── README.md                # Documentation
