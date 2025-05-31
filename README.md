# 🐶 DogRoulette

DogRoulette is a full-stack web app that shows adoptable dogs near you, pulled from multiple pet adoption APIs.

## 🗂 Project Structure

```
dogroulette/
├── backend/ # FastAPI backend for dog API
├── frontend/ # Next.js frontend (React)
└── venv/ # Python virtual environment
```

## 🚀 Getting Started

### Backend (FastAPI)

```bash
source venv/bin/activate
pip install -r requirements.txt  # first time only
pre-commit install  # first time only
cd backend
uvicorn main:app --reload
```

### Frontend (Next.js)
```bash
cd frontend
npm install
npm run dev
```

App will run at http://localhost:3000

