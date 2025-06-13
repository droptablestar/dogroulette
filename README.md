# 🐶 DogRoulette

DogRoulette is a full-stack web app that shows adoptable dogs near you, pulled
from the Petfinder API: https://www.petfinder.com/developers/v2/docs/.

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
docker-compose build backend  # first time only
```

Then can be run with
```bash
docker-compose up backend
```

### Frontend (Next.js)

```bash
docker-compose build frontend  # first time only
```

Then can be run with
```bash
docker-compose up frontend
```

App will run at http://localhost:3000

