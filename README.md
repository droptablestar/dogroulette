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
# first time only
pre-commit install
docker-compose build backend
```

Then can be run with
```bash
docker-compose up backend
```
Backend will run at http://localhost:8000 and docs are available at `/docs`. 

#### Migrations
To generate a migration run the following:
```bash
alembic revision --autogenerate -m "Meaningful message here..."
```
This will create a file under alembic/versions/ with something like:
```python
op.alter_column("pet", "petfinder_id", existing_type=sa.VARCHAR(), type_=sa.INTEGER())
```

###### Apply the migration
```bash
alembic upgrade head
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

